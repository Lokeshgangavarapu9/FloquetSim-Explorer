"""
FloquetSim Explorer - Parameter Sweep & Benchmark Orchestration
Specification: Master Engineering Specification v1.2, Subphase 8.3, 8.4, 8.5
Executes Trotter sweeps (m=1..5) and time dynamics sweeps (t=1..10) without forcing curve shapes.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

from src.circuits import build_trotter_circuit
from src.classical_solver import simulate_exact_evolution, compute_exact_unitary
from src.processors import load_processor, get_processor_status
from src.transpiler import transpile_trotter_circuit
from src.noise import build_noise_model
from src.simulation import simulate_ideal_statevector, simulate_noisy_shots, simulate_ideal_shots
from src.observables import expectation_from_statevector, expectation_from_counts
from src.metrics import (
    extract_circuit_metrics,
    calculate_trotter_error,
    calculate_noise_error,
    calculate_total_error,
    calculate_shot_uncertainty,
)


def run_trotter_sweep(
    processor_id: str,
    trotter_steps_list: List[int] = None,
    fixed_time: float = 5.0,
    shots: int = 2048,
    seed: int = 42,
    noise_scale: float = 1.0,
) -> pd.DataFrame:
    """
    Execute systematic Trotter step sweep across m in trotter_steps_list at fixed evolution time.
    Compares ideal Trotter error vs noisy simulation error against exact classical reference.
    """
    if trotter_steps_list is None:
        trotter_steps_list = [1, 2, 3, 4, 5]

    config, cmap = load_processor(processor_id)
    noise_model = build_noise_model(config, scale_factor=noise_scale)

    # 1. Exact classical reference at fixed_time
    exact_res = simulate_exact_evolution(
        num_spins=4,
        time_points=[fixed_time],
        initial_state="0000",
    )
    exact_m = exact_res["staggered_m"][0]

    rows = []
    for m in trotter_steps_list:
        # Build logical circuit
        qc_logical = build_trotter_circuit(
            num_spins=4,
            trotter_steps=m,
            total_time=fixed_time,
            initial_state="0000",
            measure=False,
        )

        # Transpile against target coupling map
        qc_transpiled = transpile_trotter_circuit(
            circuit=qc_logical,
            coupling_map=cmap,
            basis_gates=config.basis_gates,
            optimization_level=1,
            seed_transpiler=seed,
        )

        metrics = extract_circuit_metrics(qc_transpiled, config)

        # Ideal statevector simulation (pure Trotter error)
        sv = simulate_ideal_statevector(qc_logical)
        _, _, ideal_m = expectation_from_statevector(sv, num_spins=4)

        # Noisy shot simulation (with hardware noise)
        noisy_counts = simulate_noisy_shots(
            circuit=qc_transpiled,
            noise_model=noise_model,
            shots=shots,
            seed=seed,
        )
        _, _, noisy_m = expectation_from_counts(noisy_counts, num_spins=4)

        err_trotter = calculate_trotter_error(ideal_m, exact_m)
        err_noise = calculate_noise_error(noisy_m, ideal_m)
        err_total = calculate_total_error(noisy_m, exact_m)
        shot_sigma = calculate_shot_uncertainty(noisy_m, shots)

        rows.append({
            "processor": config.processor_id,
            "trotter_steps": m,
            "fixed_time": fixed_time,
            "depth": metrics["circuit_depth"],
            "count_1q": metrics["count_1q_gates"],
            "count_2q": metrics["count_2q_gates"],
            "count_swap": metrics["count_swap_gates"],
            "total_gates": metrics["total_gates"],
            "exact_m": exact_m,
            "ideal_m": ideal_m,
            "noisy_m": noisy_m,
            "trotter_error": err_trotter,
            "noise_error": err_noise,
            "total_error": err_total,
            "shot_sigma": shot_sigma,
        })

    return pd.DataFrame(rows)


def run_time_dynamics_sweep(
    processor_id: str,
    time_list: List[float] = None,
    trotter_step: int = 3,
    shots: int = 2048,
    seed: int = 42,
    noise_scale: float = 1.0,
) -> pd.DataFrame:
    """
    Execute stroboscopic time evolution sweep across t in time_list at fixed Trotter steps.
    Compares dynamical trajectory between exact, ideal, and noisy execution.
    """
    if time_list is None:
        time_list = [float(t) for t in range(1, 11)]

    config, cmap = load_processor(processor_id)
    noise_model = build_noise_model(config, scale_factor=noise_scale)

    exact_res = simulate_exact_evolution(
        num_spins=4,
        time_points=time_list,
        initial_state="0000",
    )

    rows = []
    for idx, t in enumerate(time_list):
        exact_m = exact_res["staggered_m"][idx]

        qc_logical = build_trotter_circuit(
            num_spins=4,
            trotter_steps=trotter_step,
            total_time=t,
            initial_state="0000",
            measure=False,
        )

        qc_transpiled = transpile_trotter_circuit(
            circuit=qc_logical,
            coupling_map=cmap,
            basis_gates=config.basis_gates,
            optimization_level=1,
            seed_transpiler=seed,
        )

        sv = simulate_ideal_statevector(qc_logical)
        ideal_local_z, _, ideal_m = expectation_from_statevector(sv, num_spins=4)

        noisy_counts = simulate_noisy_shots(
            circuit=qc_transpiled,
            noise_model=noise_model,
            shots=shots,
            seed=seed,
        )
        noisy_local_z, _, noisy_m = expectation_from_counts(noisy_counts, num_spins=4)

        err_bar = calculate_shot_uncertainty(noisy_m, shots)
        exact_local_z = exact_res["local_z"][idx]

        row = {
            "processor": config.processor_id,
            "time": t,
            "trotter_steps": trotter_step,
            "exact_m": exact_m,
            "ideal_m": ideal_m,
            "noisy_m": noisy_m,
            "error_bar": err_bar,
        }
        for q in range(4):
            row[f"exact_z_{q}"] = float(exact_local_z[q])
            row[f"ideal_z_{q}"] = float(ideal_local_z[q])
            row[f"noisy_z_{q}"] = float(noisy_local_z[q])

        rows.append(row)

    return pd.DataFrame(rows)


def run_full_ab_benchmark(
    trotter_steps_list: List[int] = None,
    time_list: List[float] = None,
    shots: int = 2048,
    seed: int = 42,
) -> Dict[str, pd.DataFrame]:
    """
    Run the complete comparative A/B benchmark across both Processor A and Processor B.
    """
    df_trotter_a = run_trotter_sweep("demo_processor_A", trotter_steps_list, shots=shots, seed=seed)
    df_trotter_b = run_trotter_sweep("demo_processor_B", trotter_steps_list, shots=shots, seed=seed)
    df_trotter = pd.concat([df_trotter_a, df_trotter_b], ignore_index=True)

    df_time_a = run_time_dynamics_sweep("demo_processor_A", time_list, shots=shots, seed=seed)
    df_time_b = run_time_dynamics_sweep("demo_processor_B", time_list, shots=shots, seed=seed)
    df_time = pd.concat([df_time_a, df_time_b], ignore_index=True)

    # Circuit metrics summary
    df_metrics = df_trotter[["processor", "trotter_steps", "depth", "count_1q", "count_2q", "count_swap", "total_gates"]].copy()

    return {
        "trotter_sweep": df_trotter,
        "time_dynamics": df_time,
        "circuit_metrics": df_metrics,
    }
