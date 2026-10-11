"""
FloquetSim Explorer - Synthetic Demonstration Noise Model Builder
Specification: Master Engineering Specification v1.2, Subphase 8.1
Constructs Qiskit Aer NoiseModel parameterized by illustrative synthetic error rates.
"""

from typing import Optional
from qiskit_aer.noise import (
    NoiseModel,
    depolarizing_error,
    thermal_relaxation_error,
    ReadoutError,
)
from src.schema import ProcessorConfig


def build_noise_model(
    config: ProcessorConfig,
    scale_factor: float = 1.0,
) -> NoiseModel:
    """
    Construct Qiskit Aer NoiseModel based on ProcessorConfig parameters.
    Supports scaling factor for noise sweep studies.
    """
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
    if n_params.readout_error and len(n_params.readout_error) == 2:
        e01, e10 = n_params.readout_error
        # Scaled readout confusion matrix: [[P(0|0), P(1|0)], [P(0|1), P(1|1)]]
        p00 = 1.0 - (e10 * scale_factor)
        p10 = e10 * scale_factor
        p01 = e01 * scale_factor
        p11 = 1.0 - (e01 * scale_factor)
        # Ensure valid probability distribution in each column
        probs = [
            [max(0.0, min(1.0, p00)), max(0.0, min(1.0, p01))],
            [max(0.0, min(1.0, p10)), max(0.0, min(1.0, p11))],
        ]
        ro_err = ReadoutError(probs)
        noise_model.add_all_qubit_readout_error(ro_err)

    return noise_model
