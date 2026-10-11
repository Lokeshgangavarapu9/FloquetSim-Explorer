"""
FloquetSim Explorer - Section 01: Home (Introduction & Overview)
Specification: Frontend UI Blueprint v1.2 FINAL, Page 2
"""

import streamlit as st
from ui.graph_3d import create_3d_quantum_graph_figure
from src.processors import load_processor, get_processor_status


def render_home_view():
    """Render Section 01: Home Introduction & Overview."""
    col_hero, col_graph = st.columns([1.1, 0.9], gap="large")

    with col_hero:
        st.markdown(
            """
            <div style="padding-top: 20px;">
                <span style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: #5267F2;">
                    SRM University-AP Qiskit Fall Fest 2026
                </span>
                <h1 style="font-size: 2.75rem; font-weight: 700; line-height: 1.15; margin: 8px 0 16px 0; color: #172033;">
                    FloquetSim Explorer
                </h1>
                <p style="font-size: 1.15rem; color: #687386; line-height: 1.5; margin-bottom: 24px;">
                    Explore quantum spin dynamics. Understand noise.<br>
                    Visualize simulation results in interactive 3D.
                </p>
                <p style="font-size: 0.95rem; color: #475569; line-height: 1.6; margin-bottom: 28px;">
                    An open-source scientific research platform investigating how physical processor coupling 
                    governs the trade-off between Trotter discretization error and hardware decoherence in 
                    closed-boundary spin chains.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🚀 Explore Simulation", type="primary", use_container_width=True):
                st.session_state["nav_destination"] = "Simulation Studio"
                st.rerun()

        with btn_col2:
            if st.button("🌐 Explore 3D Quantum Graph", use_container_width=True):
                st.session_state["nav_destination"] = "Interactive 3D Graph"
                st.rerun()

    with col_graph:
        st.markdown(
            """
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 0.9rem; font-weight: 600; color: #172033;">
                    Physical Spin Network (3D Preview)
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Quick preview selector
        preview_proc = st.radio(
            "Processor Preview",
            options=["demo_processor_A", "demo_processor_B"],
            format_func=lambda x: "Proc A (5Q Line)" if "A" in x else "Proc B (7Q Ring)",
            horizontal=True,
            label_visibility="collapsed",
        )

        try:
            config, _ = load_processor(preview_proc)
            fig_hero = create_3d_quantum_graph_figure(
                config=config,
                height=380,
                show_node_labels=True,
            )
            st.plotly_chart(fig_hero, use_container_width=True)
            st.caption(f"Topology: {config.name} ({config.num_qubits} Qubits). Mouse to rotate & zoom.")
        except Exception as exc:
            st.info(f"3D Preview unavailable: {exc}")

    st.write("")
    st.write("")

    # Four Core Capability Cards (Blueprint Page 2)
    st.markdown("### Platform Modules")
    card_cols = st.columns(4)

    with card_cols[0]:
        st.markdown(
            """
            <div class="feature-card">
                <span class="feature-icon">⚛️</span>
                <div class="feature-title">Quantum Simulation</div>
                <div class="feature-desc">
                    First-order Lie-Trotter circuits parameterized by Transverse-Field Ising dynamics.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Studio", key="btn_card_studio", use_container_width=True):
            st.session_state["nav_destination"] = "Simulation Studio"
            st.rerun()

    with card_cols[1]:
        st.markdown(
            """
            <div class="feature-card">
                <span class="feature-icon">🌐</span>
                <div class="feature-title">Processor Topologies</div>
                <div class="feature-desc">
                    Interactive 3D graphs exploring coupling distances, SWAP overhead, and routing.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View Topologies", key="btn_card_topo", use_container_width=True):
            st.session_state["nav_destination"] = "Processor Topology Explorer"
            st.rerun()

    with card_cols[2]:
        st.markdown(
            """
            <div class="feature-card">
                <span class="feature-icon">📉</span>
                <div class="feature-title">Noise Analysis</div>
                <div class="feature-desc">
                    Depolarizing, thermal relaxation, and row-stochastic readout error calibration.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Noise", key="btn_card_noise", use_container_width=True):
            st.session_state["nav_destination"] = "Scientific Results"
            st.rerun()

    with card_cols[3]:
        st.markdown(
            """
            <div class="feature-card">
                <span class="feature-icon">📊</span>
                <div class="feature-title">Scientific Results</div>
                <div class="feature-desc">
                    Publication-grade 2D & 3D magnetization dynamics, Trotter trade-offs, and CSV exports.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View Results", key="btn_card_results", use_container_width=True):
            st.session_state["nav_destination"] = "Scientific Results"
            st.rerun()
