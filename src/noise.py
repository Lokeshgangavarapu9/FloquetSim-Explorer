"""
FloquetSim Explorer - Synthetic Demonstration Noise Model Builder
Specification: Master Engineering Specification v1.2, Subphase 8.1
Constructs Qiskit Aer NoiseModel parameterized by illustrative synthetic error rates.
"""

from typing import List, Optional

try:
    from qiskit_aer.noise import (  # type: ignore
        NoiseModel,
        depolarizing_error,
        thermal_relaxation_error,
        ReadoutError,
    )
except ImportError:
    NoiseModel = None  # type: ignore
    depolarizing_error = None  # type: ignore
    thermal_relaxation_error = None  # type: ignore
    ReadoutError = None  # type: ignore

from src.schema import ProcessorConfig


def compute_readout_error_matrix(
    readout_error: List[float],
    scale_factor: float = 1.0,
) -> List[List[float]]:
    """
    Construct a 2x2 row-stochastic readout assignment matrix for Qiskit Aer ReadoutError.

    Parameters
    ----------
    readout_error : List[float]
        Pair [e01, e10] where:
        - e01 = P(measure 0 | true state 1) (readout error when preparing |1>)
        - e10 = P(measure 1 | true state 0) (readout error when preparing |0>)
    scale_factor : float
        Non-negative noise scale multiplier (default 1.0).

    Returns
    -------
    List[List[float]]
        2x2 assignment matrix compliant with Qiskit Aer ReadoutError convention:
        [
            [P(0|0), P(1|0)],  # Row 0: outcomes given true state |0>
            [P(0|1), P(1|1)]   # Row 1: outcomes given true state |1>
        ]
        Every element is in [0.0, 1.0] and every row sums to 1.0 within floating-point tolerance.

    Raises
    ------
    ValueError
        If scale_factor < 0.0, readout_error is invalid length, or rates are outside [0.0, 1.0].
    """
    if scale_factor < 0.0:
        raise ValueError(f"scale_factor must be >= 0.0, got {scale_factor}")

    if not readout_error or len(readout_error) != 2:
        raise ValueError(
            f"readout_error must contain exactly two rates [e01, e10], got {readout_error}"
        )

    e01, e10 = float(readout_error[0]), float(readout_error[1])
    if not (0.0 <= e01 <= 1.0 and 0.0 <= e10 <= 1.0):
        raise ValueError(
            f"Invalid readout error rates in configuration: [e01={e01}, e10={e10}]. "
            f"Rates must be valid probabilities in [0.0, 1.0]."
        )

    # Scale and clip error probabilities to valid probability range [0.0, 1.0]
    # For extreme scales (e.g. scale_factor >= 50.0), clipping prevents unphysical rates > 1.0
    scaled_e10 = min(1.0, max(0.0, e10 * scale_factor))
    scaled_e01 = min(1.0, max(0.0, e01 * scale_factor))

    # In Qiskit Aer's ReadoutError assignment matrix convention:
    # Row i represents the probability distribution of measured outcomes when true state is |i>.
    # Row 0 (true state |0>):
    #   Outcome 0: P(0|0) = 1.0 - P(1|0)
    #   Outcome 1: P(1|0) = scaled_e10
    # Row 1 (true state |1>):
    #   Outcome 0: P(0|1) = scaled_e01
    #   Outcome 1: P(1|1) = 1.0 - P(0|1)
    p10 = scaled_e10
    p00 = 1.0 - p10

    p01 = scaled_e01
    p11 = 1.0 - p01

    # Explicit normalization ensures rows sum to exactly 1.0 within floating-point tolerance
    row0_sum = p00 + p10
    row0 = [p00 / row0_sum, p10 / row0_sum] if row0_sum > 0.0 else [1.0, 0.0]

    row1_sum = p01 + p11
    row1 = [p01 / row1_sum, p11 / row1_sum] if row1_sum > 0.0 else [0.0, 1.0]

    return [row0, row1]


def build_noise_model(
    config: ProcessorConfig,
    scale_factor: float = 1.0,
) -> NoiseModel:
    """
    Construct Qiskit Aer NoiseModel based on ProcessorConfig parameters.
    Supports scaling factor for noise sweep studies.
    """
    if scale_factor < 0.0:
        raise ValueError(f"scale_factor must be >= 0.0, got {scale_factor}")

    if NoiseModel is None:
        raise ImportError(
            "Qiskit Aer is required to construct a NoiseModel. "
            "Please ensure qiskit-aer is installed in your cloud container."
        )

    noise_model = NoiseModel()
    n_params = config.noise

    # Scaled error rates
    p_1q = min(1.0, max(0.0, n_params.gate_error_1q * scale_factor))
    p_2q = min(1.0, max(0.0, n_params.gate_error_2q * scale_factor))

    # 1. Single-qubit depolarizing error
    if p_1q > 0.0:
        err_1q = depolarizing_error(p_1q, 1)
        # Apply to standard 1Q basis gates
        target_1q = [g for g in config.basis_gates if g in ["x", "sx"]]
        if not target_1q:
            target_1q = ["x", "sx"]
        noise_model.add_all_qubit_quantum_error(err_1q, target_1q)

    # 2. Two-qubit depolarizing error
    if p_2q > 0.0:
        err_2q = depolarizing_error(p_2q, 2)
        target_2q = [g for g in config.basis_gates if g in ["cx", "ecr"]]
        if not target_2q:
            target_2q = ["cx"]
        noise_model.add_all_qubit_quantum_error(err_2q, target_2q)

    # 3. Thermal relaxation error (optional physical channel)
    # T1, T2 in ns: 100 us = 100,000 ns, 80 us = 80,000 ns
    t1_ns = n_params.t1_us * 1e3
    t2_ns = n_params.t2_us * 1e3
    if t1_ns > 0 and t2_ns > 0 and t2_ns <= 2 * t1_ns:
        try:
            err_relax_1q = thermal_relaxation_error(t1_ns, t2_ns, n_params.gate_time_1q_ns)
            err_relax_2q = thermal_relaxation_error(t1_ns, t2_ns, n_params.gate_time_2q_ns).tensor(
                thermal_relaxation_error(t1_ns, t2_ns, n_params.gate_time_2q_ns)
            )
            # Relaxation can be optionally composed; keeping primarily depolarizing for benchmark stability
        except Exception:
            pass

    # 4. Measurement readout error
    if n_params.readout_error:
        probs = compute_readout_error_matrix(n_params.readout_error, scale_factor=scale_factor)
        ro_err = ReadoutError(probs)
        noise_model.add_all_qubit_readout_error(ro_err)

    return noise_model
