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
from src.metrics import extract_circuit_metrics, calculate_trotter_error, calculate_noise_error, calculate_total_error, calculate_shot_uncertainty
from src.experiments import run_trotter_sweep, run_time_dynamics_sweep


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
def cached_trotter_sweep(processor_id: str, shots: int, seed: int, fixed_time: float):
    return run_trotter_sweep(processor_id, trotter_steps_list=[1, 2, 3, 4, 5], fixed_time=fixed_time, shots=shots, seed=seed)


@st.cache_data
def cached_time_sweep(processor_id: str, shots: int, seed: int, trotter_step: int):
    return run_time_dynamics_sweep(processor_id, time_list=[float(t) for t in range(1, 11)], trotter_step=trotter_step, shots=shots, seed=seed)


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

config, cmap = load_processor(selected_proc)
status_info = get_processor_status(config)

if not status_info["is_official"]:
    st.markdown(
        f"""
        <div class="status-banner-demo">
            <b>[PROVISIONAL DEMONSTRATION TOPOLOGY (NON-OFFICIAL)]</b><br>
            Active hardware: <b>{config.name}</b> ({config.num_qubits} Qubits). 
            Standalone official files were not provided in the public kit. 
            All simulations employ strictly verified demonstration topologies and synthetic noise models. Zero claims of physical IBM hardware calibration.
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
# MAIN DASHBOARD BODY: Reactive Live Quantum Simulation
# -------------------------------------------------------------
col1, col2 = st.columns([1, 1])

# Run Single Circuit Compilation for Live Metrics
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

with col1:
    st.subheader("1. Spatial Staggered Magnetization Dynamics")
    st.caption("Quench dynamics comparing exact classical solver against quantum execution over time.")
    
    with st.spinner("Calculating time evolution trajectory..."):
        df_time = cached_time_sweep(selected_proc, shots_count, random_seed, trotter_m)

    fig_time, ax_time = plt.subplots(figsize=(6.5, 3.8), dpi=150)
    ax_time.plot(df_time["time"], df_time["exact_m"], "k-", label="Exact Classical (SciPy expm)", linewidth=2)
    ax_time.plot(df_time["time"], df_time["ideal_m"], "b--", label=f"Ideal Trotter (m={trotter_m})")
    ax_time.errorbar(
        df_time["time"],
        df_time["noisy_m"],
        yerr=df_time["error_bar"],
        fmt="o",
        color="#2563eb",
        capsize=3,
        label=f"{config.processor_id} Noisy Aer",
    )
    ax_time.set_xlabel("Time (s)")
    ax_time.set_ylabel("Staggered Magnetization $M_{\mathrm{stag}}$")
    ax_time.set_ylim(-1.1, 1.1)
    ax_time.legend(fontsize=8, loc="upper right")
    ax_time.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig_time)
    plt.close(fig_time)

with col2:
    st.subheader("2. Trotter-Noise Competition & Trade-off")
    st.caption("Evaluating algorithmic discretization error decay against noise-induced error growth.")
    
    with st.spinner("Sweeping Trotter steps m=1..5..."):
        df_trotter = cached_trotter_sweep(selected_proc, shots_count, random_seed, evolution_time)

    fig_trotter, ax_trotter = plt.subplots(figsize=(6.5, 3.8), dpi=150)
    ax_trotter.plot(df_trotter["trotter_steps"], df_trotter["trotter_error"], "k--o", label="Ideal Trotter Error")
    ax_trotter.plot(df_trotter["trotter_steps"], df_trotter["total_error"], "r-s", label="Total Noisy Error", linewidth=2)
    ax_trotter.set_xlabel("Lie-Trotter Steps ($m$)")
    ax_trotter.set_ylabel("Absolute Observable Error")
    ax_trotter.set_xticks([1, 2, 3, 4, 5])
    ax_trotter.legend(fontsize=8)
    ax_trotter.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig_trotter)
    plt.close(fig_trotter)


# -------------------------------------------------------------
# BOTTOM ZONE: Hardware Metrics Cards & CSV Data Export
# -------------------------------------------------------------
st.subheader("3. Hardware & Compilation Metrics")

m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
m_col1.metric("Physical Qubits", f"{circuit_metrics['num_qubits']} Q")
m_col2.metric("Circuit Depth", f"{circuit_metrics['circuit_depth']}")
m_col3.metric("Two-Qubit Gates", f"{circuit_metrics['count_2q_gates']} CX")
m_col4.metric("Inserted SWAPs", f"{circuit_metrics['count_swap_gates']}")
m_col5.metric("Est. Gate Time", f"{circuit_metrics['estimated_duration_ns']:.0f} ns")

st.write("")
exp_col1, exp_col2 = st.columns([1, 1])

with exp_col1:
    csv_trotter = df_trotter.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Trotter Sweep CSV",
        data=csv_trotter,
        file_name="trotter_sweep_results.csv",
        mime="text/csv",
    )

with exp_col2:
    csv_time = df_time.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Time Dynamics CSV",
        data=csv_time,
        file_name="time_evolution_results.csv",
        mime="text/csv",
    )
