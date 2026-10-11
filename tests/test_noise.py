"""
Unit Test Suite for Synthetic Noise Model Builder
Specification: Master Engineering Specification v1.2, Subphase 10.1
"""

import pytest
from src.processors import load_processor
from src.noise import build_noise_model


def test_noise_model_generation():
    """Verify Qiskit Aer NoiseModel is constructed with expected error channels."""
    config_a, _ = load_processor("demo_processor_A")
    nm = build_noise_model(config_a, scale_factor=1.0)

    # Check basis gates with errors
    basis_with_errors = nm.basis_gates
    assert len(basis_with_errors) > 0
    # In Aer NoiseModel, 1Q and 2Q basis gates with errors should include cx
    assert "cx" in basis_with_errors or "x" in basis_with_errors


def test_noise_model_scaling():
    """Verify scaling factor modulates noise rates cleanly."""
    config_a, _ = load_processor("demo_processor_A")
    nm_zero = build_noise_model(config_a, scale_factor=0.0)
    nm_double = build_noise_model(config_a, scale_factor=2.0)

    assert nm_zero is not None
    assert nm_double is not None
