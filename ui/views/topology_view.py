"""
FloquetSim Explorer - Section 05: Processor Topology Explorer
Specification: Frontend UI Blueprint v1.2 FINAL, Page 6
Dedicated analysis of quantum processor coupling graphs, graph distance realities,
and compiler routing constraints.
"""

import streamlit as st
from ui.graph_3d import create_3d_quantum_graph_figure, get_processor_3d_coordinates
from src.processors import load_processor, get_processor_status


def render_topology_view():
    """Render Section 05: Processor Topology Explorer."""
    st.markdown("## 🗺️ Processor Topology Explorer")
    st.caption("Investigate how hardware connectivity graphs, diameters, and degree constraints govern SWAP overhead in NISQ compilation.")

    col_info, col_graph, col_node = st.columns([0.85, 1.35, 0.8], gap="large")

    with col_info:
        st.markdown("#### Select Processor")
        proc_id = st.selectbox(
            "Active Architecture",
            options=["demo_processor_A", "demo_processor_B"],
            format_func=lambda x: "Demo Processor A (5Q Line)" if "A" in x else "Demo Processor B (7Q Heavy-Hex Ring)",
            key="topo_proc_select",
        )

        try:
            config, cmap = load_processor(proc_id)
            status_info = get_processor_status(config)
        except Exception as e:
            st.error(f"Error loading processor: {e}")
            return

        is_line = "A" in proc_id
        topo_type = "Linear Path Graph (P_5)" if is_line else "Heavy-Hex Cycle + Leaf (C_6 + P_1)"
        diameter = "4 hops" if is_line else "3 hops"

        st.markdown(
            f"""
            <div class="scientific-card">
                <b>Topology Metrics:</b><br>
                • <b>Processor:</b> {config.processor_id}<br>
                • <b>Physical Qubits:</b> {config.num_qubits}<br>
                • <b>Coupling Edges:</b> {len(config.coupling_map)}<br>
                • <b>Graph Type:</b> {topo_type}<br>
                • <b>Graph Diameter:</b> {diameter}<br>
                • <b>Status:</b> {'Official' if status_info['is_official'] else 'Provisional Demo'}<br>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### Edge Connections")
        edge_text = ", ".join(f"({e[0]},{e[1]})" for e in config.coupling_map)
        st.caption(f"Coupling pairs: {edge_text}")

        st.markdown(
            """
            <div class="banner-demo">
                <b>Boundary Routing Reality:</b><br>
                To simulate closed periodic boundary condition <i>Z3 Z0</i> across spins [0, 1, 2, 3]:<br>
                • Shortest path dist(0, 3) = <b>3 hops</b> on both Processor A and B.<br>
                • Neither processor contains an induced 4-cycle.<br>
                • Sabre routing must insert SWAP gates to bring spins adjacent.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_node:
        st.markdown("#### Node Inspector")
        node_options = list(range(config.num_qubits))
        selected_node = st.selectbox(
            "Select Qubit Node",
            options=node_options,
            format_func=lambda i: f"Qubit Q{i}",
            key="topo_node_select",
        )

        # Adjacency
        adj = []
        for e in config.coupling_map:
            if e[0] == selected_node:
                adj.append(e[1])
            elif e[1] == selected_node:
                adj.append(e[0])
        adj.sort()

        coords = get_processor_3d_coordinates(config.processor_id, config.num_qubits)
        pt = coords.get(selected_node, (0.0, 0.0, 0.0))

        st.markdown(
            f"""
            <div class="scientific-card">
                <span style="font-size: 1.1rem; font-weight: 600; color: #8B5CF6;">⚛️ Qubit Q{selected_node}</span><br><br>
                • <b>Degree:</b> {len(adj)}<br>
                • <b>Nearest Neighbors:</b> {', '.join(f'Q{n}' for n in adj) if adj else 'None'}<br>
                • <b>3D Position:</b> ({pt[0]:.2f}, {pt[1]:.2f}, {pt[2]:.2f})<br>
                • <b>Incident Edges:</b> {len(adj)}<br>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### Neighbor List")
        for n in adj:
            st.markdown(f"• **Qubit Q{n}** (1-hop distance)")

    with col_graph:
        st.markdown("#### 3D Processor Topology")
        fig_topo = create_3d_quantum_graph_figure(
            config=config,
            selected_node=selected_node,
            height=500,
            show_node_labels=True,
        )
        st.plotly_chart(fig_topo, use_container_width=True)
        st.caption("Rotate: Click & drag. Zoom: Scroll. Selected qubit is purple, incident edges and neighbors are highlighted in cyan.")
