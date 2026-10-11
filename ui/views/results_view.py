"""
FloquetSim Explorer - Section 04: Scientific Results
Specification: Nagrik Scientific Research Interface Design Reference
Comprehensive quantum benchmark results: Spatiotemporal Heatmap & 3D Surface,
Lie-Trotter error breakdown, noise sensitivity, and processor compilation overhead.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
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
    COLOR_ERROR,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
)
from src.experiments import run_trotter_sweep, run_time_dynamics_sweep


@st.cache_data
def get_cached_time_dynamics(proc_id: str, m_val: int, shots: int, noise_scale: float):
    """Retrieve or compute time evolution sweep with site-resolved columns."""
    t_list = [float(t) / 10.0 for t in range(1, 40)]  # 0.1 to 3.9 s (39 steps)
    return run_time_dynamics_sweep(
        processor_id=proc_id,
        time_list=t_list,
        trotter_step=m_val,
        shots=shots,
        seed=42,
        noise_scale=noise_scale,
    )


@st.cache_data
def get_cached_trotter_sweep(proc_id: str, t_fixed: float, shots: int, noise_scale: float):
    """Retrieve or compute Trotter step sweep m in [1..5]."""
    return run_trotter_sweep(
        processor_id=proc_id,
        trotter_steps_list=[1, 2, 3, 4, 5],
        fixed_time=t_fixed,
        shots=shots,
        seed=42,
        noise_scale=noise_scale,
    )


def render_results_view():
    """Render Section 04: Scientific Results."""
    st.markdown("## 📊 Scientific Results & Benchmark Visualizations")
    st.caption("Inspect rigorous numerical observables, spatiotemporal wave heatmaps, Trotter error trade-offs, and hardware routing overhead.")

    # Top Control Bar
    bar_c1, bar_c2, bar_c3, bar_c4 = st.columns([1.5, 1.2, 1.2, 1.2], gap="medium")
    with bar_c1:
        proc_options = ["demo_processor_A", "demo_processor_B"]
        default_idx = 0 if st.session_state.get("selected_processor_id", "A") == "demo_processor_A" else 1
        proc_id = st.selectbox(
            "Processor Architecture",
            options=proc_options,
            index=default_idx,
            format_func=lambda x: "Demo Processor A (5Q Line)" if "A" in x else "Demo Processor B (7Q Hex-Ring)",
            key="res_proc_select",
        )
        st.session_state["selected_processor_id"] = proc_id

    with bar_c2:
        m_step = st.slider("Trotter Step m", 1, 5, 3, key="res_m_step")

    with bar_c3:
        noise_scale = st.slider("Noise Multiplier λ", 0.0, 3.0, 1.0, 0.25, key="res_noise_scale")

    with bar_c4:
        shots = st.selectbox("Shots", [1024, 2048, 4096], index=1, key="res_shots")

    # The 5 Result Tabs
    tab_dyn, tab_trot, tab_noise, tab_over, tab_tables = st.tabs([
        "🌊 Magnetization Dynamics",
        "📉 Lie-Trotter Error Analysis",
        "⚡ Noise Sensitivity Profile",
        "🏛️ Compilation Overhead",
        "📋 Numerical Data Tables",
    ])

    # -------------------------------------------------------------
    # TAB 1: MAGNETIZATION DYNAMICS
    # -------------------------------------------------------------
    with tab_dyn:
        st.markdown("#### Spatiotemporal Spin Dynamics & Magnetization Trajectories")
        df_dyn = get_cached_time_dynamics(proc_id, m_step, shots, noise_scale)

        display_c1, display_c2 = st.columns([1.2, 2.8])
        with display_c1:
            plot_type = st.radio(
                "Visualization Type",
                options=["2D Line Dynamics", "Spatiotemporal Heatmap", "3D Wave Surface"],
                index=0,
                key="res_plot_type",
            )

        if plot_type == "2D Line Dynamics":
            with display_c2:
                disp_mode = st.radio(
                    "Display Metric",
                    options=["Global Staggered ⟨M_stag⟩", "Site-Resolved ⟨Z_j⟩ (Q0..Q3)", "Composite All"],
                    index=0,
                    horizontal=True,
                    key="res_disp_mode",
                )

            fig_dyn = go.Figure()

            if disp_mode == "Global Staggered ⟨M_stag⟩" or disp_mode == "Composite All":
                fig_dyn.add_trace(
                    go.Scatter(
                        x=df_dyn["time"],
                        y=df_dyn["exact_m"],
                        mode="lines",
                        line=dict(color=COLOR_TEXT_SECONDARY, width=2.5, dash="dash"),
                        name="Exact Classical",
                    )
                )
                fig_dyn.add_trace(
                    go.Scatter(
                        x=df_dyn["time"],
                        y=df_dyn["ideal_m"],
                        mode="lines+markers",
                        line=dict(color=COLOR_CYAN, width=2),
                        marker=dict(size=4),
                        name="Ideal Trotter",
                    )
                )
                fig_dyn.add_trace(
                    go.Scatter(
                        x=df_dyn["time"],
                        y=df_dyn["noisy_m"],
                        mode="lines+markers",
                        line=dict(color=COLOR_AMBER, width=2),
                        marker=dict(size=4),
                        error_y=dict(
                            type="data",
                            array=df_dyn["error_bar"] if "error_bar" in df_dyn.columns else None,
                            visible=True if "error_bar" in df_dyn.columns else False,
                            color="rgba(255, 179, 0, 0.35)",
                        ),
                        name="Noisy Aer Shots",
                    )
                )

            if disp_mode == "Site-Resolved ⟨Z_j⟩ (Q0..Q3)" or disp_mode == "Composite All":
                colors_sites = [COLOR_CYAN, COLOR_AMBER, COLOR_VIOLET, COLOR_SUCCESS]
                for q_idx in range(4):
                    col_key = f"noisy_z_{q_idx}"
                    if col_key in df_dyn.columns:
                        fig_dyn.add_trace(
                            go.Scatter(
                                x=df_dyn["time"],
                                y=df_dyn[col_key],
                                mode="lines",
                                line=dict(color=colors_sites[q_idx], width=1.8),
                                name=f"Q{q_idx} ⟨Z_{q_idx}⟩",
                            )
                        )

            apply_plotly_theme(fig_dyn, height=440, title="Non-Equilibrium Spin Dynamics ⟨M(t)⟩")
            fig_dyn.update_layout(
                xaxis_title="Evolution Time t (seconds)",
                yaxis_title="Magnetization Expectation",
                yaxis=dict(range=[-1.05, 1.05]),
            )
            st.plotly_chart(fig_dyn, use_container_width=True)

        elif plot_type == "Spatiotemporal Heatmap":
            # Site-Resolved Heatmap: X = time, Y = spin site index, Z = local magnetization
            z_matrix = []
            for q_idx in range(4):
                col_key = f"exact_z_{q_idx}"
                if col_key in df_dyn.columns:
                    z_matrix.append(df_dyn[col_key].values)
                else:
                    z_matrix.append(np.zeros(len(df_dyn)))

            fig_hm = go.Figure(
                data=go.Heatmap(
                    z=z_matrix,
                    x=df_dyn["time"].values,
                    y=["Site Q0", "Site Q1", "Site Q2", "Site Q3"],
                    colorscale="Tealrose",
                    zmin=-1.0,
                    zmax=1.0,
                    colorbar=dict(
                        title="Polarization ⟨Z_j⟩",
                        titlefont=dict(color=COLOR_TEXT_PRIMARY, size=11),
                        tickfont=dict(color=COLOR_TEXT_SECONDARY, size=10),
                    ),
                    hovertemplate="Time: %{x:.2f} s<br>Spin Site: %{y}<br>⟨Z_j⟩: %{z:+.3f}<extra></extra>",
                )
            )
            apply_plotly_theme(fig_hm, height=360, title="Spatiotemporal Spin Polarization Heatmap ⟨Z(j, t)⟩")
            fig_hm.update_layout(
                xaxis_title="Evolution Time t (seconds)",
                yaxis_title="Lattice Site",
            )
            st.plotly_chart(fig_hm, use_container_width=True)

        elif plot_type == "3D Wave Surface":
            # 3D Spatiotemporal Wave Surface: X = time, Y = spin site index, Z = local magnetization
            z_matrix = []
            for q_idx in range(4):
                col_key = f"exact_z_{q_idx}"
                if col_key in df_dyn.columns:
                    z_matrix.append(df_dyn[col_key].values)
                else:
                    z_matrix.append(np.zeros(len(df_dyn)))

            z_surface = np.array(z_matrix)
            x_times = df_dyn["time"].values
            y_sites = np.array([0, 1, 2, 3])

            fig_surf = go.Figure(
                data=[
                    go.Surface(
                        z=z_surface,
                        x=x_times,
                        y=y_sites,
                        colorscale="Tealrose",
                        cmin=-1.0,
                        cmax=1.0,
                        contours=dict(
                            z=dict(
                                show=True,
                                usecolormap=True,
                                highlightcolor="#00D5E8",
                                project=dict(z=True),
                            )
                        ),
                        colorbar=dict(
                            title="⟨Z_j⟩",
                            titlefont=dict(color=COLOR_TEXT_PRIMARY, size=11),
                            tickfont=dict(color=COLOR_TEXT_SECONDARY, size=10),
                        ),
                        hovertemplate="Time: %{x:.2f} s<br>Site: Q%{y}<br>⟨Z_j⟩: %{z:+.3f}<extra></extra>",
                    )
                ]
            )
            fig_surf.update_layout(
                paper_bgcolor=COLOR_CANVAS,
                scene=dict(
                    bgcolor=COLOR_CANVAS,
                    xaxis=dict(
                        title="Time t (s)",
                        gridcolor=COLOR_BORDER,
                        tickfont=dict(color=COLOR_TEXT_SECONDARY, size=9),
                        titlefont=dict(color=COLOR_TEXT_PRIMARY, size=11),
                    ),
                    yaxis=dict(
                        title="Qubit Site j",
                        gridcolor=COLOR_BORDER,
                        tickvals=[0, 1, 2, 3],
                        ticktext=["Q0", "Q1", "Q2", "Q3"],
                        tickfont=dict(color=COLOR_TEXT_SECONDARY, size=9),
                        titlefont=dict(color=COLOR_TEXT_PRIMARY, size=11),
                    ),
                    zaxis=dict(
                        title="Polarization ⟨Z_j⟩",
                        gridcolor=COLOR_BORDER,
                        range=[-1.05, 1.05],
                        tickfont=dict(color=COLOR_TEXT_SECONDARY, size=9),
                        titlefont=dict(color=COLOR_TEXT_PRIMARY, size=11),
                    ),
                    camera=dict(eye=dict(x=1.75, y=-1.5, z=1.1)),
                ),
                margin=dict(l=0, r=0, t=20, b=0),
                height=460,
            )
            st.plotly_chart(fig_surf, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 2: LIE-TROTTER ERROR ANALYSIS
    # -------------------------------------------------------------
    with tab_trot:
        st.markdown("#### Lie-Trotter Discretization vs Hardware Noise Accumulation")
        df_trot = get_cached_trotter_sweep(proc_id, 5.0, shots, noise_scale)

        # Robust column resolution
        col_tot = "total_error" if "total_error" in df_trot.columns else "error_total"
        col_trot = "trotter_error" if "trotter_error" in df_trot.columns else "error_trotter"
        col_noise = "noise_error" if "noise_error" in df_trot.columns else "error_noise"

        best_m = int(df_trot.loc[df_trot[col_tot].idxmin()]["trotter_steps"])
        min_err = float(df_trot[col_tot].min())

        st.markdown(
            f"""
            <div class="banner-official">
                <b>Optimal Step Count Identified:</b> Minimal total error occurs at <b>m* = {best_m}</b> (Total error ϵ = <b>{min_err:.4f}</b>).<br>
                For m &lt; {best_m}, algorithmic truncation error dominates: ϵ ~ O(t²/m). For m &gt; {best_m}, accumulated two-qubit gate noise dominates.
            </div>
            """,
            unsafe_allow_html=True,
        )

        fig_err = go.Figure()

        # Algorithmic error curve
        fig_err.add_trace(
            go.Scatter(
                x=df_trot["trotter_steps"],
                y=df_trot[col_trot],
                mode="lines+markers",
                line=dict(color=COLOR_CYAN, width=2.5),
                marker=dict(size=6),
                name="Algorithmic Trotter Error",
            )
        )

        # Accumulated noise error curve
        fig_err.add_trace(
            go.Scatter(
                x=df_trot["trotter_steps"],
                y=df_trot[col_noise],
                mode="lines+markers",
                line=dict(color=COLOR_AMBER, width=2.5),
                marker=dict(size=6),
                name="Accumulated Gate Noise Error",
            )
        )

        # Total combined error
        fig_err.add_trace(
            go.Scatter(
                x=df_trot["trotter_steps"],
                y=df_trot[col_tot],
                mode="lines+markers",
                line=dict(color=COLOR_VIOLET, width=3, dash="dot"),
                marker=dict(size=8),
                name="Total Empirical Error ϵ",
            )
        )

        # Optimal callout marker
        fig_err.add_trace(
            go.Scatter(
                x=[best_m],
                y=[min_err],
                mode="markers+text",
                marker=dict(color="#10B981", size=14, symbol="star"),
                text=[f"Optimal m*={best_m}"],
                textposition="top center",
                textfont=dict(color="#10B981", size=12, family="JetBrains Mono, monospace"),
                name="Optimal m*",
                showlegend=False,
            )
        )

        apply_plotly_theme(fig_err, height=420, title="Trotter Error Competition Trade-Off Curve")
        fig_err.update_layout(
            xaxis_title="Trotter Steps m",
            yaxis_title="Absolute Error |ΔM|",
            xaxis=dict(dtick=1),
        )
        st.plotly_chart(fig_err, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 3: NOISE SENSITIVITY PROFILE
    # -------------------------------------------------------------
    with tab_noise:
        st.markdown("#### Hardware Noise Sensitivity & Error Scaling")
        st.caption("Quantifies fidelity degradation across noise scale multipliers λ ∈ [0.0, 3.0].")

        noise_scales = [0.0, 0.5, 1.0, 1.5, 2.0]
        noise_rows = []
        for n_s in noise_scales:
            df_n = get_cached_trotter_sweep(proc_id, 5.0, shots, n_s)
            c_tot = "total_error" if "total_error" in df_n.columns else "error_total"
            c_noise = "noise_error" if "noise_error" in df_n.columns else "error_noise"
            row_best = df_n.loc[df_n["trotter_steps"] == m_step].iloc[0]
            noise_rows.append({
                "noise_scale": n_s,
                "error_total": row_best[c_tot],
                "error_noise": row_best[c_noise],
            })
        df_noise_scan = pd.DataFrame(noise_rows)

        fig_noise = go.Figure()
        fig_noise.add_trace(
            go.Scatter(
                x=df_noise_scan["noise_scale"],
                y=df_noise_scan["error_total"],
                mode="lines+markers",
                line=dict(color=COLOR_CYAN, width=2.5),
                marker=dict(size=7),
                name=f"Total Error at m={m_step}",
            )
        )
        fig_noise.add_trace(
            go.Scatter(
                x=df_noise_scan["noise_scale"],
                y=df_noise_scan["error_noise"],
                mode="lines+markers",
                line=dict(color=COLOR_AMBER, width=2),
                marker=dict(size=7),
                name=f"Noise Contribution at m={m_step}",
            )
        )
        apply_plotly_theme(fig_noise, height=380, title="Noise Sensitivity Profile vs Multiplier λ")
        fig_noise.update_layout(
            xaxis_title="Noise Scale Factor λ (0 = Ideal, 1 = Baseline)",
            yaxis_title="Error Magnitude",
        )
        st.plotly_chart(fig_noise, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 4: COMPILATION OVERHEAD
    # -------------------------------------------------------------
    with tab_over:
        st.markdown("#### Hardware Routing & SWAP Gate Overhead")
        st.caption("Comparison of native 2Q CNOT gates vs transpiler-inserted routing SWAP gates across architectures.")

        df_trot_a = get_cached_trotter_sweep("demo_processor_A", 5.0, shots, noise_scale)
        df_trot_b = get_cached_trotter_sweep("demo_processor_B", 5.0, shots, noise_scale)

        m_idx = m_step
        row_a = df_trot_a.loc[df_trot_a["trotter_steps"] == m_idx].iloc[0]
        row_b = df_trot_b.loc[df_trot_b["trotter_steps"] == m_idx].iloc[0]

        cnot_a = row_a["count_2q"] if "count_2q" in row_a else row_a.get("cnot_count", 0)
        swap_a = row_a["count_swap"] if "count_swap" in row_a else row_a.get("swap_count", 0)
        cnot_b = row_b["count_2q"] if "count_2q" in row_b else row_b.get("cnot_count", 0)
        swap_b = row_b["count_swap"] if "count_swap" in row_b else row_b.get("swap_count", 0)

        fig_bar = go.Figure()
        fig_bar.add_trace(
            go.Bar(
                name="Native Interaction CNOTs",
                x=["Processor A (5Q Line)", "Processor B (7Q Hex)"],
                y=[max(0, cnot_a - 3 * swap_a), max(0, cnot_b - 3 * swap_b)],
                marker_color=COLOR_CYAN,
            )
        )
        fig_bar.add_trace(
            go.Bar(
                name="Routing SWAP Gates (×3 CNOTs)",
                x=["Processor A (5Q Line)", "Processor B (7Q Hex)"],
                y=[3 * swap_a, 3 * swap_b],
                marker_color=COLOR_AMBER,
            )
        )
        apply_plotly_theme(fig_bar, height=380, title=f"2Q Gate Decomposition at m = {m_step}")
        fig_bar.update_layout(
            barmode="stack",
            yaxis_title="Total 2Q CNOT Count",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 5: NUMERICAL DATA TABLES & CSV EXPORT
    # -------------------------------------------------------------
    with tab_tables:
        st.markdown("#### Tabular Numerical Results & CSV Export")
        st.markdown("##### 1. Trotter Discretization Sweep (m = 1..5)")
        st.dataframe(df_trot, use_container_width=True)
        csv_trot = df_trot.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download trotter_sweep_results.csv",
            data=csv_trot,
            file_name="trotter_sweep_results.csv",
            mime="text/csv",
            key="dl_trot_csv",
        )

        st.markdown("##### 2. Time Evolution Trajectory Dataset")
        st.dataframe(df_dyn.head(15), use_container_width=True)
        csv_dyn = df_dyn.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download time_dynamics_results.csv",
            data=csv_dyn,
            file_name="time_dynamics_results.csv",
            mime="text/csv",
            key="dl_dyn_csv",
        )
