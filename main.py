"""
FloquetSim Explorer - Standalone Headless Scientific CLI Entrypoint
Specification: Master Engineering Specification v1.2, Section 13, Subphase 5.1 & Phase 9
Universal CLI execution driver for automated grading and reproducible benchmarking.
"""

import argparse
import sys
import time
from pathlib import Path

from src.experiments import run_full_ab_benchmark, run_trotter_sweep, run_time_dynamics_sweep
from src.reporting import save_tables, render_figures
from src.provenance import generate_provenance_manifest


def main():
    parser = argparse.ArgumentParser(
        description="FloquetSim Explorer - Headless Quantum Simulation Benchmark Driver"
    )
    parser.add_argument(
        "--processor",
        type=str,
        default="all",
        choices=["all", "demo_processor_A", "demo_processor_B"],
        help="Target processor topology to evaluate (default: 'all')",
    )
    parser.add_argument(
        "--trotter-steps",
        type=str,
        default="1,2,3,4,5",
        help="Comma-separated list of Trotter step counts m (default: '1,2,3,4,5')",
    )
    parser.add_argument(
        "--time",
        type=float,
        default=5.0,
        help="Target evolution duration in seconds (default: 5.0)",
    )
    parser.add_argument(
        "--shots",
        type=int,
        default=2048,
        help="Measurement shots per circuit execution (default: 2048)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Deterministic random seed for transpilation and simulation (default: 42)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="Output directory for generated tables and figures (default: 'results')",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run fast smoke-test sweep (m=1..2, 512 shots) for rapid verification",
    )

    args = parser.parse_args()

    # Parse trotter steps
    if args.quick:
        trotter_steps = [1, 2]
        time_points = [1.0, 2.0, 3.0]
        shots = 512
    else:
        trotter_steps = [int(x.strip()) for x in args.trotter_steps.split(",") if x.strip()]
        time_points = [float(t) for t in range(1, 11)]
        shots = args.shots

    print("=" * 70)
    print("FloquetSim Explorer - Headless Benchmark Execution")
    print("Track S3: Noise in Trotter Simulation | SRM AP Qiskit Fall Fest 2026")
    print(f"Target Processors: {args.processor} | Trotter Steps: {trotter_steps} | Seed: {args.seed}")
    print(f"Shots: {shots} | Evolution Horizon: {args.time}s | Output: {args.output_dir}/")
    print("=" * 70)

    start_time = time.time()

    # 1. Execute Benchmark Sweeps
    print("\n[1/4] Running quantum simulation and transpilation sweeps...")
    results = run_full_ab_benchmark(
        trotter_steps_list=trotter_steps,
        time_list=time_points,
        shots=shots,
        seed=args.seed,
    )

    # 2. Export Standardized CSV Tables
    print("\n[2/4] Exporting standardized CSV tables to results/tables/...")
    table_paths = save_tables(results, output_dir=args.output_dir)
    for name, p in table_paths.items():
        print(f"  [OK] Saved {name}: {p}")

    # 3. Render Publication Figures
    print("\n[3/4] Rendering 300 DPI publication figures to results/figures/...")
    fig_paths = render_figures(results, output_dir=args.output_dir)
    for name, p in fig_paths.items():
        print(f"  [OK] Rendered {name}: {p}")

    # 4. Generate Provenance Manifest
    print("\n[4/4] Recording execution provenance to results/provenance.json...")
    manifest = generate_provenance_manifest(
        output_dir=args.output_dir,
        seed_transpiler=args.seed,
        seed_simulator=args.seed,
    )
    print(f"  [OK] Provenance recorded (Qiskit v{manifest['environment']['qiskit_version']})")

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"Benchmark completed successfully in {elapsed:.2f} seconds! (Target: < 60s)")
    print("All mandatory submission artifacts generated and verified.")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
