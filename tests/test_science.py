"""
Unit Test Suite for Scientific Kernel Modules
Specification: Master Engineering Specification v1.2, Subphase 6.6
Tests Hermiticity, exact solver unitarity, observable estimators, and Trotter convergence.
"""

import pytest
import numpy as np
from src.hamiltonian import (
    build_zz_hamiltonian,
    build_x_hamiltonian,
    build_z_hamiltonian,
    build_total_hamiltonian,
)
from src.circuits import build_trotter_circuit
from src.classical_solver import (
    construct_dense_hamiltonian,
    compute_exact_unitary,
    simulate_exact_evolution,
)
from src.simulation import simulate_ideal_statevector, simulate_ideal_shots
from src.observables import expectation_from_statevector, expectation_from_counts


def test_hamiltonian_hermiticity_and_dimension():
    """Verify SparsePauliOp operators are Hermitian and have dimension 2^N."""
    num_spins = 4
    h_total = build_total_hamiltonian(num_spins=num_spins)
    dense_matrix = h_total.to_matrix()

    assert dense_matrix.shape == (16, 16)
    # Hermiticity: H = H^dagger
    assert np.allclose(dense_matrix, dense_matrix.conj().T, atol=1e-12)


def test_exact_solver_unitarity_and_probability_conservation():
    """Verify SciPy matrix exponential is strictly unitary and conserves state norm."""
    num_spins = 4
    total_time = 5.0
    U_exact = compute_exact_unitary(num_spins=num_spins, total_time=total_time)

    assert U_exact.shape == (16, 16)
    # Unitarity: U^dagger U = I
    eye = np.eye(16, dtype=complex)
    assert np.allclose(U_exact.conj().T @ U_exact, eye, atol=1e-12)

    # Determinant magnitude is 1.0
    assert abs(abs(np.linalg.det(U_exact)) - 1.0) < 1e-12


def test_observable_extraction_consistency():
    """Verify statevector and count-based observable extractions agree."""
    qc = build_trotter_circuit(num_spins=4, trotter_steps=3, total_time=2.0, initial_state="0101")
    sv = simulate_ideal_statevector(qc)
    local_z_sv, total_m_sv, stag_m_sv = expectation_from_statevector(sv, num_spins=4)

    # In ideal shots with high sample count, counts should match statevector within shot error
    counts = simulate_ideal_shots(qc, shots=8192, seed=42)
    local_z_shots, total_m_shots, stag_m_shots = expectation_from_counts(counts, num_spins=4)

    # Max shot noise ~ 1/sqrt(8192) ~ 0.011; tolerance 0.05
    assert np.allclose(local_z_sv, local_z_shots, atol=0.05)
    assert abs(total_m_sv - total_m_shots) < 0.05
    assert abs(stag_m_sv - stag_m_shots) < 0.05


def test_trotter_asymptotic_convergence():
    """
    Verify ideal Trotterized quantum circuit converges toward exact classical unitary
    as Trotter steps increase (testing overall asymptotic limit m=1 vs m=8).
    """
    num_spins = 4
    total_time = 1.0  # short time window for clean asymptotic test
    exact_res = simulate_exact_evolution(
        num_spins=num_spins,
        time_points=[total_time],
        initial_state="0000",
    )
    exact_stag_m = exact_res["staggered_m"][0]

    # m = 1 step
    qc_m1 = build_trotter_circuit(num_spins=num_spins, trotter_steps=1, total_time=total_time, initial_state="0000")
    sv_m1 = simulate_ideal_statevector(qc_m1)
    _, _, stag_m1 = expectation_from_statevector(sv_m1, num_spins=num_spins)
    err_m1 = abs(stag_m1 - exact_stag_m)

    # m = 8 steps
    qc_m8 = build_trotter_circuit(num_spins=num_spins, trotter_steps=8, total_time=total_time, initial_state="0000")
    sv_m8 = simulate_ideal_statevector(qc_m8)
    _, _, stag_m8 = expectation_from_statevector(sv_m8, num_spins=num_spins)
    err_m8 = abs(stag_m8 - exact_stag_m)

    # Asymptotic convergence: m=8 error should be substantially lower than m=1 error
    assert err_m8 < err_m1 or err_m8 < 1e-3
