"""
FloquetSim Explorer - Exact Classical Reference Solver
Specification: Master Engineering Specification v1.2, Subphase 6.3
Evaluates exact time evolution via SciPy dense matrix exponentiation (scipy.linalg.expm).
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import scipy.linalg


# Single-qubit Pauli matrices
_PAULI_I = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.complex128)
_PAULI_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
_PAULI_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=np.complex128)
_PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)


def construct_dense_hamiltonian(
    num_spins: int = 4,
    J: float = 1.0,
    J_boundary: float = 1.0,
    hz: float = 0.1,
    hx: float = 1.0,
    delta_hx: float = 0.05,
) -> np.ndarray:
    """
    Construct the dense 2^N x 2^N Hamiltonian matrix H = H_ZZ + H_X + H_Z.
    Qubit 0 is the least significant qubit (right-most in Kronecker product).
    """
    dim = 2 ** num_spins
    H = np.zeros((dim, dim), dtype=np.complex128)

    def _embed_single(op: np.ndarray, target: int) -> np.ndarray:
        # Kronecker product: q_{N-1} x ... x q_1 x q_0
        res = np.array([[1.0]], dtype=np.complex128)
        for q in reversed(range(num_spins)):
            res = np.kron(res, op if q == target else _PAULI_I)
        return res

    def _embed_pair(op1: np.ndarray, target1: int, op2: np.ndarray, target2: int) -> np.ndarray:
        res = np.array([[1.0]], dtype=np.complex128)
        for q in reversed(range(num_spins)):
            if q == target1:
                cur = op1
            elif q == target2:
                cur = op2
            else:
                cur = _PAULI_I
            res = np.kron(res, cur)
        return res

    # 1. H_ZZ terms: sum J * Z_j Z_{j+1} + J_boundary * Z_{N-1} Z_0
    for j in range(num_spins - 1):
        H += J * _embed_pair(_PAULI_Z, j, _PAULI_Z, j + 1)
    if num_spins > 2 and J_boundary != 0.0:
        H += J_boundary * _embed_pair(_PAULI_Z, num_spins - 1, _PAULI_Z, 0)

    # 2. H_X terms: sum (hx + delta_hx) * X_j
    for j in range(num_spins):
        H += (hx + delta_hx) * _embed_single(_PAULI_X, j)

    # 3. H_Z terms: sum hz * Z_j
    for j in range(num_spins):
        H += hz * _embed_single(_PAULI_Z, j)

    # Verify Hermiticity
    diff = np.max(np.abs(H - H.conj().T))
    if diff > 1e-14:
        raise ValueError(f"Constructed Hamiltonian is non-Hermitian! Max diff: {diff}")

    return H


def compute_exact_unitary(
    num_spins: int = 4,
    total_time: float = 5.0,
    J: float = 1.0,
    J_boundary: float = 1.0,
    hz: float = 0.1,
    hx: float = 1.0,
    delta_hx: float = 0.05,
) -> np.ndarray:
    """
    Compute exact continuous time evolution operator U_exact(t) = exp(-i H t).
    Guarantees unitarity to < 1e-14 tolerance.
    """
    H = construct_dense_hamiltonian(
        num_spins=num_spins,
        J=J,
        J_boundary=J_boundary,
        hz=hz,
        hx=hx,
        delta_hx=delta_hx,
    )
    U = scipy.linalg.expm(-1.0j * H * total_time)

    # Unitarity check
    dim = 2 ** num_spins
    eye = np.eye(dim, dtype=np.complex128)
    unitarity_dev = np.max(np.abs(U.conj().T @ U - eye))
    if unitarity_dev > 1e-12:
        raise ValueError(f"Unitarity deviation {unitarity_dev} exceeds tolerance 1e-12.")

    return U


def build_initial_statevector(num_spins: int = 4, initial_state: str = "0000") -> np.ndarray:
    """
    Construct initial statevector in computational basis.
    initial_state is string of '0' and '1' of length num_spins.
    """
    dim = 2 ** num_spins
    psi = np.zeros(dim, dtype=np.complex128)
    # Binary index conversion: q_0 is least significant bit
    idx = 0
    for j, bit in enumerate(initial_state):
        if bit == "1":
            idx += (1 << j)
    psi[idx] = 1.0 + 0.0j
    return psi


def compute_exact_magnetization(
    statevector: np.ndarray,
    num_spins: int = 4,
) -> Tuple[List[float], float, float]:
    """
    Compute exact local Z expectations, total magnetization, and staggered magnetization
    from a dense statevector.
    Returns: (local_z_list, total_m, staggered_m)
    """
    local_z = []
    # For qubit j, <Z_j> = sum_k |psi_k|^2 * (+1 if bit j is 0 else -1)
    probs = np.abs(statevector) ** 2
    for j in range(num_spins):
        z_val = 0.0
        for k in range(len(statevector)):
            bit = (k >> j) & 1
            z_val += probs[k] * (1.0 if bit == 0 else -1.0)
        local_z.append(float(z_val))

    total_m = float(np.mean(local_z))
    # Staggered: 1/N sum (-1)^j <Z_j>
    staggered_m = float(np.mean([((-1) ** j) * val for j, val in enumerate(local_z)]))

    return local_z, total_m, staggered_m


def simulate_exact_evolution(
    num_spins: int = 4,
    time_points: List[float] = None,
    initial_state: str = "0000",
    J: float = 1.0,
    J_boundary: float = 1.0,
    hz: float = 0.1,
    hx: float = 1.0,
    delta_hx: float = 0.05,
) -> Dict[str, Any]:
    """
    Compute exact trajectory across time_points.
    """
    if time_points is None:
        time_points = [float(t) for t in range(1, 11)]

    H = construct_dense_hamiltonian(
        num_spins=num_spins,
        J=J,
        J_boundary=J_boundary,
        hz=hz,
        hx=hx,
        delta_hx=delta_hx,
    )
    psi_0 = build_initial_statevector(num_spins, initial_state)

    results = {
        "time_points": time_points,
        "local_z": [],
        "total_m": [],
        "staggered_m": [],
        "statevectors": [],
    }

    for t in time_points:
        U_t = scipy.linalg.expm(-1.0j * H * t)
        psi_t = U_t @ psi_0
        local_z, total_m, stag_m = compute_exact_magnetization(psi_t, num_spins)
        results["local_z"].append(local_z)
        results["total_m"].append(total_m)
        results["staggered_m"].append(stag_m)
        results["statevectors"].append(psi_t)

    return results
