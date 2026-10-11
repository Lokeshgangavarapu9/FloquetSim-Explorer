"""
FloquetSim Explorer - Section 05: Processor Topology Explorer
Specification: Nagrik Scientific Research Interface Design Reference
Three-part layout: Processor metrics on left, interactive 3D graph in center,
selected-qubit inspector on right, with coupling edge list table and graph theory glossary below.
"""

import streamlit as st
import pandas as pd
import networkx as nx
from ui.graph_3d import (
    create_3d_quantum_graph_figure,
    create_2d_quantum_graph_figure,
    get_processor_3d_coordinates,
    get_processor_2d_coordinates,
)
from src.processors import load_processor, get_processor_status
from ui.theme import (
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


def render_topology_view():
    """Render Section 05: Processor Topology Explorer."""
    st.markdown("## 🗺️ Processor Topology Explorer")
    st.caption("Investigate how hardware connectivity graphs, diameters, and degree constraints govern SWAP overhead in NISQ compilation.")

    # Top Selector
    top_sel_col1, top_sel_col2 = st.columns([1.5, 1.2])
    with top_sel_col1:
        proc_id = st.selectbox(
            "Select Processor Architecture",
            options=["demo_processor_A", "demo_processor_B"],
            format_func=lambda x: "Demo Processor A (5-Qubit Linear Chain)" if "A" in x else "Demo Processor B (7-Qubit Hex-Ring + Leaf)",
            key="topo_proc_select",
        )
        st.session_state["selected_processor_id"] = proc_id

    with top_sel_col2:
        topo_dim_mode = st.radio(
            "Visualization Mode",
            options=["3D Topology", "2D Planar"],
            index=0,
            horizontal=True,
            key="topo_dim_mode",
            help="Switch between 3D interactive spatial layout and 2D planar graph projection.",
        )

    try:
        config, cmap = load_processor(proc_id)
        status_info = get_processor_status(config)
    except Exception as e:
        st.error(f"Error loading processor: {e}")
        return

    # NetworkX representation
    G = nx.Graph()
    G.add_nodes_from(range(config.num_qubits))
    G.add_edges_from(config.coupling_map)

    is_line = "A" in proc_id
    num_nodes = config.num_qubits
    num_edges = len(config.coupling_map)
    avg_deg = sum(dict(G.degree()).values()) / num_nodes if num_nodes else 0
    diameter = nx.diameter(G) if nx.is_connected(G) else "N/A"
    is_conn = nx.is_connected(G)
    cycles = nx.cycle_basis(G)
    has_cycle = len(cycles) > 0
    has_branch = not is_line

    # 3-Part Main Workspace
    col_metrics, col_graph, col_inspector = st.columns([0.85, 1.45, 0.9], gap="medium")

    with col_metrics:
        st.markdown("#### Topology Metrics")
        st.markdown(
            f"""
            <div class="scientific-card">
                <div style="font-size: 0.88rem; line-height: 1.8;">
                    • <b>Number of Qubits:</b> <span style="font-family:'JetBrains Mono', monospace; color:{COLOR_CYAN}; font-weight:700;">{num_nodes}</span><br>
                    • <b>Coupling Edges:</b> <span style="font-family:'JetBrains Mono', monospace; font-weight:700;">{num_edges}</span><br>
                    • <b>Average Degree:</b> <span style="font-family:'JetBrains Mono', monospace;">{avg_deg:.2f}</span><br>
                    • <b>Graph Diameter:</b> <span style="font-family:'JetBrains Mono', monospace;">{diameter} hops</span><br>
                    • <b>Is Connected:</b> <span style="color: {COLOR_SUCCESS}; font-weight: 600;">{'Yes' if is_conn else 'No'}</span><br>
                    • <b>Has Branch:</b> <span style="font-weight: 600;">{'Yes' if has_branch else 'No'}</span><br>
                    • <b>Has Cycle:</b> <span style="font-weight: 600;">{'Yes' if has_cycle else 'No'}</span><br>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="banner-demo" style="font-size: 0.82rem;">
                <b>Boundary Routing Reality:</b><br>
                To simulate periodic boundary <i>Z3 Z0</i>:<br>
                • Shortest path dist(0, 3) = <b>3 hops</b> on both Processor A and B.<br>
                • Neither processor contains an induced 4-cycle.<br>
                • Sabre routing must insert SWAP gates to bring spins adjacent.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_inspector:
        st.markdown("#### Selected Qubit")
        node_options = list(range(config.num_qubits))
        selected_node = st.selectbox(
            "Active Qubit",
            options=node_options,
            format_func=lambda i: f"Qubit Q{i}",
            index=1 if config.num_qubits >= 2 else 0,
            key="topo_node_select",
        )

        neighbors = sorted(list(G.neighbors(selected_node)))
        coords_3d = get_processor_3d_coordinates(config.processor_id, config.num_qubits)
        coords_2d = get_processor_2d_coordinates(config.processor_id, config.num_qubits)
        pt_3d = coords_3d.get(selected_node, (0.0, 0.0, 0.0))
        pt_2d = coords_2d.get(selected_node, (0.0, 0.0))
        pos_display = f"({pt_3d[0]:.2f}, {pt_3d[1]:.2f}, {pt_3d[2]:.2f}) [3D]" if topo_dim_mode == "3D Topology" else f"({pt_2d[0]:.2f}, {pt_2d[1]:.2f}) [2D]"

        st.markdown(
            f"""
            <div class="scientific-card">
                <div style="font-size: 1.15rem; font-weight: 700; color: {COLOR_AMBER}; margin-bottom: 8px;">
                    ⚛ Qubit Q{selected_node}
                </div>
                <div class="caption-text" style="line-height: 1.7;">
                    • <b>Degree:</b> {len(neighbors)}<br>
                    • <b>Incident Neighbors:</b> {', '.join(f'Q{n}' for n in neighbors) if neighbors else 'None'}<br>
                    • <b>Position ({'3D' if topo_dim_mode == '3D Topology' else '2D'}):</b> {pos_display}<br>
                </div>
                <hr style="margin: 10px 0; border: none; border-top: 1px solid {COLOR_BORDER};">
                <div style="font-weight: 600; font-size: 0.84rem; color: {COLOR_TEXT_PRIMARY}; margin-bottom: 6px;">Neighbor List:</div>
                <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                    {' '.join([f'<span class="param-pill">Q{n}</span>' for n in neighbors]) if neighbors else 'None'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_graph:
        st.markdown(f"#### {'3D' if topo_dim_mode == '3D Topology' else '2D Planar'} Processor Topology")
        if topo_dim_mode == "3D Topology":
            fig_topo = create_3d_quantum_graph_figure(
                config=config,
                selected_node=selected_node,
                show_node_labels=True,
                show_connections=True,
                height=430,
            )
        else:
            fig_topo = create_2d_quantum_graph_figure(
                config=config,
                selected_node=selected_node,
                show_node_labels=True,
                show_connections=True,
                height=430,
            )
        st.plotly_chart(fig_topo, use_container_width=True)

    st.write("")

    # Coupling Edge List Table
    st.markdown("#### Coupling Edge List")
    edge_rows = []
    for idx, (q1, q2) in enumerate(config.coupling_map):
        edge_rows.append({
            "Edge #": idx + 1,
            "Qubit 1": f"Q{q1}",
            "Qubit 2": f"Q{q2}",
            "Coupling Type": "Bidirectional Physical Resonance",
            "Error Rate (2Q)": f"{config.noise.gate_error_2q:.3f}",
        })
    df_edges = pd.DataFrame(edge_rows)
    st.dataframe(df_edges, use_container_width=True)

    # Graph Theory Glossary
    with st.expander("📖 Graph Theory Reference & SWAP Routing Principles"):
        st.markdown(
            f"""
            <div style="font-size: 0.85rem; color: {COLOR_TEXT_SECONDARY}; line-height: 1.6;">
                • <b>Degree:</b> The number of physical coupling edges directly incident to a qubit node. High degree allows parallel two-qubit gates with fewer routing bottlenecks.<br>
                • <b>Graph Diameter:</b> The maximum shortest-path distance between any pair of qubits. A larger diameter directly increases the worst-case number of SWAP gates required to mediate non-local interactions.<br>
                • <b>Cycle Basis:</b> Independent closed loops formed by coupling edges. Demo Processor B features an induced 6-cycle, whereas Demo Processor A is a strictly acyclic tree (linear chain).<br>
                • <b>Boundary Routing (Periodic Boundary Conditions):</b> In closed-boundary spin chains, interactions like <i>Z_3 Z_0</i> require mediating gates between distant physical qubits. Because neither processor has native C4 connectivity, transpiler heuristics (e.g. Sabre) insert SWAP operations to align logical spin states.
            </div>
            """,
            unsafe_allow_html=True,
        )
