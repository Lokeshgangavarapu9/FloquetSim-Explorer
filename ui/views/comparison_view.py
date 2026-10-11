"""
FloquetSim Explorer - Section 06: Experiment Comparison
Specification: Frontend UI Blueprint v1.2 FINAL, Page 7
Side-by-side comparison of two experiment configurations with synchronized charts,
metric deltas, and architectural difference highlighting.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.processors import load_processor
from src.experiments import run_time_dynamics_sweep
from src.circuits import build_trotter_circuit
from src.transpiler import transpile_trotter_circuit
from src.metrics import extract_circuit_metrics


@st.cache_data
def get_run_dynamics(proc_id: str, m_val: int, shots: int, noise_scale: float, seed: int):
    return run_time_dynamics_sweep(
        processor_id=proc_id,
        time_list=[float(t) for t in range(1, 11)],
        trotter_step=m_val,
        shots=shots,
        seed=seed,
        noise_scale=noise_scale,
    )


def render_comparison_view():
    """Render Section 06: Experiment Comparison."""
    st.markdown("## ⚖️ Experiment Comparison")
    st.caption("Compare two experimental runs across processor architectures, noise parameters, and Trotter steps with synchronized observables.")

    # Two side-by-side configuration cards
    col_exp_a, col_exp_b = st.columns(2, gap="large")

    with col_exp_a:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="background-color: #5267F2; color: #FFFFFF; border-radius: 6px; padding: 2px 8px; font-size: 0.8rem; font-weight: 600;">A</span>
                <span style="font-weight: 600; font-size: 1.1rem; color: #172033;">Experiment A</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        proc_a = st.selectbox("Processor A", ["demo_processor_A", "demo_processor_B"], index=0, key="cmp_proc_a")
        m_a = st.slider("Trotter Step m_A", 1, 5, 2, key="cmp_m_a")
        noise_a = st.slider("Noise Multiplier λ_A", 0.0, 3.0, 1.0, 0.25, key="cmp_noise_a")
        shots_a = st.selectbox("Shots A", [1024, 2048, 4096], index=1, key="cmp_shots_a")

    with col_exp_b:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                <span style="background-color: #8B5CF6; color: #FFFFFF; border-radius: 6px; padding: 2px 8px; font-size: 0.8rem; font-weight: 600;">B</span>
                <span style="font-weight: 600; font-size: 1.1rem; color: #172033;">Experiment B</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        proc_b = st.selectbox("Processor B", ["demo_processor_A", "demo_processor_B"], index=1, key="cmp_proc_b")
        m_b = st.slider("Trotter Step m_B", 1, 5, 4, key="cmp_m_b")
        noise_b = st.slider("Noise Multiplier λ_B", 0.0, 3.0, 1.0, 0.25, key="cmp_noise_b")
        shots_b = st.selectbox("Shots B", [1024, 2048, 4096], index=1, key="cmp_shots_b")

    # Mismatch warning if comparing differing physical models
    mismatches = []
    if proc_a != proc_b:
        mismatches.append(f"Processor ({proc_a} vs {proc_b})")
    if m_a != m_b:
        mismatches.append(f"Trotter steps (m={m_a} vs m={m_b})")
    if noise_a != noise_b:
        mismatches.append(f"Noise scale (λ={noise_a} vs λ={noise_b})")

    if mismatches:
        st.info(f"ℹ️ **Parameter variations highlighted:** {', '.join(mismatches)}")

    # Fetch and plot synchronized dynamics
    try:
        with st.spinner("Synchronizing simulation trajectories..."):
            df_a = get_run_dynamics(proc_a, m_a, shots_a, noise_a, 42)
            df_b = get_run_dynamics(proc_b, m_b, shots_b, noise_b, 42)

        fig_cmp = go.Figure()
        # Classical exact ground truth
        fig_cmp.add_trace(go.Scatter(
            x=df_a["time"],
            y=df_a["exact_m"],
            mode="lines",
            name="Exact Classical Reference",
            line=dict(color="#0F172A", width=2, dash="dash"),
        ))
        # Experiment A curve
        label_a = f"Exp A: {proc_a} (m={m_a}, λ={noise_a:.1f})"
        fig_cmp.add_trace(go.Scatter(
            x=df_a["time"],
            y=df_a["noisy_m"],
            error_y=dict(type="data", array=df_a["error_bar"], visible=True),
            mode="lines+markers",
            name=label_a,
            line=dict(color="#5267F2", width=2.5),
            marker=dict(size=7),
        ))
        # Experiment B curve
        label_b = f"Exp B: {proc_b} (m={m_b}, λ={noise_b:.1f})"
        fig_cmp.add_trace(go.Scatter(
            x=df_b["time"],
            y=df_b["noisy_m"],
            error_y=dict(type="data", array=df_b["error_bar"], visible=True),
            mode="lines+markers",
            name=label_b,
            line=dict(color="#8B5CF6", width=2.5),
            marker=dict(size=7),
        ))

        fig_cmp.update_layout(
            title="Synchronized Staggered Magnetization Dynamics",
            xaxis_title="Evolution Time (s)",
            yaxis_title="Staggered Magnetization M_stag",
            yaxis_range=[-1.1, 1.1],
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#F8FAFC",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=20, t=50, b=40),
            height=420,
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

        # Comparative Circuit Compilation Metrics
        st.write("---")
        st.markdown("#### Compilation Overhead Comparison (at t = 5.0 s)")

        config_a, cmap_a = load_processor(proc_a)
        config_b, cmap_b = load_processor(proc_b)

        qc_a = build_trotter_circuit(num_spins=4, trotter_steps=m_a, total_time=5.0)
        t_a = transpile_trotter_circuit(qc_a, coupling_map=cmap_a, basis_gates=config_a.basis_gates, optimization_level=1, seed_transpiler=42)
        met_a = extract_circuit_metrics(t_a, config_a)

        qc_b = build_trotter_circuit(num_spins=4, trotter_steps=m_b, total_time=5.0)
        t_b = transpile_trotter_circuit(qc_b, coupling_map=cmap_b, basis_gates=config_b.basis_gates, optimization_level=1, seed_transpiler=42)
        met_b = extract_circuit_metrics(t_b, config_b)

        c_col1, c_col2, c_col3, c_col4 = st.columns(4)
        c_col1.metric("Transpiled Depth", f"{met_a['circuit_depth']} (A)", delta=f"{met_b['circuit_depth'] - met_a['circuit_depth']} (B-A)", delta_color="inverse")
        c_col2.metric("Two-Qubit Gates", f"{met_a['count_2q_gates']} CX (A)", delta=f"{met_b['count_2q_gates'] - met_a['count_2q_gates']} CX", delta_color="inverse")
        c_col3.metric("Inserted SWAPs", f"{met_a['count_swap_gates']} (A)", delta=f"{met_b['count_swap_gates'] - met_a['count_swap_gates']}", delta_color="inverse")
        c_col4.metric("Est. Duration", f"{met_a['estimated_duration_ns']:.0f} ns", delta=f"{met_b['estimated_duration_ns'] - met_a['estimated_duration_ns']:.0f} ns", delta_color="inverse")

    except Exception as exc:
        st.error(f"Error computing comparison: {exc}")
