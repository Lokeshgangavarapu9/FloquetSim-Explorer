"""
Unit Test Suite for Failure Resilience & Edge-Case Handling
Specification: Master Engineering Specification v1.2, Subphase 10.6
"""

import pytest
from src.circuits import build_trotter_circuit
from src.processors import load_processor
from src.simulation import run_simulation
from src.noise import build_noise_model


def test_invalid_trotter_steps_raises_value_error():
    """Verify non-positive trotter_steps raises clear ValueError."""
    with pytest.raises(ValueError, match="trotter_steps must be >= 1"):
        build_trotter_circuit(num_spins=4, trotter_steps=0, total_time=5.0)

    with pytest.raises(ValueError, match="trotter_steps must be >= 1"):
        build_trotter_circuit(num_spins=4, trotter_steps=-2, total_time=5.0)


def test_invalid_time_raises_value_error():
    """Verify negative total_time raises clear ValueError."""
    with pytest.raises(ValueError, match="total_time must be >= 0.0"):
        build_trotter_circuit(num_spins=4, trotter_steps=3, total_time=-1.0)


def test_invalid_initial_state_length():
    """Verify mismatch between initial_state length and num_spins raises ValueError."""
    with pytest.raises(ValueError, match="initial_state length"):
        build_trotter_circuit(num_spins=4, trotter_steps=3, total_time=1.0, initial_state="00")


def test_extreme_noise_parameter_does_not_crash():
    """Verify simulation completes cleanly even under high noise scale."""
    config_a, _ = load_processor("demo_processor_A")
    nm_extreme = build_noise_model(config_a, scale_factor=10.0)

    qc = build_trotter_circuit(num_spins=4, trotter_steps=1, total_time=1.0)
    res = run_simulation(qc, mode="noisy_shots", noise_model=nm_extreme, shots=256, seed=42)
    assert res["counts"] is not None
    assert sum(res["counts"].values()) == 256
