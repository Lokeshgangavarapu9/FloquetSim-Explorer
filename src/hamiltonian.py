"""
FloquetSim Explorer - Hamiltonian & Pauli Operator Synthesis
Specification: Master Engineering Specification v1.2, Subphase 6.1
All Hamiltonian parameters have consistent units of angular frequency (rad/s, hbar=1).
"""

from typing import List, Tuple, Optional
import numpy as np
from qiskit.quantum_info import SparsePauliOp


def _make_pauli_string(num_qubits: int, qubit_ops: List[Tuple[int, str]]) -> str:
    """
    Construct a Qiskit little-endian Pauli string for specified qubit operators.
    In Qiskit, qubit index 0 corresponds to the right-most character (index -1).
    """
    chars = ["I"] * num_qubits
    for qubit_idx, op_char in qubit_ops:
        if not (0 <= qubit_idx < num_qubits):
            raise ValueError(f"Qubit index {qubit_idx} out of range for {num_qubits} qubits.")
        # Qubit k is at string position (num_qubits - 1 - k)
        chars[num_qubits - 1 - qubit_idx] = op_char
    return "".join(chars)


def build_zz_hamiltonian(
    num_spins: int = 4,
    J: float = 1.0,
    J_boundary: float = 1.0,
) -> SparsePauliOp:
    """
    Construct longitudinal Ising interaction Hamiltonian H_ZZ:
    H_ZZ = sum_{j=0}^{N-2} J * Z_j Z_{j+1} + J_boundary * Z_{N-1} Z_0
    Units: J, J_boundary in rad/s.
    """
    pauli_list = []
    # Nearest-neighbor chain terms
    for j in range(num_spins - 1):
        label = _make_pauli_string(num_spins, [(j, "Z"), (j + 1, "Z")])
        pauli_list.append((label, float(J)))

    # Periodic boundary condition term
    if num_spins > 2 and J_boundary != 0.0:
        boundary_label = _make_pauli_string(num_spins, [(num_spins - 1, "Z"), (0, "Z")])
        pauli_list.append((boundary_label, float(J_boundary)))

    return SparsePauliOp.from_list(pauli_list).simplify()


def build_x_hamiltonian(
    num_spins: int = 4,
    hx: float = 1.0,
    delta_hx: float = 0.05,
) -> SparsePauliOp:
    """
    Construct transverse magnetic field Hamiltonian H_X:
    H_X = sum_{j=0}^{N-1} (hx + delta_hx^j) * X_j
    Units: hx, delta_hx in rad/s.
    """
    pauli_list = []
    for j in range(num_spins):
        coeff = float(hx + delta_hx)
        label = _make_pauli_string(num_spins, [(j, "X")])
        pauli_list.append((label, coeff))

    return SparsePauliOp.from_list(pauli_list).simplify()


def build_z_hamiltonian(
    num_spins: int = 4,
    hz: float = 0.1,
) -> SparsePauliOp:
    """
    Construct longitudinal symmetry-breaking field Hamiltonian H_Z:
    H_Z = sum_{j=0}^{N-1} hz * Z_j
    Units: hz in rad/s.
    """
    pauli_list = []
    for j in range(num_spins):
        label = _make_pauli_string(num_spins, [(j, "Z")])
        pauli_list.append((label, float(hz)))

    return SparsePauliOp.from_list(pauli_list).simplify()


def build_total_hamiltonian(
    num_spins: int = 4,
    J: float = 1.0,
    J_boundary: float = 1.0,
    hx: float = 1.0,
    delta_hx: float = 0.05,
    hz: float = 0.1,
) -> SparsePauliOp:
    """
    Assemble the complete interacting Transverse-Field Ising Hamiltonian:
    H = H_ZZ + H_X + H_Z
    All terms are dimensionally consistent in rad/s.
    """
    h_zz = build_zz_hamiltonian(num_spins, J=J, J_boundary=J_boundary)
    h_x = build_x_hamiltonian(num_spins, hx=hx, delta_hx=delta_hx)
    h_z = build_z_hamiltonian(num_spins, hz=hz)
    return (h_zz + h_x + h_z).simplify()
