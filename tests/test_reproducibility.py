"""
Unit Test Suite for Transpiler Determinism & Reproducibility
Specification: Master Engineering Specification v1.2, Subphase 10.3
"""

import pytest
from src.circuits import build_trotter_circuit
from src.processors import load_processor
from src.transpiler import transpile_trotter_circuit
from src.metrics import extract_circuit_metrics


def test_transpilation_reproducibility_10_runs():
    """Verify bit-for-bit identical circuit depth and gate counts across 10 repeated seeded runs."""
    config_a, cmap_a = load_processor("demo_processor_A")
    qc = build_trotter_circuit(num_spins=4, trotter_steps=3, total_time=5.0)

    depths = []
    cnot_counts = []
    swap_counts = []

    for _ in range(10):
        transpiled = transpile_trotter_circuit(
            circuit=qc,
            coupling_map=cmap_a,
            basis_gates=config_a.basis_gates,
            optimization_level=1,
            seed_transpiler=42,
        )
        metrics = extract_circuit_metrics(transpiled, config_a)
        depths.append(metrics["circuit_depth"])
        cnot_counts.append(metrics["count_2q_gates"])
        swap_counts.append(metrics["count_swap_gates"])

    # Assert 0 variance across all 10 runs
    assert len(set(depths)) == 1
    assert len(set(cnot_counts)) == 1
    assert len(set(swap_counts)) == 1
