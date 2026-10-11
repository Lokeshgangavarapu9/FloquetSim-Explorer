"""
FloquetSim Explorer - Section 03: Interactive 3D Quantum Graph
Specification: Nagrik Scientific Research Interface Design Reference
Interactive 3D quantum processor topology visualization with camera angle presets,
synchronized time transport control hub, node inspector, and active micro-sparkline trajectory.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from ui.graph_3d import (
    create_3d_quantum_graph_figure,
    create_2d_quantum_graph_figure,
    get_processor_3d_coordinates,
    get_processor_2d_coordinates,
)
from src.processors import load_processor, get_processor_status
from src.classical_solver import simulate_exact_evolution
from ui.theme import (
    apply_plotly_theme,
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


@st.cache_data
def get_cached_trajectory_data(num_spins: int = 4):
    """Generate dense exact time trajectory for synchronized visualization."""
    times = [float(t) / 10.0 for t in range(0, 51)]  # 0.0 to 5.0 s (51 steps)
    res = simulate_exact_evolution(
        num_spins=num_spins,
        time_points=times,
        initial_state="0000",
    )
    return times, res


def render_graph_3d_view():
    """Render Section 03: Interactive 3D Quantum Graph."""
    st.markdown("## 🌐 Interactive 3D Quantum Graph")
    st.caption("Inspect physical processor connectivity, node degrees, and local observables with camera presets and synchronized time transport.")

    # -------------------------------------------------------------
    # TOP TOOLBAR: ARCHITECTURE & DISPLAY CONTROLS
    # -------------------------------------------------------------
    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([1.3, 1.1, 1.1, 1.2], gap="medium")

    with ctrl_col1:
        proc_options = ["demo_processor_A", "demo_processor_B"]
        default_idx = 0 if st.session_state.get("selected_processor_id", "A") == "demo_processor_A" else 1
        proc_id = st.selectbox(
            "Processor Architecture",
            options=proc_options,
            index=default_idx,
            format_func=lambda x: "Demo Processor A (5-Qubit Line)" if "A" in x else "Demo Processor B (7-Qubit Hex-Ring)",
            key="g3d_proc_select",
        )
        st.session_state["selected_processor_id"] = proc_id

    try:
        config, cmap = load_processor(proc_id)
        status_info = get_processor_status(config)
    except Exception as e:
        st.error(f"Error loading processor: {e}")
        return

    with ctrl_col2:
        graph_dim_mode = st.radio(
            "Graph Dimension Mode",
            options=["3D Holographic", "2D Planar"],
            index=0,
            horizontal=True,
            key="g3d_dim_mode",
            help="Switch between 3D interactive holographic canvas and 2D planar graph projection.",
        )

    with ctrl_col3:
        color_mode = st.selectbox(
            "Node Color Encoding",
            options=["Default Highlight", "By Degree", "Instantaneous Magnetization ⟨Z⟩"],
            index=0,
            key="g3d_color_mode",
            help="Select scientific property encoded by node color.",
        )

    with ctrl_col4:
        st.markdown(
            f"""
            <div style="padding-top: 18px; font-size: 0.8rem; color: {COLOR_TEXT_SECONDARY};">
                <b>Demonstration Notice:</b> Verified synthetic topology.<br>
                Zero claims of physical IBM hardware calibration.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -------------------------------------------------------------
    # SYNCHRONIZED TIME TRANSPORT HUB
    # -------------------------------------------------------------
    times, traj_res = get_cached_trajectory_data(num_spins=4)
    total_timesteps = len(times)

    if "sim_time_idx" not in st.session_state:
        st.session_state["sim_time_idx"] = 0

    st.markdown("#### ⏱️ Synchronized Time Transport Control Hub")
    trans_c1, trans_c2, trans_c3, trans_c4, trans_c5, trans_c6 = st.columns([0.8, 0.8, 0.9, 0.8, 3.2, 1.2], gap="small")

    with trans_c1:
        if st.button("◀ Prev", key="btn_prev_step", use_container_width=True):
            st.session_state["sim_time_idx"] = max(0, st.session_state["sim_time_idx"] - 1)
            st.rerun()

    with trans_c2:
        if st.button("Next ▶", key="btn_next_step", use_container_width=True):
            st.session_state["sim_time_idx"] = min(total_timesteps - 1, st.session_state["sim_time_idx"] + 1)
            st.rerun()

    with trans_c3:
        if st.button("▶ Step +2", key="btn_step_2", use_container_width=True):
            st.session_state["sim_time_idx"] = min(total_timesteps - 1, st.session_state["sim_time_idx"] + 2)
            st.rerun()

    with trans_c4:
        if st.button("↺ Reset", key="btn_reset_time", use_container_width=True):
            st.session_state["sim_time_idx"] = 0
            st.rerun()

    with trans_c5:
        selected_time_idx = st.slider(
            "Scrub Simulation Time t (s)",
            min_value=0,
            max_value=total_timesteps - 1,
            value=st.session_state["sim_time_idx"],
            step=1,
            format="%d",
            label_visibility="collapsed",
            key="slider_time_idx",
        )
        if selected_time_idx != st.session_state["sim_time_idx"]:
            st.session_state["sim_time_idx"] = selected_time_idx
            st.rerun()

    current_idx = st.session_state["sim_time_idx"]
    current_t = times[current_idx]

    with trans_c6:
        st.markdown(
            f"""
            <div style="background-color:{COLOR_RAISED}; border:1px solid {COLOR_BORDER}; border-radius:6px; padding:6px 10px; text-align:center; font-family:'JetBrains Mono', monospace; font-size:0.85rem; color:{COLOR_CYAN}; font-weight:700;">
                t = {current_t:.2f} s
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Compute instantaneous observables
    obs_dict = {}
    if color_mode == "Instantaneous Magnetization ⟨Z⟩":
        current_local_z = traj_res["local_z"][current_idx]
        for spin_idx, z_val in enumerate(current_local_z):
            obs_dict[spin_idx] = z_val
        for q in range(4, config.num_qubits):
            obs_dict[q] = 0.0

    st.write("")

    # -------------------------------------------------------------
    # CAMERA ANGLE PRESETS (3D) OR PLANAR INDICATOR (2D)
    # -------------------------------------------------------------
    if graph_dim_mode == "3D Holographic":
        cam_col1, cam_col2, cam_col3, cam_col4, _ = st.columns([1.1, 1.2, 1.2, 1.0, 3.5], gap="small")
        
        if "camera_preset" not in st.session_state:
            st.session_state["camera_preset"] = dict(x=1.65, y=1.65, z=1.25)

        with cam_col1:
            if st.button("📐 Isometric 3D", key="cam_iso", use_container_width=True):
                st.session_state["camera_preset"] = dict(x=1.65, y=1.65, z=1.25)
                st.rerun()

        with cam_col2:
            if st.button("🎯 Planar (Top-Down)", key="cam_top", use_container_width=True):
                st.session_state["camera_preset"] = dict(x=0.01, y=0.01, z=2.50)
                st.rerun()

        with cam_col3:
            if st.button("🔭 Side Elevation", key="cam_side", use_container_width=True):
                st.session_state["camera_preset"] = dict(x=2.50, y=0.01, z=0.01)
                st.rerun()

        with cam_col4:
            if st.button("↺ Reset View", key="cam_reset", use_container_width=True):
                st.session_state["camera_preset"] = dict(x=1.65, y=1.65, z=1.25)
                st.rerun()
    else:
        st.markdown(
            f"""
            <div style="font-size:0.8rem; color:{COLOR_CYAN}; font-family:'JetBrains Mono', monospace; padding: 4px 0 8px 0;">
                ⚡ <b>2D Planar Projection:</b> Fixed-aspect orthographic topology view with node and coupling interactions.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -------------------------------------------------------------
    # MAIN WORKSPACE: GRAPH CANVAS (LEFT) & QUBIT INSPECTOR (RIGHT)
    # -------------------------------------------------------------
    graph_col, inspector_col = st.columns([1.45, 0.85], gap="large")

    with inspector_col:
        st.markdown("#### Qubit Telemetry Inspector")
        node_options = list(range(config.num_qubits))
        selected_node = st.selectbox(
            "Selected Active Qubit",
            options=node_options,
            format_func=lambda i: f"Qubit Q{i}",
            index=1 if config.num_qubits >= 2 else 0,
            key="g3d_node_select",
        )

        adj_map = {i: [] for i in range(config.num_qubits)}
        for q1, q2 in config.coupling_map:
            adj_map[q1].append(q2)
            adj_map[q2].append(q1)

        neighbors = sorted(adj_map.get(selected_node, []))
        coords_3d = get_processor_3d_coordinates(config.processor_id, config.num_qubits)
        coords_2d = get_processor_2d_coordinates(config.processor_id, config.num_qubits)
        pt_3d = coords_3d.get(selected_node, (0.0, 0.0, 0.0))
        pt_2d = coords_2d.get(selected_node, (0.0, 0.0))
        coord_display = f"({pt_3d[0]:.2f}, {pt_3d[1]:.2f}, {pt_3d[2]:.2f})" if graph_dim_mode == "3D Holographic" else f"({pt_2d[0]:.2f}, {pt_2d[1]:.2f})"

        # Node details card
        st.markdown(
            f"""
            <div class="scientific-card">
                <div style="font-size: 1.15rem; font-weight: 700; color: {COLOR_AMBER}; margin-bottom: 6px;">
                    ⚛ Active Node: Qubit Q{selected_node}
                </div>
                <div class="caption-text" style="line-height: 1.7;">
                    • <b>Degree:</b> {len(neighbors)} incident edges<br>
                    • <b>Physical Neighbors:</b> {', '.join(f'Q{n}' for n in neighbors) if neighbors else 'None'}<br>
                    • <b>Coordinates ({'3D' if graph_dim_mode == '3D Holographic' else '2D'}):</b> {coord_display}<br>
                </div>
                <hr style="margin: 8px 0; border: none; border-top: 1px solid {COLOR_BORDER};">
                <div style="font-size: 0.8rem; font-weight: 600; color: {COLOR_TEXT_PRIMARY}; margin-bottom: 6px;">
                    Incident Couplings:
                </div>
                <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                    {' '.join([f'<span class="param-pill">Q{selected_node} ↔ Q{n}</span>' for n in neighbors]) if neighbors else 'None'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Active state telemetry card
        if selected_node < 4:
            current_z = traj_res["local_z"][current_idx][selected_node]
            p0 = (1.0 + current_z) / 2.0
            p1 = (1.0 - current_z) / 2.0
            st.markdown(
                f"""
                <div class="scientific-card">
                    <div style="font-size: 0.82rem; font-weight: 700; color: {COLOR_CYAN}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                        Active State Telemetry (t = {current_t:.2f} s)
                    </div>
                    <div style="font-size: 0.88rem; line-height: 1.7;">
                        • <b>Instantaneous Polarization ⟨Z_{selected_node}⟩:</b> <span style="font-family:'JetBrains Mono', monospace; color:{COLOR_CYAN}; font-weight:700;">{current_z:+.4f}</span><br>
                        • <b>State Probability P(|0⟩):</b> <span style="font-family:'JetBrains Mono', monospace;">{p0:.3f}</span><br>
                        • <b>State Probability P(|1⟩):</b> <span style="font-family:'JetBrains Mono', monospace;">{p1:.3f}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Micro-Sparkline Plot for selected qubit over time
            st.markdown(f"###### ⟨Z_{selected_node}(t)⟩ Dynamic Micro-Sparkline")
            spark_times = times
            spark_z = [step_z[selected_node] for step_z in traj_res["local_z"]]

            fig_spark = go.Figure()
            fig_spark.add_trace(
                go.Scatter(
                    x=spark_times,
                    y=spark_z,
                    mode="lines",
                    line=dict(color=COLOR_CYAN, width=2),
                    name=f"⟨Z_{selected_node}⟩",
                    hoverinfo="x+y",
                )
            )
            # Current time marker
            fig_spark.add_trace(
                go.Scatter(
                    x=[current_t],
                    y=[current_z],
                    mode="markers",
                    marker=dict(color=COLOR_AMBER, size=9, symbol="circle"),
                    name="Current t",
                    hoverinfo="none",
                )
            )
            apply_plotly_theme(fig_spark, height=140)
            fig_spark.update_layout(
                margin=dict(l=35, r=15, t=10, b=25),
                showlegend=False,
                yaxis=dict(range=[-1.05, 1.05], dtick=1.0),
            )
            st.plotly_chart(fig_spark, use_container_width=True)
        else:
            st.info(f"Qubit Q{selected_node} is an idle ancilla/branch node for this 4-spin simulation.")

    with graph_col:
        st.markdown(f"#### {'3D Holographic' if graph_dim_mode == '3D Holographic' else '2D Planar'} Quantum Processor Canvas")
        if graph_dim_mode == "3D Holographic":
            fig_graph = create_3d_quantum_graph_figure(
                config=config,
                selected_node=selected_node,
                show_node_labels=True,
                show_connections=True,
                color_mode=color_mode,
                observable_values=obs_dict if obs_dict else None,
                height=490,
                camera_eye=st.session_state["camera_preset"],
                current_time=current_t,
            )
        else:
            fig_graph = create_2d_quantum_graph_figure(
                config=config,
                selected_node=selected_node,
                show_node_labels=True,
                show_connections=True,
                color_mode=color_mode,
                observable_values=obs_dict if obs_dict else None,
                height=490,
                current_time=current_t,
            )
        st.plotly_chart(fig_graph, use_container_width=True)
