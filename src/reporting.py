"""
FloquetSim Explorer - Scientific Results Reporting & Figure Generation
Specification: Master Engineering Specification v1.2, Subphase 9.1 & 9.2
Exports standardized CSV tables and renders publication-grade 300 DPI figures using matplotlib (Agg backend).
"""

from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("Agg")  # Strictly headless backend
import matplotlib.pyplot as plt
from src.mitigation import compute_fourier_spectrum


def save_tables(
    benchmark_results: Dict[str, pd.DataFrame],
    output_dir: str = "results",
) -> Dict[str, Path]:
    """
    Save standardized machine-readable CSV tables into output_dir/tables/.
    """
    tables_dir = Path(output_dir) / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    paths = {}

    # 1. Circuit metrics comparison
    if "circuit_metrics" in benchmark_results:
        p1 = tables_dir / "circuit_metrics_comparison.csv"
        benchmark_results["circuit_metrics"].to_csv(p1, index=False)
        paths["circuit_metrics"] = p1

    # 2. Trotter sweep results
    if "trotter_sweep" in benchmark_results:
        p2 = tables_dir / "trotter_sweep_results.csv"
        benchmark_results["trotter_sweep"].to_csv(p2, index=False)
        paths["trotter_sweep"] = p2

    # 3. Time evolution dynamics
    if "time_dynamics" in benchmark_results:
        p3 = tables_dir / "time_evolution_results.csv"
        benchmark_results["time_dynamics"].to_csv(p3, index=False)
        paths["time_dynamics"] = p3

    return paths


