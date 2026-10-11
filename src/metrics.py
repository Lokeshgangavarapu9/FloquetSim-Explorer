"""
FloquetSim Explorer - Circuit Metrics & Error Analysis Module
Specification: Master Engineering Specification v1.2, Subphase 7.5 & 8.6
Extracts depth, gate counts, SWAP overhead, and computes statistical and physical errors.
"""

import math
from typing import Dict, Any, Optional
from qiskit import QuantumCircuit
from src.schema import ProcessorConfig


def extract_circuit_metrics(
    circuit: QuantumCircuit,
    config: Optional[ProcessorConfig] = None,
) -> Dict[str, Any]:
    """
    Extract quantitative structural and resource metrics from compiled QuantumCircuit.
    """
    ops = circuit.count_ops()

    # Gate categorization
    names_1q = {"rz", "sx", "x", "h", "s", "sdg", "t", "tdg", "rx", "ry"}
    names_2q = {"cx", "cz", "ecr", "swap", "rxx", "ryy", "rzz"}

    count_1q = sum(count for op, count in ops.items() if op.lower() in names_1q)
    count_2q = sum(count for op, count in ops.items() if op.lower() in names_2q)
    count_swap = ops.get("swap", 0)
    total_gates = sum(ops.values())

    # Execution duration estimate based on config gate durations
    duration_ns = 0.0
    if config is not None:
        duration_ns += count_1q * config.noise.gate_time_1q_ns
        duration_ns += count_2q * config.noise.gate_time_2q_ns

    return {
        "circuit_depth": circuit.depth(),
        "num_qubits": circuit.num_qubits,
        "total_gates": total_gates,
        "count_1q_gates": count_1q,
        "count_2q_gates": count_2q,
        "count_swap_gates": count_swap,
        "estimated_duration_ns": duration_ns,
        "raw_ops": dict(ops),
    }


def calculate_trotter_error(ideal_val: float, exact_val: float) -> float:
    """
    Algorithmic Trotter error: |M_ideal - M_exact|
    """
    return float(abs(ideal_val - exact_val))


def calculate_noise_error(noisy_val: float, ideal_val: float) -> float:
    """
    Hardware noise error: |M_noisy - M_ideal|
    """
    return float(abs(noisy_val - ideal_val))


def calculate_total_error(noisy_val: float, exact_val: float) -> float:
    """
    Total simulation error: |M_noisy - M_exact|
    """
    return float(abs(noisy_val - exact_val))


def calculate_shot_uncertainty(exp_val: float, shots: int = 2048) -> float:
    """
    Theoretical binomial shot noise standard deviation:
    sigma = sqrt((1 - <Z>^2) / shots)
    """
    if shots <= 0:
        return 0.0
    # Clamp exp_val to [-1, 1] to avoid negative variance under numerical noise
    clamped_val = max(-1.0, min(1.0, exp_val))
    variance = max(0.0, 1.0 - (clamped_val ** 2))
    return float(math.sqrt(variance / shots))
