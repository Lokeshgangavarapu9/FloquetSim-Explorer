"""
FloquetSim Explorer - Section 04: Scientific Results
Specification: Frontend UI Blueprint v1.2 FINAL, Page 5
Present computed physics results in clear plots with tabs for Magnetization Dynamics (2D & 3D),
Trotter Convergence, Noise Analysis, Processor Comparison, and Numerical Results.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.processors import load_processor
from src.experiments import run_trotter_sweep, run_time_dynamics_sweep, run_full_ab_benchmark
from src.classical_solver import simulate_exact_evolution


@st.cache_data
def get_cached_time_data(proc_id: str, shots: int, seed: int, m: int, noise_scale: float):
    return run_time_dynamics_sweep(
        processor_id=proc_id,
        time_list=[float(t) for t in range(1, 11)],
        trotter_step=m,
        shots=shots,
        seed=seed,
        noise_scale=noise_scale,
    )


@st.cache_data
def get_cached_trotter_data(proc_id: str, shots: int, seed: int, t_val: float, noise_scale: float):
    return run_trotter_sweep(
        processor_id=proc_id,
        trotter_steps_list=[1, 2, 3, 4, 5],
        fixed_time=t_val,
        shots=shots,
        seed=seed,
        noise_scale=noise_scale,
    )


def render_results_view():
    """Render Section 04: Scientific Results."""
    st.markdown("## 📊 Scientific Results")
    st.caption("Quantitative exploration of non-equilibrium quench dynamics, Lie-Trotter convergence, and architectural noise scaling.")

    # Global filter bar
    filt_col1, filt_col2, filt_col3, filt_col4 = st.columns(4)
    with filt_col1:
        res_proc = st.selectbox(
            "Target Processor",
            options=["demo_processor_A", "demo_processor_B"],
            format_func=lambda x: "Proc A (5Q Line)" if "A" in x else "Proc B (7Q Ring)",
            key="res_proc_select",
        )
    with filt_col2:
        res_m = st.selectbox("Trotter Step (m)", options=[1, 2, 3, 4, 5], index=2, key="res_m_select")
    with filt_col3:
        res_shots = st.selectbox("Shots", options=[1024, 2048, 4096], index=1, key="res_shots_select")
    with filt_col4:
        res_noise = st.slider("Noise Multiplier λ", 0.0, 3.0, 1.0, 0.25, key="res_noise_slider")

    # Fetch active data
    try:
        df_time = get_cached_time_data(res_proc, res_shots, 42, res_m, res_noise)
        df_trotter = get_cached_trotter_data(res_proc, res_shots, 42, 5.0, res_noise)
    except Exception as exc:
        st.error(f"Error computing results: {exc}")
        return

    # Tabs (Blueprint Page 5)
    tab_dyn, tab_trotter, tab_noise, tab_proc, tab_num = st.tabs([
        "📈 Magnetization Dynamics",
        "⚖️ Trotter Comparison",
        "📉 Noise Analysis",
        "🔀 Processor Comparison",
        "📋 Numerical Tables & Export",
    ])

    with tab_dyn:
        col_2d, col_3d = st.columns([1.1, 0.9], gap="large")

        with col_2d:
            st.markdown("#### Staggered Magnetization (2D Time-Series)")
            fig_2d = go.Figure()
            fig_2d.add_trace(go.Scatter(
                x=df_time["time"],
                y=df_time["exact_m"],
                mode="lines",
                name="Exact Classical (SciPy expm)",
                line=dict(color="#1E293B", width=2.5),
            ))
            fig_2d.add_trace(go.Scatter(
                x=df_time["time"],
                y=df_time["ideal_m"],
                mode="lines+markers",
                name=f"Ideal Trotter (m={res_m})",
                line=dict(color="#5267F2", dash="dash", width=2),
                marker=dict(size=6),
            ))
            fig_2d.add_trace(go.Scatter(
                x=df_time["time"],
                y=df_time["noisy_m"],
                error_y=dict(type="data", array=df_time["error_bar"], visible=True),
                mode="markers",
                name=f"Noisy Aer (λ={res_noise:.2f})",
                marker=dict(color="#29B6D8", size=8),
            ))
            fig_2d.update_layout(
                xaxis_title="Evolution Time (s)",
                yaxis_title="Staggered Magnetization M_stag",
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#F8FAFC",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=40, r=20, t=30, b=40),
                height=380,
            )
            st.plotly_chart(fig_2d, use_container_width=True)

        with col_3d:
            st.markdown("#### 3D Spatiotemporal Magnetization Surface")
            # Compute exact local site magnetizations across all time points
            try:
                time_pts = list(range(1, 11))
                exact_all = simulate_exact_evolution(num_spins=4, time_points=[float(t) for t in time_pts])
                local_z_matrix = np.array(exact_all["local_z"])  # shape: (10, 4)

                fig_surf = go.Figure(data=[
                    go.Surface(
                        z=local_z_matrix,
                        x=[0, 1, 2, 3],  # Qubit sites
                        y=time_pts,      # Time points
                        colorscale="Viridis",
                        colorbar=dict(title="⟨Z_j⟩", len=0.7),
                    )
                ])
                fig_surf.update_layout(
                    scene=dict(
                        xaxis_title="Qubit Site (j)",
                        yaxis_title="Time (s)",
                        zaxis_title="⟨Z_j⟩",
                        bgcolor="#FFFFFF",
                    ),
                    paper_bgcolor="#FFFFFF",
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=380,
                )
                st.plotly_chart(fig_surf, use_container_width=True)
            except Exception as e:
                st.info(f"3D Surface unavailable: {e}")

        st.markdown(
            """
            <div class="scientific-card-alt">
                <b>Key Physical Insights:</b><br>
                • Staggered magnetization exhibits non-equilibrium coherent oscillation under transverse field quench (hx = 1.0 rad/s).<br>
                • Trotter discretization introduces algorithmic phase error bounded by BCH scaling O(t²/m).<br>
                • Finite shot statistics (N_shots = %d) produce observable variance σ_M = √(1 - M²)/√N_shots.
            </div>
            """ % res_shots,
            unsafe_allow_html=True,
        )

    with tab_trotter:
        st.markdown("#### Lie-Trotter Error Convergence & Noise Trade-off")
        fig_tr = go.Figure()
        fig_tr.add_trace(go.Scatter(
            x=df_trotter["trotter_steps"],
            y=df_trotter["trotter_error"],
            mode="lines+markers",
            name="Ideal Discretization Error (|M_ideal - M_exact|)",
            line=dict(color="#1E293B", dash="dash"),
            marker=dict(symbol="circle", size=8),
        ))
        fig_tr.add_trace(go.Scatter(
            x=df_trotter["trotter_steps"],
            y=df_trotter["total_error"],
            mode="lines+markers",
            name="Total Noisy Simulation Error (|M_noisy - M_exact|)",
            line=dict(color="#EF4444", width=2.5),
            marker=dict(symbol="square", size=8),
        ))
        fig_tr.update_layout(
            xaxis=dict(title="Trotter Discretization Steps (m)", tickvals=[1, 2, 3, 4, 5]),
            yaxis_title="Absolute Observable Error",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#F8FAFC",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=20, t=30, b=40),
            height=380,
        )
        st.plotly_chart(fig_tr, use_container_width=True)

        if not df_trotter.empty and "total_error" in df_trotter.columns:
            opt_idx = df_trotter["total_error"].idxmin()
            m_opt = int(df_trotter.loc[opt_idx, "trotter_steps"])
            err_opt = df_trotter.loc[opt_idx, "total_error"]
            st.info(
                f"🏆 **Optimal Operating Point:** $m^* = {m_opt}$ minimizes total error to **{err_opt:.4f}**. "
                f"Beyond $m^*$, circuit depth increases two-qubit gate decoherence faster than Trotter error decays."
            )

    with tab_noise:
        st.markdown("#### Synthetic Hardware Noise Model Characterization")
        st.caption("Configured error rates from the competition starter guide. Note: All simulations use synthetic channels; zero physical IBM hardware is connected.")

        n_col1, n_col2, n_col3 = st.columns(3)
        n_col1.metric("1Q Gate Error (p1)", f"{0.001 * res_noise:.4f}")
        n_col2.metric("2Q Gate Error (p2)", f"{0.010 * res_noise:.4f}")
        n_col3.metric("Readout Error [e01, e10]", f"[{0.01*res_noise:.3f}, {0.02*res_noise:.3f}]")

        st.markdown(
            """
            <div class="scientific-card">
                <b>Noise Channel Mechanics:</b><br>
                1. <b>Single-Qubit Depolarizing:</b> Applied to basis gates <code>x, sx</code> with error rate <code>p1 = 0.001 × λ</code>.<br>
                2. <b>Two-Qubit Depolarizing:</b> Applied to entangling gate <code>cx</code> with error rate <code>p2 = 0.010 × λ</code>.<br>
                3. <b>Readout Assignment Matrix:</b> Row-stochastic confusion matrix <code>[[1 - p10, p10], [p01, 1 - p01]]</code> where row sums strictly equal 1.0 within numerical precision.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab_proc:
        st.markdown("#### Comparative Architectural Benchmark (Processor A vs B)")
        try:
            ab_res = run_full_ab_benchmark(shots=res_shots, seed=42)
            df_ab = ab_res["circuit_metrics"]

            fig_cmp = go.Figure()
            for proc, grp in df_ab.groupby("processor"):
                label = "Proc A (5Q Line)" if "A" in proc else "Proc B (7Q Ring)"
                color = "#5267F2" if "A" in proc else "#8B5CF6"
                fig_cmp.add_trace(go.Scatter(
                    x=grp["trotter_steps"],
                    y=grp["depth"],
                    mode="lines+markers",
                    name=f"{label} - Depth",
                    line=dict(color=color),
                ))
            fig_cmp.update_layout(
                xaxis=dict(title="Trotter Steps (m)", tickvals=[1, 2, 3, 4, 5]),
                yaxis_title="Transpiled Circuit Depth",
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#F8FAFC",
                height=350,
            )
            st.plotly_chart(fig_cmp, use_container_width=True)
        except Exception as e:
            st.info(f"Processor comparison unavailable: {e}")

    with tab_num:
        st.markdown("#### Tabular Outputs & Machine-Readable Data")
        try:
            st.dataframe(df_trotter, use_container_width=True)
        except Exception:
            st.table(df_trotter)

        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.download_button(
                "📥 Download Trotter Results CSV",
                data=df_trotter.to_csv(index=False).encode("utf-8"),
                file_name="trotter_sweep_results.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with d_col2:
            st.download_button(
                "📥 Download Time Evolution CSV",
                data=df_time.to_csv(index=False).encode("utf-8"),
                file_name="time_evolution_results.csv",
                mime="text/csv",
                use_container_width=True,
            )
