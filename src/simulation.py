"""
FloquetSim Explorer - Quantum Simulation Dispatcher
Specification: Master Engineering Specification v1.2, Subphase 6.4 & 8.2
Dispatches execution across ideal statevector, ideal shots, and noisy shots.
"""

from typing import Dict, Any, Optional, Union
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel


def simulate_ideal_statevector(circuit: QuantumCircuit) -> np.ndarray:
    """
    Execute circuit using exact noiseless statevector simulation.
    Returns 1D complex128 NumPy array of state amplitudes (dimension 2^N).
    Circuit must NOT contain measurement gates.
    """
    circ_no_meas = circuit.remove_final_measurements(inplace=False)
    # Using Qiskit quantum_info Statevector or AerSimulator statevector
    try:
        sv = Statevector.from_instruction(circ_no_meas)
        return np.asarray(sv.data, dtype=np.complex128)
    except Exception:
        sim = AerSimulator(method="statevector")
        circ_save = circ_no_meas.copy()
        circ_save.save_statevector()
        result = sim.run(circ_save).result()
        return np.asarray(result.get_statevector(circ_save), dtype=np.complex128)


def simulate_ideal_shots(
    circuit: QuantumCircuit,
    shots: int = 2048,
    seed: int = 42,
) -> Dict[str, int]:
    """
    Execute circuit using noiseless shot-based measurement simulation.
    Automatically attaches measurements if missing.
    Returns dictionary of bitstrings and integer counts.
    """
    qc = circuit.copy()
    if not qc.cregs or qc.num_clbits < qc.num_qubits:
        qc.measure_all()

    sim = AerSimulator()
    result = sim.run(qc, shots=shots, seed_simulator=seed).result()
    return result.get_counts(qc)


def simulate_noisy_shots(
    circuit: QuantumCircuit,
    noise_model: Optional[NoiseModel] = None,
    shots: int = 2048,
    seed: int = 42,
) -> Dict[str, int]:
    """
    Execute circuit with physical gate errors, relaxation, and readout noise.
    """
    qc = circuit.copy()
    if not qc.cregs or qc.num_clbits < qc.num_qubits:
        qc.measure_all()

    sim = AerSimulator(noise_model=noise_model)
    result = sim.run(qc, shots=shots, seed_simulator=seed).result()
    return result.get_counts(qc)


def run_simulation(
    circuit: QuantumCircuit,
    mode: str = "noisy_shots",
    noise_model: Optional[NoiseModel] = None,
    shots: int = 2048,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Unified simulation dispatcher supporting:
    - 'ideal_statevector': exact infinite-shot noiseless statevector
    - 'ideal_shots': shot noise only, zero gate noise
    - 'noisy_shots': full hardware noise model with shot noise
    """
    if mode == "ideal_statevector":
        sv = simulate_ideal_statevector(circuit)
        return {"mode": mode, "statevector": sv, "counts": None}
    elif mode == "ideal_shots":
        counts = simulate_ideal_shots(circuit, shots=shots, seed=seed)
        return {"mode": mode, "statevector": None, "counts": counts, "shots": shots}
    elif mode == "noisy_shots":
        counts = simulate_noisy_shots(circuit, noise_model=noise_model, shots=shots, seed=seed)
        return {"mode": mode, "statevector": None, "counts": counts, "shots": shots}
    else:
        raise ValueError(f"Unknown simulation mode '{mode}'. Expected 'ideal_statevector', 'ideal_shots', or 'noisy_shots'.")
