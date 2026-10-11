"""
Unit Test Suite for Physical Invariants & Limiting Cases
Specification: Master Engineering Specification v1.2, Subphase 10.2
"""

import pytest
import numpy as np
from src.classical_solver import construct_dense_hamiltonian, compute_exact_unitary
from src.circuits import build_trotter_circuit
from src.simulation import simulate_ideal_statevector, simulate_ideal_shots
from src.observables import expectation_from_statevector, expectation_from_counts


def test_uncoupled_single_spin_limit():
    """
    Limiting case J=0, hz=0: All spins evolve independently under H = hx * sum X_j.
    Analytical state for each spin: cos(hx * t) |0> - i sin(hx * t) |1>.
    Analytical <Z_j(t)> = cos^2(hx * t) - sin^2(hx * t) = cos(2 * hx * t).
    """
    hx = 1.0
    t = 0.5
    H_uncoupled = construct_dense_hamiltonian(
        num_spins=4,
        J=0.0,
        J_boundary=0.0,
        hz=0.0,
        hx=hx,
        delta_hx=0.0,
    )
    U = compute_exact_unitary(
        num_spins=4,
        total_time=t,
        J=0.0,
        J_boundary=0.0,
        hz=0.0,
        hx=hx,
        delta_hx=0.0,
    )

    psi_0 = np.zeros(16, dtype=complex)
    psi_0[0] = 1.0  # |0000>
    psi_t = U @ psi_0

    local_z, total_m, _ = expectation_from_statevector(psi_t, num_spins=4)
    expected_z = np.cos(2.0 * hx * t)

    for val in local_z:
        assert abs(val - expected_z) < 1e-10
    assert abs(total_m - expected_z) < 1e-10


def test_magnetization_bounds_and_probability_sum():
    """Verify expectation values are bounded in [-1.0, 1.0] and probabilities sum to 1.0."""
    qc = build_trotter_circuit(num_spins=4, trotter_steps=3, total_time=5.0)
    sv = simulate_ideal_statevector(qc)

    # Probability sum
    probs = np.abs(sv) ** 2
    assert abs(np.sum(probs) - 1.0) < 1e-12

    local_z, total_m, stag_m = expectation_from_statevector(sv, num_spins=4)
    for z in local_z:
        assert -1.0 - 1e-12 <= z <= 1.0 + 1e-12
    assert -1.0 - 1e-12 <= total_m <= 1.0 + 1e-12
    assert -1.0 - 1e-12 <= stag_m <= 1.0 + 1e-12
