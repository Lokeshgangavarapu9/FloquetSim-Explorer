"""
FloquetSim Explorer - Landing Page (Public Entrypoint)
Specification: Qiskit Fall Fest 2026 Scientific Software Submission
A dark cinematic scientific landing interface featuring deep navy-black canvas (#07090E),
technical hairline borders (#2A354D), and holographic cyan (#00D5E8) & gold (#FFB300) accents.
Introduces the project, displays an interactive quantum processor graph with 2D/3D toggle,
and provides clear one-click actions to enter the scientific workspace.
"""

import streamlit as st
from ui.graph_3d import create_3d_quantum_graph_figure, create_2d_quantum_graph_figure
from src.processors import load_processor
from ui.theme import (
    COLOR_CANVAS,
    COLOR_SURFACE,
    COLOR_RAISED,
    COLOR_BORDER,
    COLOR_CYAN,
    COLOR_AMBER,
    COLOR_VIOLET,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
)


def render_landing_page():
    """Render the official Landing Page for FloquetSim Explorer."""
    # -------------------------------------------------------------
    # 1. HERO SECTION & INTERACTIVE QUANTUM VISUAL
    # -------------------------------------------------------------
    col_hero, col_visual = st.columns([1.1, 0.9], gap="large")

    with col_hero:
        st.markdown(
            f"""
            <div style="padding-top: 6px;">
                <span class="param-pill">
                    SRM University-AP • Qiskit Fall Fest 2026 • Track S3
                </span>
                <h1 style="margin: 12px 0 6px 0; color: {COLOR_TEXT_PRIMARY}; font-size: 2.35rem;">
                    FloquetSim Explorer
                </h1>
                <h3 style="color: {COLOR_CYAN}; margin-bottom: 14px; font-weight: 600; font-size: 1.25rem;">
                    Quantum Spin Dynamics & Trotter Noise Analysis Platform
                </h3>
                <p class="caption-text" style="font-size: 0.95rem; line-height: 1.6; margin-bottom: 22px;">
                    Investigate non-equilibrium quantum dynamics in the continuous Transverse-Field 
                    Ising Model (TFIM). Quantify the trade-off between higher-order Trotter discretization 
                    error and hardware noise accumulation across real demonstration processor topologies.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Primary Call to Action Buttons
        btn_c1, btn_c2, btn_c3 = st.columns(3)
        with btn_c1:
            if st.button("🚀 Enter Simulation Studio", type="primary", use_container_width=True, key="landing_cta_studio"):
                st.session_state["nav_destination"] = "Simulation Studio"
                st.rerun()
        with btn_c2:
            if st.button("🌐 3D/2D Quantum Graph", use_container_width=True, key="landing_cta_graph"):
                st.session_state["nav_destination"] = "Interactive Quantum Graph"
                st.rerun()
        with btn_c3:
            if st.button("📊 Scientific Results", use_container_width=True, key="landing_cta_results"):
                st.session_state["nav_destination"] = "Scientific Results"
                st.rerun()

        st.write("")

        # Implemented Model Formulation Card
        with st.expander("📖 Implemented Physical Model (Continuous 1D TFIM)", expanded=False):
            st.markdown(
                f"""
                <div style="font-size: 0.85rem; color: {COLOR_TEXT_SECONDARY}; line-height: 1.6;">
                    Continuous 1D Transverse-Field Ising Model for $N=4$ spins with periodic boundary conditions ($Z_3 Z_0$):
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.latex(r"H = H_{ZZ} + H_X + H_Z")
            st.latex(r"H_{ZZ} = J \sum_{j=0}^{2} Z_j Z_{j+1} + J_{\text{boundary}} Z_3 Z_0")
            st.latex(r"H_X = \sum_{j=0}^{3} (h_x + \delta h_x) X_j, \quad H_Z = h_z \sum_{j=0}^{3} Z_j")
            st.caption("Standard units: rad/s (ħ = 1). Parameters: J = 1.0, hx = 1.0, δhx = 0.05, hz = 0.1.")

    with col_visual:
        # Topology preview with 2D/3D switch
        top_c1, top_c2 = st.columns([1.6, 1.2])
        with top_c1:
            proc_options = ["demo_processor_A", "demo_processor_B"]
            default_idx = 0 if st.session_state.get("selected_processor_id", "A") == "demo_processor_A" else 1
            selected_proc = st.selectbox(
                "Processor Preview",
                options=proc_options,
                index=default_idx,
                format_func=lambda x: "Processor A (5Q Line)" if "A" in x else "Processor B (7Q Hex-Ring)",
                key="landing_proc_preview",
                label_visibility="collapsed",
            )
            st.session_state["selected_processor_id"] = selected_proc

        with top_c2:
            view_mode_landing = st.radio(
                "View Mode",
                options=["3D View", "2D View"],
                index=0,
                horizontal=True,
                key="landing_view_mode",
                label_visibility="collapsed",
            )

        try:
            cfg, _ = load_processor(selected_proc)
            if view_mode_landing == "3D View":
                fig_preview = create_3d_quantum_graph_figure(
                    config=cfg,
                    selected_node=1,
                    show_node_labels=True,
                    show_connections=True,
                    height=320,
                )
            else:
                fig_preview = create_2d_quantum_graph_figure(
                    config=cfg,
                    selected_node=1,
                    show_node_labels=True,
                    show_connections=True,
                    height=320,
                )
            st.plotly_chart(fig_preview, use_container_width=True)
            st.caption("Interactive Quantum Graph Preview. Click or drag to orbit. Switch to 2D for planar layout.")
        except Exception as e:
            st.error(f"Error loading processor preview: {e}")

    st.write("---")

    # -------------------------------------------------------------
    # 2. CORE SCIENTIFIC RESEARCH CAPABILITIES
    # -------------------------------------------------------------
    st.markdown("#### Supported Scientific Capabilities & Benchmark Protocols")
    
    cap_c1, cap_c2, cap_c3, cap_c4 = st.columns(4)

    with cap_c1:
        st.markdown(
            f"""
            <div class="scientific-card">
                <div style="font-size: 1.05rem; font-weight: 700; color: {COLOR_CYAN}; margin-bottom: 6px;">
                    ⚛ Simulation Studio
                </div>
                <div class="caption-text" style="line-height: 1.5; margin-bottom: 12px;">
                    Execute single-shot and sweep Trotter simulations with configurable noise parameters, time horizons, and deterministic seeds.
                </div>
                <div style="font-size: 0.78rem; color: {COLOR_AMBER}; font-family: 'JetBrains Mono', monospace;">
                    Aer CPU • 2Q Noise Models
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Studio", key="landing_goto_studio", use_container_width=True):
            st.session_state["nav_destination"] = "Simulation Studio"
            st.rerun()

    with cap_c2:
        st.markdown(
            f"""
            <div class="scientific-card">
                <div style="font-size: 1.05rem; font-weight: 700; color: {COLOR_AMBER}; margin-bottom: 6px;">
                    🌐 3D & 2D Quantum Graph
                </div>
                <div class="caption-text" style="line-height: 1.5; margin-bottom: 12px;">
                    Inspect processor coupling graphs with dual 2D/3D views, synchronized time scrubbers, active telemetry, and sparklines.
                </div>
                <div style="font-size: 0.78rem; color: {COLOR_CYAN}; font-family: 'JetBrains Mono', monospace;">
                    Dual-Layer Beams • Halo HUD
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Graphs", key="landing_goto_graph", use_container_width=True):
            st.session_state["nav_destination"] = "Interactive Quantum Graph"
            st.rerun()

    with cap_c3:
        st.markdown(
            f"""
            <div class="scientific-card">
                <div style="font-size: 1.05rem; font-weight: 700; color: {COLOR_VIOLET}; margin-bottom: 6px;">
                    📊 Scientific Results
                </div>
                <div class="caption-text" style="line-height: 1.5; margin-bottom: 12px;">
                    Analyze spatiotemporal wave heatmaps, 3D surface projections, Trotter trade-off curves, and optimal m* operating points.
                </div>
                <div style="font-size: 0.78rem; color: #10B981; font-family: 'JetBrains Mono', monospace;">
                    Heatmaps • Optimal m* • CSVs
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View Benchmarks", key="landing_goto_results", use_container_width=True):
            st.session_state["nav_destination"] = "Scientific Results"
            st.rerun()

    with cap_c4:
        st.markdown(
            f"""
            <div class="scientific-card">
                <div style="font-size: 1.05rem; font-weight: 700; color: #10B981; margin-bottom: 6px;">
                    ⎇ Topology Explorer
                </div>
                <div class="caption-text" style="line-height: 1.5; margin-bottom: 12px;">
                    Investigate graph theory metrics, shortest routing distances, and periodic boundary SWAP routing overhead.
                </div>
                <div style="font-size: 0.78rem; color: {COLOR_TEXT_SECONDARY}; font-family: 'JetBrains Mono', monospace;">
                    Sabre Routing • SWAP Deltas
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Inspect Topologies", key="landing_goto_topo", use_container_width=True):
            st.session_state["nav_destination"] = "Processor Topology Explorer"
            st.rerun()

    st.write("---")

    # -------------------------------------------------------------
    # 3. SCIENTIFIC ATTRIBUTION & PROVENANCE FOOTER
    # -------------------------------------------------------------
    foot_c1, foot_c2 = st.columns([2.0, 1.0])
    with foot_c1:
        st.markdown(
            f"""
            <div style="font-size: 0.8rem; color: {COLOR_TEXT_SECONDARY}; line-height: 1.6;">
                <b>Computational Engine:</b> Qiskit Aer Monte Carlo simulation calibrated against exact classical SciPy unitary integration.<br>
                <b>Demonstration Notice:</b> Processors A and B are synthetic demonstration topologies for compiler analysis. Zero claims of live IBM quantum cloud hardware connectivity.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with foot_c2:
        st.markdown(
            f"""
            <div style="text-align: right; font-size: 0.78rem; color: {COLOR_TEXT_SECONDARY}; font-family: 'JetBrains Mono', monospace;">
                Track S3: Noise in Trotter Simulation<br>
                SRM University-AP • 2026
            </div>
            """,
            unsafe_allow_html=True,
        )