def render_figures(
    benchmark_results: Dict[str, pd.DataFrame],
    output_dir: str = "results",
) -> Dict[str, Path]:
    """
    Render publication-quality 300 DPI scientific figures into output_dir/figures/.
    """
    figures_dir = Path(output_dir) / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    paths = {}

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # -------------------------------------------------------------
    # Figure 1: Trotter-Noise Trade-off (Error vs Trotter Steps m)
    # -------------------------------------------------------------
    if "trotter_sweep" in benchmark_results:
        df = benchmark_results["trotter_sweep"]
        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

        # Plot ideal Trotter error (Processor A line)
        df_a = df[df["processor"] == "demo_processor_A"]
        df_b = df[df["processor"] == "demo_processor_B"]

        if not df_a.empty:
            ax.plot(
                df_a["trotter_steps"],
                df_a["trotter_error"],
                "k--",
                marker="o",
                label="Ideal Algorithmic Trotter Error",
            )
            ax.plot(
                df_a["trotter_steps"],
                df_a["total_error"],
                color="#2563eb",
                marker="s",
                linewidth=2,
                label="Processor A Total Error (5Q Line)",
            )
        if not df_b.empty:
            ax.plot(
                df_b["trotter_steps"],
                df_b["total_error"],
                color="#dc2626",
                marker="^",
                linewidth=2,
                label="Processor B Total Error (7Q Heavy-Hex)",
            )

        ax.set_title("Trotter-Noise Competition: Error vs. Discretization Steps", fontsize=13, fontweight="bold")
        ax.set_xlabel("Lie-Trotter Steps per Interval ($m$)", fontsize=11)
        ax.set_ylabel("Absolute Simulation Error $\mathcal{E}(m)$", fontsize=11)
        ax.set_xticks(sorted(df["trotter_steps"].unique()))
        ax.legend(frameon=True, fontsize=10)
        plt.tight_layout()

        p1 = figures_dir / "fig1_trotter_noise_tradeoff.png"
        fig.savefig(p1, dpi=300)
        plt.close(fig)
        paths["fig1"] = p1

    # -------------------------------------------------------------
    # Figure 2: Spatial Staggered Magnetization Dynamics vs Time
    # -------------------------------------------------------------
    if "time_dynamics" in benchmark_results:
        df_time = benchmark_results["time_dynamics"]
        fig, ax = plt.subplots(figsize=(9, 5), dpi=300)

        # Exact classical baseline
        df_a = df_time[df_time["processor"] == "demo_processor_A"]
        df_b = df_time[df_time["processor"] == "demo_processor_B"]

        if not df_a.empty:
            ax.plot(
                df_a["time"],
                df_a["exact_m"],
                "k-",
                linewidth=2.5,
                label="Exact Classical Reference (SciPy expm)",
            )
            ax.plot(
                df_a["time"],
                df_a["ideal_m"],
                "b--",
                label="Ideal Trotter Circuit ($m=3$)",
            )
            ax.errorbar(
                df_a["time"],
                df_a["noisy_m"],
                yerr=df_a["error_bar"],
                fmt="o",
                color="#2563eb",
                capsize=3,
                label="Processor A Noisy Simulation (5Q Line)",
            )
        if not df_b.empty:
            ax.errorbar(
                df_b["time"],
                df_b["noisy_m"],
                yerr=df_b["error_bar"],
                fmt="^",
                color="#dc2626",
                capsize=3,
                label="Processor B Noisy Simulation (7Q Heavy-Hex)",
            )

        ax.set_title("Spatial Staggered Magnetization Dynamics $M_{\mathrm{stag}}(t)$", fontsize=13, fontweight="bold")
        ax.set_xlabel("Evolution Time $t$ (seconds, $\hbar=1$)", fontsize=11)
        ax.set_ylabel("Staggered Magnetization $M_{\mathrm{stag}}$", fontsize=11)
        ax.set_ylim(-1.1, 1.1)
        ax.legend(frameon=True, fontsize=9, loc="upper right")
        plt.tight_layout()

        p2 = figures_dir / "fig2_magnetization_dynamics.png"
        fig.savefig(p2, dpi=300)
        plt.close(fig)
        paths["fig2"] = p2

    # -------------------------------------------------------------
    # Figure 3: Circuit Complexity & Hardware Overhead Comparison
    # -------------------------------------------------------------
    if "circuit_metrics" in benchmark_results:
        df_m = benchmark_results["circuit_metrics"]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)

        df_a = df_m[df_m["processor"] == "demo_processor_A"]
        df_b = df_m[df_m["processor"] == "demo_processor_B"]

        steps = sorted(df_m["trotter_steps"].unique())
        x = np.arange(len(steps))
        width = 0.35

        if not df_a.empty and not df_b.empty:
            # Subplot 1: Circuit Depth
            ax1.bar(x - width/2, df_a["depth"], width, label="Proc A (5Q Line)", color="#2563eb")
            ax1.bar(x + width/2, df_b["depth"], width, label="Proc B (7Q Heavy-Hex)", color="#dc2626")
            ax1.set_title("Compiled Circuit Depth vs. Trotter Steps", fontsize=11, fontweight="bold")
            ax1.set_xlabel("Trotter Steps ($m$)")
            ax1.set_ylabel("Circuit Depth")
            ax1.set_xticks(x)
            ax1.set_xticklabels(steps)
            ax1.legend()

            # Subplot 2: Total 2Q Gates & SWAPs
            ax2.bar(x - width/2, df_a["count_2q"], width, label="Proc A 2Q Gates", color="#3b82f6")
            ax2.bar(x + width/2, df_b["count_2q"], width, label="Proc B 2Q Gates", color="#ef4444")
            ax2.set_title("Two-Qubit Gate Count vs. Trotter Steps", fontsize=11, fontweight="bold")
            ax2.set_xlabel("Trotter Steps ($m$)")
            ax2.set_ylabel("Two-Qubit Operations (CNOT/ECR)")
            ax2.set_xticks(x)
            ax2.set_xticklabels(steps)
            ax2.legend()

        plt.tight_layout()
        p3 = figures_dir / "fig3_circuit_overhead.png"
        fig.savefig(p3, dpi=300)
        plt.close(fig)
        paths["fig3"] = p3

    # -------------------------------------------------------------
    # Figure 4: Exploratory Discrete Fourier Power Spectrum
    # -------------------------------------------------------------
    if "time_dynamics" in benchmark_results:
        df_time = benchmark_results["time_dynamics"]
        df_a = df_time[df_time["processor"] == "demo_processor_A"]
        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)

        if not df_a.empty:
            exact_traj = df_a["exact_m"].tolist()
            noisy_traj = df_a["noisy_m"].tolist()

            freqs_ex, p_ex = compute_fourier_spectrum(exact_traj, dt=1.0)
            freqs_no, p_no = compute_fourier_spectrum(noisy_traj, dt=1.0)

            ax.plot(freqs_ex, p_ex, "k-o", label="Exact Classical Spectrum", linewidth=2)
            ax.plot(freqs_no, p_no, "r--s", label="Noisy Simulated Spectrum", linewidth=1.5)

            ax.set_title("Discrete Fourier Power Spectrum $S(f)$ (Exploratory)", fontsize=12, fontweight="bold")
            ax.set_xlabel("Frequency (cycles/sec, $1/s$)")
            ax.set_ylabel("Power Spectral Density")
            ax.legend()

        plt.tight_layout()
        p4 = figures_dir / "fig4_fourier_spectrum.png"
        fig.savefig(p4, dpi=300)
        plt.close(fig)
        paths["fig4"] = p4

    return paths
