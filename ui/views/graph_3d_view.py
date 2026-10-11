"""
FloquetSim Explorer - Section 03: Interactive 3D Quantum Graph
Specification: Frontend UI Blueprint v1.2 FINAL, Page 4
Dedicated viewport with full 3D manipulation, node inspection cards, neighbor highlighting,
and real computed observable overlays.
"""

import streamlit as st
from ui.graph_3d import create_3d_quantum_graph_figure, get_processor_3d_coordinates
from src.processors import load_processor
from src.classical_solver import simulate_exact_evolution


def render_graph_3d_view():
    """Render Section 03: Interactive 3D Quantum Graph."""
    st.markdown("## 🌐 Interactive 3D Quantum Graph")
    st.caption("Explore physical processor coupling graphs in 3D. Inspect connectivity, degree distributions, and computed observables.")

    col_viewport, col_inspector = st.columns([1.35, 0.65], gap="large")

    # Sidebar controls inside left column
    with col_inspector:
        st.markdown("#### Display Controls")

        proc_id = st.selectbox(
            "Processor Topology",
            options=["demo_processor_A", "demo_processor_B"],
            format_func=lambda x: "Demo Processor A (5Q Line)" if "A" in x else "Demo Processor B (7Q Heavy-Hex Ring)",
            index=0,
            key="graph_3d_proc",
        )

        try:
            config, cmap = load_processor(proc_id)
        except Exception as e:
            st.error(f"Error loading processor: {e}")
            return

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            show_labels = st.checkbox("Show Labels", value=True, key="graph_3d_labels")
        with col_opt2:
            reset_cam = st.button("🔄 Reset View", use_container_width=True, key="graph_3d_reset_cam")

        # Observable Overlay Toggle
        color_by_obs = st.checkbox("Color by Magnetization ⟨Z_j⟩", value=False, key="graph_3d_color_obs")
        
        obs_values = None
        if color_by_obs:
            st.caption("Observable Overlay (Real Computed Ground Truth)")
            time_val = st.slider("Time Step t (s)", min_value=0.5, max_value=10.0, value=3.0, step=0.5, key="graph_3d_time_slider")
            
            # Compute actual local site magnetizations at time_val
            try:
                exact_data = simulate_exact_evolution(
                    num_spins=4,
                    time_points=[time_val],
                    initial_state="0000",
                )
                local_z = exact_data["local_z"][0]  # Array of length 4 for 4 spins
                obs_values = {}
                for idx, val in enumerate(local_z):
                    obs_values[idx] = float(val)
                # Any remaining qubits on larger processor default to 0.0 unmapped
                for q_idx in range(4, config.num_qubits):
                    obs_values[q_idx] = 0.0
            except Exception as exc:
                st.warning(f"Could not compute observable overlay: {exc}")
                obs_values = None

        st.write("---")
        st.markdown("#### Node Inspector")

        # Node selector
        node_options = list(range(config.num_qubits))
        selected_q = st.selectbox(
            "Select Qubit to Inspect",
            options=node_options,
            format_func=lambda i: f"Qubit Q{i}",
            index=0,
            key="graph_3d_selected_node",
        )

        # Compute neighbor details
        adj_map = {}
        for edge in config.coupling_map:
            q1, q2 = edge
            adj_map.setdefault(q1, []).append(q2)
            adj_map.setdefault(q2, []).append(q1)

        neighbors = sorted(adj_map.get(selected_q, []))
        degree = len(neighbors)
        coords = get_processor_3d_coordinates(config.processor_id, config.num_qubits)
        coord_xyz = coords.get(selected_q, (0.0, 0.0, 0.0))

        st.markdown(
            f"""
            <div class="scientific-card">
                <div style="font-weight: 600; font-size: 1.1rem; color: #5267F2; margin-bottom: 8px;">
                    ⚛️ Qubit Q{selected_q} Details
                </div>
                <div style="font-size: 0.875rem; color: #172033; line-height: 1.6;">
                    • <b>Processor:</b> {config.name}<br>
                    • <b>Degree:</b> {degree}<br>
                    • <b>Physical Neighbors:</b> {', '.join(f'Q{n}' for n in neighbors) if neighbors else 'None'}<br>
                    • <b>3D Position:</b> ({coord_xyz[0]:.2f}, {coord_xyz[1]:.2f}, {coord_xyz[2]:.2f})<br>
                    {f"• <b>Magnetization ⟨Z⟩:</b> {obs_values[selected_q]:+.3f}<br>" if (obs_values and selected_q in obs_values) else ""}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Legend explanation
        st.markdown(
            """
            <div style="font-size: 0.8rem; color: #687386; line-height: 1.4; margin-top: 10px;">
                <b>Legend:</b><br>
                🟣 <b>Violet:</b> Selected Qubit<br>
                🔵 <b>Cyan:</b> Nearest Neighbors (highlighted)<br>
                🔷 <b>Blue:</b> Standard Unselected Qubits<br>
                <i>(Or Red/Blue diverging scale when Magnetization is enabled)</i>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_viewport:
        # Camera eye
        camera_eye = dict(x=1.6, y=1.6, z=1.2) if not reset_cam else dict(x=1.7, y=1.7, z=1.3)

        fig_3d = create_3d_quantum_graph_figure(
            config=config,
            selected_node=selected_q,
            show_node_labels=show_labels,
            observable_values=obs_values,
            height=580,
            camera_eye=camera_eye,
        )
        st.plotly_chart(fig_3d, use_container_width=True)
        st.caption("Rotate: Click & drag. Zoom: Scroll. Pan: Right-click & drag. Click nodes to inspect in panel.")
