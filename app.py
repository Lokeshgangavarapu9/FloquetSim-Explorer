"""
FloquetSim Explorer - Interactive Scientific Web Dashboard
Specification: Master Engineering Specification v1.2, Phase 11
Monolithic Streamlit scientific dashboard backed by decoupled core modules in src/.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.circuits import build_trotter_circuit
from src.classical_solver import simulate_exact_evolution
from src.processors import load_processor, get_processor_status
from src.transpiler import transpile_trotter_circuit
from src.noise import build_noise_model
from src.simulation import simulate_ideal_statevector, simulate_noisy_shots
from src.observables import expectation_from_statevector, expectation_from_counts
from src.metrics import (
    extract_circuit_metrics,
    calculate_trotter_error,
    calculate_noise_error,
    calculate_total_error,
    calculate_shot_uncertainty,
)
from src.experiments import (
    run_trotter_sweep,
    run_time_dynamics_sweep,
    run_full_ab_benchmark,
)


# Page Configuration - White background scientific theme
st.set_page_config(
    page_title="FloquetSim Explorer | Quantum Trotter Benchmark",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for clean, restrained scientific presentation
st.markdown(
    """
    <style>
    .main { background-color: #ffffff; color: #0f172a; }
    .stMetric { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; }
    .status-banner-demo { background-color: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; padding: 10px 14px; color: #991b1b; font-size: 0.9rem; }
    .status-banner-official { background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 6px; padding: 10px 14px; color: #166534; font-size: 0.9rem; }
    h1, h2, h3 { color: #0f172a; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def cached_trotter_sweep(processor_id: str, shots: int, seed: int, fixed_time: float, noise_scale: float):
    return run_trotter_sweep(
        processor_id,
        trotter_steps_list=[1, 2, 3, 4, 5],
        fixed_time=fixed_time,
        shots=shots,
        seed=seed,
        noise_scale=noise_scale,
    )


@st.cache_data
def cached_time_sweep(processor_id: str, shots: int, seed: int, trotter_step: int, noise_scale: float):
    return run_time_dynamics_sweep(
        processor_id,
        time_list=[float(t) for t in range(1, 11)],
        trotter_step=trotter_step,
        shots=shots,
        seed=seed,
        noise_scale=noise_scale,
    )


@st.cache_data
def cached_ab_benchmark(shots: int, seed: int):
    return run_full_ab_benchmark(
        trotter_steps_list=[1, 2, 3, 4, 5],
        time_list=[float(t) for t in range(1, 11)],
        shots=shots,
        seed=seed,
    )


# -------------------------------------------------------------
# SIDEBAR: Experiment Controls & Parameter Selection
# -------------------------------------------------------------
st.sidebar.title("⚛️ Experiment Controls")
st.sidebar.markdown("**Track S3: Noise in Trotter Simulation**")

selected_proc = st.sidebar.selectbox(
    "Target Processor Topology",
    options=["demo_processor_A", "demo_processor_B"],
    format_func=lambda x: "Processor A (5Q Linear Baseline)" if "A" in x else "Processor B (7Q Heavy-Hex Ring)",
    index=0,
)

trotter_m = st.sidebar.slider("Trotter Discretization Steps (m)", min_value=1, max_value=5, value=3, step=1)
evolution_time = st.sidebar.slider("Evolution Time Horizon (seconds)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
sim_mode = st.sidebar.radio("Simulation Mode", options=["noisy_shots", "ideal_statevector", "ideal_shots"], index=0)
shots_count = st.sidebar.selectbox("Measurement Shots", options=[1024, 2048, 4096], index=1)
random_seed = st.sidebar.number_input("Deterministic Seed", min_value=0, max_value=999999, value=42, step=1)

with st.sidebar.expander("Advanced Physical Parameters", expanded=False):
    coupling_J = st.slider("Ising Coupling J (rad/s)", 0.0, 2.0, 1.0, 0.1)
    transverse_hx = st.slider("Transverse Field hx (rad/s)", 0.0, 2.0, 1.0, 0.1)
    longitudinal_hz = st.slider("Longitudinal Field hz (rad/s)", 0.0, 0.5, 0.1, 0.05)
    noise_scaling = st.slider("Noise Multiplier λ", 0.0, 3.0, 1.0, 0.25)


# -------------------------------------------------------------
# TOP BANNER: Title & Hardware Provenance Notice
# -------------------------------------------------------------
st.title("FloquetSim Explorer")
st.caption("SRM University-AP Qiskit Fall Fest 2026 | Quantum Simulation of Transverse-Field Ising Chains")

try:
    config, cmap = load_processor(selected_proc)
    status_info = get_processor_status(config)
except Exception as e:
    st.error(f"Failed to load processor '{selected_proc}': {e}")
    st.stop()

if not status_info["is_official"]:
    st.markdown(
        f"""
        <div class="status-banner-demo">
            <b>[PROVISIONAL DEMONSTRATION TOPOLOGY (NON-OFFICIAL)]</b><br>
            Active hardware configuration: <b>{config.name}</b> ({config.num_qubits} Qubits). 
            Standalone official processor JSON files were not provided in the public competition kit. 
            All simulations employ strictly verified demonstration topologies and synthetic noise channels in Qiskit Aer. Zero claims are made of physical IBM quantum hardware connection.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f"""
        <div class="status-banner-official">
            <b>[OFFICIAL ORGANIZER FIXTURE ACTIVE]</b><br>
            Active hardware: <b>{config.name}</b> certified by hackathon organizers.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# -------------------------------------------------------------
# LIVE CIRCUIT METRICS EXTRACTION (with Graceful Error Handling)
# -------------------------------------------------------------
try:
    qc_logical = build_trotter_circuit(
        num_spins=4,
        trotter_steps=trotter_m,
        total_time=evolution_time,
        J=coupling_J,
        hx=transverse_hx,
        hz=longitudinal_hz,
    )
    qc_transpiled = transpile_trotter_circuit(
        circuit=qc_logical,
        coupling_map=cmap,
        basis_gates=config.basis_gates,
        optimization_level=1,
        seed_transpiler=random_seed,
    )
    circuit_metrics = extract_circuit_metrics(qc_transpiled, config)
except Exception as exc:
    st.error(f"Circuit Compilation Warning: {exc}")
    circuit_metrics = {
        "num_qubits": config.num_qubits,
        "circuit_depth": 0,
        "count_2q_gates": 0,
        "count_swap_gates": 0,
        "estimated_duration_ns": 0.0,
    }

# -------------------------------------------------------------
# TOP METRICS SUMMARY CARDS
# -------------------------------------------------------------
m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
m_col1.metric("Physical Qubits", f"{circuit_metrics['num_qubits']} Q")
m_col2.metric("Circuit Depth", f"{circuit_metrics['circuit_depth']}")
m_col3.metric("Two-Qubit Gates", f"{circuit_metrics['count_2q_gates']} CX")
m_col4.metric("Inserted SWAPs", f"{circuit_metrics['count_swap_gates']}")
m_col5.metric("Est. Duration", f"{circuit_metrics['estimated_duration_ns']:.0f} ns")

st.write("")

# -------------------------------------------------------------
# TABBED PRESENTATION: Full Feature Navigation
# -------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Magnetization Dynamics",
    "⚖️ Trotter-Noise Trade-off",
    "🔀 Processor A/B Comparison",
    "📋 Metrics & CSV Export",
])

with tab1:
    st.subheader("1. Spatial Staggered Magnetization Dynamics")
    st.caption(r"Quench dynamics comparing exact classical solver against Trotterized quantum simulation over time horizon $t \in [1, 10]$ s.")

    try:
        with st.spinner("Calculating time evolution trajectory..."):
            df_time = cached_time_sweep(selected_proc, shots_count, random_seed, trotter_m, noise_scaling)

        fig_time, ax_time = plt.subplots(figsize=(8, 4), dpi=150)
        ax_time.plot(df_time["time"], df_time["exact_m"], "k-", label="Exact Classical (SciPy expm)", linewidth=2)
        ax_time.plot(df_time["time"], df_time["ideal_m"], "b--", label=f"Ideal Trotter (m={trotter_m})")
        ax_time.errorbar(
            df_time["time"],
            df_time["noisy_m"],
            yerr=df_time["error_bar"],
            fmt="o",
            color="#2563eb",
            capsize=3,
            label=f"{config.processor_id} Noisy Aer (λ={noise_scaling:.2f})",
        )
        ax_time.set_xlabel("Time (s)")
        ax_time.set_ylabel(r"Staggered Magnetization $M_{\mathrm{stag}}$")
        ax_time.set_ylim(-1.1, 1.1)
        ax_time.legend(fontsize=9, loc="upper right")
        ax_time.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig_time)
        plt.close(fig_time)
    except Exception as exc:
        st.error(f"Error computing time dynamics: {exc}")
        df_time = pd.DataFrame()

with tab2:
    st.subheader("2. Trotter-Noise Competition & Trade-off")
    st.caption(r"Demonstrating the competition between mathematical Trotter error decay $\mathcal{O}(t^2/m)$ and gate noise accumulation.")

    try:
        with st.spinner("Sweeping Trotter steps m=1..5..."):
            df_trotter = cached_trotter_sweep(selected_proc, shots_count, random_seed, evolution_time, noise_scaling)

        fig_trotter, ax_trotter = plt.subplots(figsize=(8, 4), dpi=150)
        ax_trotter.plot(df_trotter["trotter_steps"], df_trotter["trotter_error"], "k--o", label="Ideal Trotter Error (Discretization)")
        ax_trotter.plot(df_trotter["trotter_steps"], df_trotter["total_error"], "r-s", label="Total Simulation Error (Noisy Aer)", linewidth=2)
        ax_trotter.set_xlabel("Lie-Trotter Steps ($m$)")
        ax_trotter.set_ylabel(r"Absolute Observable Error $|M_{\mathrm{sim}} - M_{\mathrm{exact}}|$")
        ax_trotter.set_xticks([1, 2, 3, 4, 5])
        ax_trotter.legend(fontsize=9)
        ax_trotter.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig_trotter)
        plt.close(fig_trotter)

        # Highlight minimum error operating point
        if not df_trotter.empty and "total_error" in df_trotter.columns:
            min_idx = df_trotter["total_error"].idxmin()
            opt_m = int(df_trotter.loc[min_idx, "trotter_steps"])
            opt_err = df_trotter.loc[min_idx, "total_error"]
            st.info(f"💡 **Empirical Optimal Trotter Step:** $m^* = {opt_m}$ with minimal total error of **{opt_err:.4f}**. Beyond $m^*$, physical gate noise overtakes discretization error reductions.")
    except Exception as exc:
        st.error(f"Error computing Trotter trade-off sweep: {exc}")
        df_trotter = pd.DataFrame()

with tab3:
    st.subheader("3. Architectural Coupling & Routing Comparison")
    st.caption("Head-to-head architectural comparison: 5-Qubit Linear Chain (Processor A) vs 7-Qubit Heavy-Hex Ring (Processor B).")

    st.markdown(
        """
        > **Topological Reality:** Both Processor A and Processor B have a graph distance of $\\text{dist}(0,3) = 3$ hops between boundary spins $q_0$ and $q_3$. 
        > Neither topology natively embeds an induced 4-cycle ($C_4$). Compiling closed boundary periodic conditions requires compiler-inserted SWAP routing on both devices.
        """
    )

    try:
        with st.spinner("Generating comparative A/B benchmark across both processor architectures..."):
            ab_results = cached_ab_benchmark(shots_count, random_seed)
            df_ab_metrics = ab_results["circuit_metrics"]

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            fig_p1, ax_p1 = plt.subplots(figsize=(5.5, 3.5), dpi=130)
            for proc_id, grp in df_ab_metrics.groupby("processor"):
                label = "Proc A (5Q Line)" if "A" in proc_id else "Proc B (7Q Ring)"
                marker = "o-" if "A" in proc_id else "s--"
                ax_p1.plot(grp["trotter_steps"], grp["depth"], marker, label=label)
            ax_p1.set_xlabel("Trotter Steps ($m$)")
            ax_p1.set_ylabel("Transpiled Circuit Depth")
            ax_p1.set_xticks([1, 2, 3, 4, 5])
            ax_p1.legend(fontsize=8)
            ax_p1.grid(True, linestyle="--", alpha=0.5)
            st.pyplot(fig_p1)
            plt.close(fig_p1)

        with col_p2:
            fig_p2, ax_p2 = plt.subplots(figsize=(5.5, 3.5), dpi=130)
            for proc_id, grp in df_ab_metrics.groupby("processor"):
                label = "Proc A (5Q Line)" if "A" in proc_id else "Proc B (7Q Ring)"
                marker = "o-" if "A" in proc_id else "s--"
                ax_p2.plot(grp["trotter_steps"], grp["count_swap"], marker, label=label)
            ax_p2.set_xlabel("Trotter Steps ($m$)")
            ax_p2.set_ylabel("Inserted SWAP Gates")
            ax_p2.set_xticks([1, 2, 3, 4, 5])
            ax_p2.legend(fontsize=8)
            ax_p2.grid(True, linestyle="--", alpha=0.5)
            st.pyplot(fig_p2)
            plt.close(fig_p2)

        st.dataframe(df_ab_metrics, use_container_width=True)
    except Exception as exc:
        st.error(f"Error computing processor comparison: {exc}")
        df_ab_metrics = pd.DataFrame()

with tab4:
    st.subheader("4. Benchmark Data & CSV Export")
    st.caption("Machine-readable benchmark datasets for audit and external plotting.")

    exp_col1, exp_col2, exp_col3 = st.columns(3)

    with exp_col1:
        if not df_trotter.empty:
            csv_trotter = df_trotter.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Trotter Sweep CSV",
                data=csv_trotter,
                file_name="trotter_sweep_results.csv",
                mime="text/csv",
                use_container_width=True,
            )

    with exp_col2:
        if not df_time.empty:
            csv_time = df_time.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Time Dynamics CSV",
                data=csv_time,
                file_name="time_evolution_results.csv",
                mime="text/csv",
                use_container_width=True,
            )

    with exp_col3:
        if "df_ab_metrics" in locals() and not df_ab_metrics.empty:
            csv_ab = df_ab_metrics.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Processor A/B Metrics CSV",
                data=csv_ab,
                file_name="circuit_metrics_comparison.csv",
                mime="text/csv",
                use_container_width=True,
            )

    st.write("")
    if not df_trotter.empty:
        st.markdown("**Active Trotter Sweep Table:**")
        st.dataframe(df_trotter, use_container_width=True)
