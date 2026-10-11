"""
FloquetSim Explorer - Section 06: Experiment Comparison
Specification: Nagrik Scientific Research Interface Design Reference
Side-by-side configuration panels: Experiment A (Cyan theme #00D5E8) and Experiment B (Violet theme #7C4DFF),
synchronized observable plots, and compilation metric deltas.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.processors import load_processor
from src.experiments import run_time_dynamics_sweep
from src.circuits import build_trotter_circuit
from src.transpiler import transpile_trotter_circuit
from src.metrics import extract_circuit_metrics
from ui.theme import (
    apply_plotly_theme,
    COLOR_CANVAS,
    COLOR_SURFACE,
    COLOR_RAISED,
    COLOR_BORDER,
    COLOR_CYAN,
    COLOR_AMBER,
    COLOR_VIOLET,
    COLOR_SUCCESS,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
)


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

    # Two side-by-side configuration cards (Cyan A vs Violet B)
    col_exp_a, col_exp_b = st.columns(2, gap="large")

    with col_exp_a:
        st.markdown(
            f"""
            <div class="scientific-card" style="border-top: 3px solid {COLOR_CYAN};">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="background-color: {COLOR_CYAN}; color: #07090E; border-radius: 4px; padding: 2px 8px; font-size: 0.8rem; font-weight: 700;">A</span>
                    <span style="font-weight: 700; font-size: 1.15rem; color: {COLOR_TEXT_PRIMARY};">Experiment A (Cyan)</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        proc_a = st.selectbox(
            "Processor A",
            ["demo_processor_A", "demo_processor_B"],
            index=0,
            format_func=lambda x: "Demo Processor A (5Q Line)" if "A" in x else "Demo Processor B (7Q Hex-Ring)",
            key="cmp_proc_a",
        )
        m_a = st.slider("Trotter Steps m_A", 1, 5, 2, key="cmp_m_a")
        noise_a = st.slider("Noise Multiplier λ_A", 0.0, 3.0, 1.0, 0.25, key="cmp_noise_a")
        shots_a = st.selectbox("Shots A", [1024, 2048, 4096], index=1, key="cmp_shots_a")

    with col_exp_b:
        st.markdown(
            f"""
            <div class="scientific-card" style="border-top: 3px solid {COLOR_VIOLET};">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="background-color: {COLOR_VIOLET}; color: #FFFFFF; border-radius: 4px; padding: 2px 8px; font-size: 0.8rem; font-weight: 700;">B</span>
                    <span style="font-weight: 700; font-size: 1.15rem; color: {COLOR_TEXT_PRIMARY};">Experiment B (Violet)</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        proc_b = st.selectbox(
            "Processor B",
            ["demo_processor_A", "demo_processor_B"],
            index=1,
            format_func=lambda x: "Demo Processor A (5Q Line)" if "A" in x else "Demo Processor B (7Q Hex-Ring)",
            key="cmp_proc_b",
        )
        m_b = st.slider("Trotter Steps m_B", 1, 5, 4, key="cmp_m_b")
        noise_b = st.slider("Noise Multiplier λ_B", 0.0, 3.0, 1.0, 0.25, key="cmp_noise_b")
        shots_b = st.selectbox("Shots B", [1024, 2048, 4096], index=1, key="cmp_shots_b")

    st.write("")

    # Transpilation Circuit Metrics Delta
    try:
        cfg_a, cmap_a = load_processor(proc_a)
        cfg_b, cmap_b = load_processor(proc_b)

        qc_a = build_trotter_circuit(num_spins=4, trotter_steps=m_a, total_time=5.0, measure=False)
        qc_b = build_trotter_circuit(num_spins=4, trotter_steps=m_b, total_time=5.0, measure=False)

        qc_trans_a = transpile_trotter_circuit(qc_a, cmap_a, cfg_a.basis_gates, 1, 42)
        qc_trans_b = transpile_trotter_circuit(qc_b, cmap_b, cfg_b.basis_gates, 1, 42)

        metrics_a = extract_circuit_metrics(qc_trans_a, cfg_a)
        metrics_b = extract_circuit_metrics(qc_trans_b, cfg_b)

        st.markdown("#### Hardware Compilation Metrics Comparison (at t = 5.0 s)")
        delta_rows = [
            {
                "Circuit Metric": "Transpiled Circuit Depth",
                "Experiment A": metrics_a.depth,
                "Experiment B": metrics_b.depth,
                "Delta (B - A)": f"{metrics_b.depth - metrics_a.depth:+d}",
            },
            {
                "Circuit Metric": "Total Gate Count",
                "Experiment A": metrics_a.total_gates,
                "Experiment B": metrics_b.total_gates,
                "Delta (B - A)": f"{metrics_b.total_gates - metrics_a.total_gates:+d}",
            },
            {
                "Circuit Metric": "Native 2Q CNOT Count",
                "Experiment A": metrics_a.cnot_count,
                "Experiment B": metrics_b.cnot_count,
                "Delta (B - A)": f"{metrics_b.cnot_count - metrics_a.cnot_count:+d}",
            },
            {
                "Circuit Metric": "Transpiler Routing SWAPs",
                "Experiment A": metrics_a.swap_count,
                "Experiment B": metrics_b.swap_count,
                "Delta (B - A)": f"{metrics_b.swap_count - metrics_a.swap_count:+d}",
            },
        ]
        df_deltas = pd.DataFrame(delta_rows)
        st.dataframe(df_deltas, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not compute circuit deltas: {e}")

    st.write("")

    # Synchronized Time Evolution Comparison Chart
    st.markdown("#### Synchronized Time Evolution Comparison ⟨M_stag(t)⟩")
    try:
        df_dyn_a = get_run_dynamics(proc_a, m_a, shots_a, noise_a, 42)
        df_dyn_b = get_run_dynamics(proc_b, m_b, shots_b, noise_b, 42)

        fig_comp = go.Figure()

        # Classical reference (exact is independent of processor)
        fig_comp.add_trace(
            go.Scatter(
                x=df_dyn_a["time"],
                y=df_dyn_a["exact_m"],
                mode="lines",
                line=dict(color=COLOR_TEXT_SECONDARY, width=2, dash="dash"),
                name="Exact Reference Benchmark",
            )
        )

        # Experiment A
        fig_comp.add_trace(
            go.Scatter(
                x=df_dyn_a["time"],
                y=df_dyn_a["noisy_m"],
                mode="lines+markers",
                line=dict(color=COLOR_CYAN, width=2.5),
                marker=dict(size=6),
                name=f"Exp A (m={m_a}, λ={noise_a})",
            )
        )

        # Experiment B
        fig_comp.add_trace(
            go.Scatter(
                x=df_dyn_b["time"],
                y=df_dyn_b["noisy_m"],
                mode="lines+markers",
                line=dict(color=COLOR_VIOLET, width=2.5),
                marker=dict(size=6),
                name=f"Exp B (m={m_b}, λ={noise_b})",
            )
        )

        apply_plotly_theme(fig_comp, height=420, title="Dynamical Trajectory Comparison: Experiment A vs B")
        fig_comp.update_layout(
            xaxis_title="Evolution Time t (seconds)",
            yaxis_title="Staggered Magnetization ⟨M_stag⟩",
            yaxis=dict(range=[-1.05, 1.05]),
        )
        st.plotly_chart(fig_comp, use_container_width=True)
    except Exception as e:
        st.error(f"Error computing comparative time dynamics: {e}")
