"""
FloquetSim Explorer - Interactive 3D Quantum Graph Engine
Specification: Nagrik Scientific Research Interface Design Reference
Renders responsive 3D quantum processor graphs on deep navy-black canvas (#07090E) with
spherical nodes, luminous coupling beams, interactive camera rotation, node selection,
neighbor highlighting, HUD telemetry, and genuine observable data overlays.
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import plotly.graph_objects as go
from src.schema import ProcessorConfig
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
    COLOR_NODE_SELECTED,
    COLOR_NODE_NEIGHBOR,
    COLOR_NODE_DEFAULT,
    COLOR_EDGE_DEFAULT,
    COLOR_EDGE_ACTIVE,
)


def get_processor_3d_coordinates(processor_id: str, num_qubits: int) -> Dict[int, Tuple[float, float, float]]:
    """
    Return stable, deterministic 3D coordinates (x, y, z) for quantum processor topology.
    Coordinates remain constant when toggling visual options or parameter controls.
    Note: These are synthetic spatial coordinates for visualization, NOT physical chip coordinates.
    """
    coords = {}
    if "A" in processor_id or num_qubits == 5:
        # Processor A: 5-qubit linear chain gently curved in 3D for depth perception
        # Couplings: (0,1), (1,2), (2,3), (3,4)
        xs = [-2.0, -1.0, 0.0, 1.0, 2.0]
        ys = [0.12, 0.38, 0.0, -0.38, -0.12]
        zs = [0.18, -0.12, 0.28, -0.12, 0.18]
        for i in range(min(num_qubits, len(xs))):
            coords[i] = (xs[i], ys[i], zs[i])
    else:
        # Processor B: 7-qubit heavy-hex-inspired unicyclic demonstration topology
        # 6-node cycle (0, 1, 2, 3, 4, 5) with leaf node 6 branching off node 2: (2, 6)
        radius = 1.85
        for i in range(6):
            angle = i * (2.0 * np.pi / 6.0)
            coords[i] = (
                radius * np.cos(angle),
                radius * np.sin(angle),
                0.22 * np.sin(2 * angle),
            )
        # Node 6 connected to node 2, positioned elevated toward interior
        if num_qubits >= 7:
            x2, y2, z2 = coords[2]
            coords[6] = (x2 * 0.42, y2 * 0.42, 0.95)

    return coords


def get_processor_2d_coordinates(processor_id: str, num_qubits: int) -> Dict[int, Tuple[float, float]]:
    """
    Return stable, deterministic 2D coordinates (x, y) for planar quantum processor topology.
    Coordinates remain constant when toggling visual options or parameter controls.
    """
    coords = {}
    if "A" in processor_id or num_qubits == 5:
        # Processor A: 5-qubit linear chain on horizontal line
        xs = [-2.0, -1.0, 0.0, 1.0, 2.0]
        for i in range(min(num_qubits, len(xs))):
            coords[i] = (xs[i], 0.0)
    else:
        # Processor B: 7-qubit hexagon (0..5) + internal leaf node 6 off node 2
        radius = 1.75
        for i in range(6):
            angle = i * (2.0 * np.pi / 6.0)
            coords[i] = (radius * np.cos(angle), radius * np.sin(angle))
        if num_qubits >= 7:
            x2, y2 = coords[2]
            coords[6] = (x2 * 0.40, y2 * 0.40)

    # Fallback for arbitrary topologies
    for i in range(num_qubits):
        if i not in coords:
            coords[i] = (float(i), 0.0)

    return coords



def create_3d_quantum_graph_figure(
    config: ProcessorConfig,
    selected_node: Optional[int] = None,
    show_node_labels: bool = True,
    show_connections: bool = True,
    color_mode: str = "Default",
    observable_values: Optional[Dict[int, float]] = None,
    observable_name: str = "Magnetization ⟨Z⟩",
    node_size_scale: float = 1.0,
    edge_width_scale: float = 1.0,
    height: int = 480,
    width: Optional[int] = None,
    camera_eye: Optional[Dict[str, float]] = None,
    current_time: Optional[float] = None,
) -> go.Figure:
    """
    Build interactive Plotly 3D Figure representing physical quantum processor graph.
    Nagrik Scientific Interface: Deep canvas (#07090E), dual-beam coupling edges,
    holographic cyan and amber accents, selected node halo, and HUD telemetry.
    """
    coords = get_processor_3d_coordinates(config.processor_id, config.num_qubits)
    coupling_edges = config.coupling_map

    # Identify degree and neighbors
    adj_map: Dict[int, List[int]] = {i: [] for i in range(config.num_qubits)}
    degree_map: Dict[int, int] = {i: 0 for i in range(config.num_qubits)}
    for q1, q2 in coupling_edges:
        if q1 in adj_map and q2 in adj_map:
            adj_map[q1].append(q2)
            adj_map[q2].append(q1)
            degree_map[q1] += 1
            degree_map[q2] += 1

    selected_neighbors = adj_map.get(selected_node, []) if selected_node is not None else []

    fig = go.Figure()

    # 1. Coupling Edges: Dual-Layer Interaction Beams (Outer Soft Glow + Inner Sharp Core)
    if show_connections:
        edge_glow_x, edge_glow_y, edge_glow_z = [], [], []
        edge_core_x, edge_core_y, edge_core_z = [], [], []
        edge_act_x, edge_act_y, edge_act_z = [], [], []

        for q1, q2 in coupling_edges:
            if q1 not in coords or q2 not in coords:
                continue
            x1, y1, z1 = coords[q1]
            x2, y2, z2 = coords[q2]

            is_active_edge = (
                selected_node is not None
                and (
                    (q1 == selected_node and q2 in selected_neighbors)
                    or (q2 == selected_node and q1 in selected_neighbors)
                )
            )

            if is_active_edge:
                edge_act_x.extend([x1, x2, None])
                edge_act_y.extend([y1, y2, None])
                edge_act_z.extend([z1, z2, None])
            else:
                edge_glow_x.extend([x1, x2, None])
                edge_glow_y.extend([y1, y2, None])
                edge_glow_z.extend([z1, z2, None])
                edge_core_x.extend([x1, x2, None])
                edge_core_y.extend([y1, y2, None])
                edge_core_z.extend([z1, z2, None])

        # Passive Edges - Outer Glow
        if edge_glow_x:
            fig.add_trace(
                go.Scatter3d(
                    x=edge_glow_x,
                    y=edge_glow_y,
                    z=edge_glow_z,
                    mode="lines",
                    line=dict(color="#171E2E", width=max(4, int(5 * edge_width_scale))),
                    opacity=0.6,
                    hoverinfo="none",
                    showlegend=False,
                    name="Coupling Glow",
                )
            )
            # Passive Edges - Core Beam
            fig.add_trace(
                go.Scatter3d(
                    x=edge_core_x,
                    y=edge_core_y,
                    z=edge_core_z,
                    mode="lines",
                    line=dict(color=COLOR_BORDER, width=max(1.5, int(2.2 * edge_width_scale))),
                    opacity=0.9,
                    hoverinfo="none",
                    showlegend=False,
                    name="Coupling Core",
                )
            )

        # Active Incident Edges - Luminous Cyan Beams
        if edge_act_x:
            fig.add_trace(
                go.Scatter3d(
                    x=edge_act_x,
                    y=edge_act_y,
                    z=edge_act_z,
                    mode="lines",
                    line=dict(color=COLOR_CYAN, width=max(4, int(5 * edge_width_scale))),
                    opacity=0.95,
                    hoverinfo="none",
                    showlegend=False,
                    name="Active Couplings",
                )
            )

    # 2. Selected Node Target Halo
    if selected_node is not None and selected_node in coords:
        sx, sy, sz = coords[selected_node]
        fig.add_trace(
            go.Scatter3d(
                x=[sx],
                y=[sy],
                z=[sz],
                mode="markers",
                marker=dict(
                    size=int(28 * node_size_scale),
                    color="rgba(0, 213, 232, 0.25)",
                    line=dict(color=COLOR_CYAN, width=2.5),
                    symbol="circle",
                ),
                hoverinfo="none",
                showlegend=False,
                name="Target Halo",
            )
        )

    # 3. Node Coordinates and Scientific Color Encoding
    node_x, node_y, node_z = [], [], []
    node_colors, text_labels, hover_texts = [], [], []

    has_mag_data = bool(observable_values and len(observable_values) > 0)

    for i in range(config.num_qubits):
        x, y, z = coords[i]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        text_labels.append(f"Q{i}")

        # Scientific Telemetry Hover
        deg = degree_map.get(i, 0)
        neighbors_str = ", ".join(f"Q{n}" for n in adj_map.get(i, [])) or "None"
        obs_val = observable_values.get(i, None) if observable_values else None

        hover_html = (
            f"<b>Qubit Q{i}</b><br>"
            f"• Architecture: {config.name}<br>"
            f"• Incident Degree: {deg}<br>"
            f"• Coupled Neighbors: {neighbors_str}<br>"
            f"• Layout Coord: ({x:.2f}, {y:.2f}, {z:.2f})<br>"
        )

        if obs_val is not None:
            p0 = (1.0 + obs_val) / 2.0
            p1 = (1.0 - obs_val) / 2.0
            hover_html += (
                f"<hr style='margin:4px 0; border:none; border-top:1px solid #2A354D;'>"
                f"• {observable_name}: <b>{obs_val:+.4f}</b><br>"
                f"• State Prob P(|0⟩): <b>{p0:.3f}</b> | P(|1⟩): <b>{p1:.3f}</b>"
            )
        elif color_mode == "Instantaneous Magnetization ⟨Z⟩":
            hover_html += "<br><i>[Run simulation to view ⟨Z⟩ data]</i>"

        hover_texts.append(hover_html)

        # Color Decision
        if color_mode == "Instantaneous Magnetization ⟨Z⟩" and has_mag_data:
            val = observable_values.get(i, 0.0)
            node_colors.append(val)
        elif color_mode == "By Degree":
            node_colors.append(deg)
        else:
            if i == selected_node:
                node_colors.append(COLOR_AMBER)
            elif i in selected_neighbors:
                node_colors.append(COLOR_CYAN)
            else:
                node_colors.append(COLOR_VIOLET)

    # 4. Core Qubit Nodes
    marker_dict: Dict[str, Any] = dict(
        size=int(14 * node_size_scale),
        line=dict(color="#F4F7FB", width=1.5),
        opacity=0.95,
    )

    if color_mode == "Instantaneous Magnetization ⟨Z⟩" and has_mag_data:
        marker_dict["color"] = node_colors
        marker_dict["colorscale"] = "Tealrose"
        marker_dict["cmin"] = -1.0
        marker_dict["cmax"] = 1.0
        marker_dict["colorbar"] = dict(
            title=dict(text="⟨Z⟩", font=dict(color=COLOR_TEXT_PRIMARY, size=11)),
            tickfont=dict(size=10, color=COLOR_TEXT_SECONDARY),
            len=0.7,
            thickness=12,
            x=1.02,
        )
    elif color_mode == "By Degree":
        marker_dict["color"] = node_colors
        marker_dict["colorscale"] = "Viridis"
        marker_dict["colorbar"] = dict(
            title=dict(text="Degree", font=dict(color=COLOR_TEXT_PRIMARY, size=11)),
            tickfont=dict(size=10, color=COLOR_TEXT_SECONDARY),
            len=0.7,
            thickness=12,
            x=1.02,
        )
    else:
        marker_dict["color"] = node_colors

    fig.add_trace(
        go.Scatter3d(
            x=node_x,
            y=node_y,
            z=node_z,
            mode="markers+text" if show_node_labels else "markers",
            text=text_labels,
            textposition="top center",
            textfont=dict(size=11, color=COLOR_TEXT_PRIMARY, family="JetBrains Mono, monospace"),
            hovertext=hover_texts,
            hoverinfo="text",
            marker=marker_dict,
            name="Qubit Nodes",
            showlegend=False,
        )
    )

    # 5. Scene, Camera, and HUD Overlay
    camera = dict(
        eye=camera_eye if camera_eye else dict(x=1.65, y=1.65, z=1.25),
        center=dict(x=0, y=0, z=0),
    )

    hud_title = f"<b>{config.name}</b>"
    if current_time is not None:
        hud_title += f" &nbsp;•&nbsp; <b>t</b> = {current_time:.2f} s"

    fig.update_layout(
        paper_bgcolor=COLOR_CANVAS,
        scene=dict(
            bgcolor=COLOR_CANVAS,
            xaxis=dict(
                showbackground=False,
                showgrid=True,
                gridcolor=COLOR_BORDER,
                zeroline=False,
                showticklabels=False,
                title="",
            ),
            yaxis=dict(
                showbackground=False,
                showgrid=True,
                gridcolor=COLOR_BORDER,
                zeroline=False,
                showticklabels=False,
                title="",
            ),
            zaxis=dict(
                showbackground=False,
                showgrid=True,
                gridcolor=COLOR_BORDER,
                zeroline=False,
                showticklabels=False,
                title="",
            ),
            camera=camera,
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        height=height,
        annotations=[
            dict(
                x=0.02,
                y=0.96,
                xref="paper",
                yref="paper",
                text=hud_title,
                showarrow=False,
                font=dict(family="JetBrains Mono, monospace", size=11, color=COLOR_CYAN),
                align="left",
                bgcolor="rgba(15, 19, 29, 0.85)",
                bordercolor=COLOR_BORDER,
                borderwidth=1,
                borderpad=5,
            )
        ] if hud_title else [],
    )
    if width:
        fig.update_layout(width=width)

    return fig


def create_2d_quantum_graph_figure(
    config: ProcessorConfig,
    selected_node: Optional[int] = None,
    show_node_labels: bool = True,
    show_connections: bool = True,
    color_mode: str = "Default",
    observable_values: Optional[Dict[int, float]] = None,
    observable_name: str = "Magnetization ⟨Z⟩",
    node_size_scale: float = 1.0,
    edge_width_scale: float = 1.0,
    height: int = 440,
    width: Optional[int] = None,
    current_time: Optional[float] = None,
) -> go.Figure:
    """
    Build interactive Plotly 2D Figure representing physical quantum processor graph.
    Nagrik Scientific Interface: Planar canvas (#07090E), coupling lines,
    holographic cyan and amber accents, selected node halo, and HUD telemetry.
    """
    coords = get_processor_2d_coordinates(config.processor_id, config.num_qubits)
    coupling_edges = config.coupling_map

    # Identify degree and neighbors
    adj_map: Dict[int, List[int]] = {i: [] for i in range(config.num_qubits)}
    degree_map: Dict[int, int] = {i: 0 for i in range(config.num_qubits)}
    for q1, q2 in coupling_edges:
        if q1 in adj_map and q2 in adj_map:
            adj_map[q1].append(q2)
            adj_map[q2].append(q1)
            degree_map[q1] += 1
            degree_map[q2] += 1

    selected_neighbors = adj_map.get(selected_node, []) if selected_node is not None else []

    fig = go.Figure()

    # 1. 2D Coupling Lines
    if show_connections:
        edge_pass_x, edge_pass_y = [], []
        edge_act_x, edge_act_y = [], []

        for q1, q2 in coupling_edges:
            if q1 not in coords or q2 not in coords:
                continue
            x1, y1 = coords[q1]
            x2, y2 = coords[q2]

            is_active = (
                selected_node is not None
                and (
                    (q1 == selected_node and q2 in selected_neighbors)
                    or (q2 == selected_node and q1 in selected_neighbors)
                )
            )

            if is_active:
                edge_act_x.extend([x1, x2, None])
                edge_act_y.extend([y1, y2, None])
            else:
                edge_pass_x.extend([x1, x2, None])
                edge_pass_y.extend([y1, y2, None])

        # Passive edges
        if edge_pass_x:
            fig.add_trace(
                go.Scatter(
                    x=edge_pass_x,
                    y=edge_pass_y,
                    mode="lines",
                    line=dict(color=COLOR_BORDER, width=max(2.0, int(2.5 * edge_width_scale))),
                    hoverinfo="none",
                    showlegend=False,
                    name="Couplings",
                )
            )

        # Active edges
        if edge_act_x:
            fig.add_trace(
                go.Scatter(
                    x=edge_act_x,
                    y=edge_act_y,
                    mode="lines",
                    line=dict(color=COLOR_CYAN, width=max(4.0, int(4.5 * edge_width_scale))),
                    hoverinfo="none",
                    showlegend=False,
                    name="Active Couplings",
                )
            )

    # 2. Selected Node Target Halo
    if selected_node is not None and selected_node in coords:
        sx, sy = coords[selected_node]
        fig.add_trace(
            go.Scatter(
                x=[sx],
                y=[sy],
                mode="markers",
                marker=dict(
                    size=int(38 * node_size_scale),
                    color="rgba(0, 213, 232, 0.20)",
                    line=dict(color=COLOR_CYAN, width=2.5),
                    symbol="circle",
                ),
                hoverinfo="none",
                showlegend=False,
                name="Target Halo",
            )
        )

    # 3. Nodes and Hover Information
    node_x, node_y = [], []
    node_colors, text_labels, hover_texts = [], [], []
    has_mag_data = bool(observable_values and len(observable_values) > 0)

    for i in range(config.num_qubits):
        x, y = coords[i]
        node_x.append(x)
        node_y.append(y)
        text_labels.append(f"Q{i}")

        deg = degree_map.get(i, 0)
        neighbors_str = ", ".join(f"Q{n}" for n in adj_map.get(i, [])) or "None"
        obs_val = observable_values.get(i, None) if observable_values else None

        hover_html = (
            f"<b>Qubit Q{i} (2D Planar)</b><br>"
            f"• Architecture: {config.name}<br>"
            f"• Incident Degree: {deg}<br>"
            f"• Coupled Neighbors: {neighbors_str}<br>"
        )

        if obs_val is not None:
            p0 = (1.0 + obs_val) / 2.0
            p1 = (1.0 - obs_val) / 2.0
            hover_html += (
                f"<hr style='margin:4px 0; border:none; border-top:1px solid #2A354D;'>"
                f"• {observable_name}: <b>{obs_val:+.4f}</b><br>"
                f"• State Prob P(|0⟩): <b>{p0:.3f}</b> | P(|1⟩): <b>{p1:.3f}</b>"
            )

        hover_texts.append(hover_html)

        if color_mode == "Instantaneous Magnetization ⟨Z⟩" and has_mag_data:
            node_colors.append(observable_values.get(i, 0.0))
        elif color_mode == "By Degree":
            node_colors.append(deg)
        else:
            if i == selected_node:
                node_colors.append(COLOR_AMBER)
            elif i in selected_neighbors:
                node_colors.append(COLOR_CYAN)
            else:
                node_colors.append(COLOR_VIOLET)

    marker_dict: Dict[str, Any] = dict(
        size=int(22 * node_size_scale),
        line=dict(color="#F4F7FB", width=2),
        opacity=0.98,
    )

    if color_mode == "Instantaneous Magnetization ⟨Z⟩" and has_mag_data:
        marker_dict["color"] = node_colors
        marker_dict["colorscale"] = "Tealrose"
        marker_dict["cmin"] = -1.0
        marker_dict["cmax"] = 1.0
        marker_dict["colorbar"] = dict(
            title=dict(text="⟨Z⟩", font=dict(color=COLOR_TEXT_PRIMARY, size=11)),
            tickfont=dict(size=10, color=COLOR_TEXT_SECONDARY),
            len=0.7,
            thickness=12,
        )
    elif color_mode == "By Degree":
        marker_dict["color"] = node_colors
        marker_dict["colorscale"] = "Viridis"
        marker_dict["colorbar"] = dict(
            title=dict(text="Degree", font=dict(color=COLOR_TEXT_PRIMARY, size=11)),
            tickfont=dict(size=10, color=COLOR_TEXT_SECONDARY),
            len=0.7,
            thickness=12,
        )
    else:
        marker_dict["color"] = node_colors

    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text" if show_node_labels else "markers",
            text=text_labels,
            textposition="top center",
            textfont=dict(size=11, color=COLOR_TEXT_PRIMARY, family="JetBrains Mono, monospace"),
            hovertext=hover_texts,
            hoverinfo="text",
            marker=marker_dict,
            name="Qubits",
            showlegend=False,
        )
    )

    hud_title = f"<b>{config.name} (2D Planar)</b>"
    if current_time is not None:
        hud_title += f" &nbsp;•&nbsp; <b>t</b> = {current_time:.2f} s"

    fig.update_layout(
        paper_bgcolor=COLOR_CANVAS,
        plot_bgcolor=COLOR_CANVAS,
        xaxis=dict(
            visible=False,
            range=[-2.8, 2.8],
        ),
        yaxis=dict(
            visible=False,
            scaleanchor="x",
            scaleratio=1,
            range=[-2.3, 2.3],
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=height,
        annotations=[
            dict(
                x=0.02,
                y=0.96,
                xref="paper",
                yref="paper",
                text=hud_title,
                showarrow=False,
                font=dict(family="JetBrains Mono, monospace", size=11, color=COLOR_CYAN),
                align="left",
                bgcolor="rgba(15, 19, 29, 0.85)",
                bordercolor=COLOR_BORDER,
                borderwidth=1,
                borderpad=5,
            )
        ] if hud_title else [],
    )
    if width:
        fig.update_layout(width=width)

    return fig

