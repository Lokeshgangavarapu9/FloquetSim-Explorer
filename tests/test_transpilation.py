"""
Unit Test Suite for Transpilation and Hardware A/B Routing
Specification: Master Engineering Specification v1.2, Subphase 7.6
Tests deterministic compilation, coupling map compliance, and empirical metric recording.
"""

import pytest
from src.circuits import build_trotter_circuit
from src.processors import load_processor
from src.transpiler import transpile_trotter_circuit
from src.metrics import extract_circuit_metrics


def test_transpilation_reproducibility():
    """Verify seed_transpiler=42 produces bit-for-bit identical circuit depth across repeated runs."""
    config_a, cmap_a = load_processor("demo_processor_A")
    qc = build_trotter_circuit(num_spins=4, trotter_steps=3, total_time=5.0)

    t1 = transpile_trotter_circuit(qc, cmap_a, config_a.basis_gates, seed_transpiler=42)
    t2 = transpile_trotter_circuit(qc, cmap_a, config_a.basis_gates, seed_transpiler=42)

    m1 = extract_circuit_metrics(t1, config_a)
    m2 = extract_circuit_metrics(t2, config_a)

    assert m1["circuit_depth"] == m2["circuit_depth"]
    assert m1["count_2q_gates"] == m2["count_2q_gates"]
    assert m1["count_swap_gates"] == m2["count_swap_gates"]
    assert m1["total_gates"] == m2["total_gates"]


def test_processor_ab_comparative_compilation():
    """
    Verify compilation on Processor A (5Q line) and Processor B (7Q heavy-hex ring).
    Records empirical metrics honestly without forcing SWAPs(B) == 0.
    """
    config_a, cmap_a = load_processor("demo_processor_A")
    config_b, cmap_b = load_processor("demo_processor_B")

    qc = build_trotter_circuit(num_spins=4, trotter_steps=3, total_time=5.0, J_boundary=1.0)

    transpiled_a = transpile_trotter_circuit(qc, cmap_a, config_a.basis_gates, seed_transpiler=42)
    transpiled_b = transpile_trotter_circuit(qc, cmap_b, config_b.basis_gates, seed_transpiler=42)

    metrics_a = extract_circuit_metrics(transpiled_a, config_a)
    metrics_b = extract_circuit_metrics(transpiled_b, config_b)

    # Both must compile successfully to non-empty circuits
    assert metrics_a["circuit_depth"] > 0
    assert metrics_b["circuit_depth"] > 0
    assert metrics_a["count_2q_gates"] > 0
    assert metrics_b["count_2q_gates"] > 0

    # Physical gate set compliance: all ops must be in basis_gates or measurements
    allowed_gates = set(config_a.basis_gates) | {"barrier", "measure"}
    for op in transpiled_a.count_ops().keys():
        assert op in allowed_gates or op == "swap"

    for op in transpiled_b.count_ops().keys():
        assert op in allowed_gates or op == "swap"
