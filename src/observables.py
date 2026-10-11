"""
FloquetSim Explorer - Observable Extraction & Pauli Z Estimators
Specification: Master Engineering Specification v1.2, Subphase 6.5
Extracts local longitudinal magnetization, total magnetization, and spatial staggered magnetization.
"""

from typing import Dict, List, Tuple, Union, Optional
import numpy as np
from qiskit.quantum_info import SparsePauliOp


def expectation_from_statevector(statevector: np.ndarray, num_spins: int = 4) -> Tuple[List[float], float, float]:
    """
    Compute local <Z_j>, total magnetization M_tot, and spatial staggered magnetization M_stag
    from a 2^N statevector.
    Returns: (local_z_list, M_tot, M_stag)
    """
    probs = np.abs(statevector) ** 2
    local_z = []
    for j in range(num_spins):
        val = 0.0
        for k in range(len(statevector)):
            bit = (k >> j) & 1
            val += probs[k] * (1.0 if bit == 0 else -1.0)
        local_z.append(float(val))

    total_m = float(np.mean(local_z))
    staggered_m = float(np.mean([((-1) ** j) * val for j, val in enumerate(local_z)]))
    return local_z, total_m, staggered_m


def expectation_from_counts(counts: Dict[str, int], num_spins: int = 4) -> Tuple[List[float], float, float]:
    """
    Compute local <Z_j>, total magnetization M_tot, and spatial staggered magnetization M_stag
    from Qiskit measurement counts dictionary.
    In Qiskit counts, bitstring '0110' has qubit 0 as the rightmost character:
    qubit j corresponds to bitstring character at index (len(bitstring) - 1 - j).
    Returns: (local_z_list, M_tot, M_stag)
    """
    total_shots = sum(counts.values())
    if total_shots == 0:
        raise ValueError("Counts dictionary cannot have zero total shots.")

    local_z = []
    for j in range(num_spins):
        n_zero = 0
        n_one = 0
        for bitstring, count in counts.items():
            # Clean string
            b = bitstring.replace(" ", "")
            # Qubit j is at index (len(b) - 1 - j)
            char_idx = len(b) - 1 - j
            if char_idx < 0:
                raise ValueError(f"Bitstring '{bitstring}' too short for qubit index {j}")
            bit_val = b[char_idx]
            if bit_val == "0":
                n_zero += count
            elif bit_val == "1":
                n_one += count
            else:
                raise ValueError(f"Invalid character '{bit_val}' in bitstring '{bitstring}'")
        exp_z = (n_zero - n_one) / total_shots
        local_z.append(float(exp_z))

    total_m = compute_total_magnetization(local_z)
    staggered_m = compute_staggered_magnetization(local_z)
    return local_z, total_m, staggered_m


def compute_total_magnetization(local_z: List[float]) -> float:
    """
    Compute total spatial longitudinal magnetization:
    M_tot = (1 / N) * sum_{j=0}^{N-1} <Z_j>
    """
    return float(np.mean(local_z))


def compute_staggered_magnetization(local_z: List[float]) -> float:
    """
    Compute spatial staggered magnetization (antiferromagnetic order):
    M_stag = (1 / N) * sum_{j=0}^{N-1} (-1)^j * <Z_j>
    """
    return float(np.mean([((-1) ** j) * val for j, val in enumerate(local_z)]))
