"""
FloquetSim Explorer - Interactive 3D Quantum Graph Engine
Specification: Frontend UI Blueprint v1.2 FINAL, Sections 3, 4, 5
Renders responsive 3D quantum processor graphs with Plotly, stable spatial layouts,
node selection, neighbor highlighting, and observable data overlays.
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import plotly.graph_objects as go
from src.schema import ProcessorConfig


def get_processor_3d_coordinates(processor_id: str, num_qubits: int) -> Dict[int, Tuple[float, float, float]]:
    """
    Return stable, deterministic 3D coordinates (x, y, z) for quantum processor topology.
    Coordinates remain constant when toggling visual options.
    """
    coords = {}
    if "A" in processor_id or num_qubits == 5:
        # Processor A: 5-qubit linear chain gently curved in 3D for depth perception
        xs = [-2.0, -1.0, 0.0, 1.0, 2.0]
        ys = [0.1, 0.35, 0.0, -0.35, -0.1]
        zs = [0.15, -0.1, 0.25, -0.1, 0.15]
        for i in range(min(num_qubits, len(xs))):
            coords[i] = (xs[i], ys[i], zs[i])
    else:
        # Processor B: 7-qubit heavy-hex-inspired unicyclic topology
        # 6-node cycle (0, 1, 2, 3, 4, 5) with leaf node 6 branching off node 2
        radius = 1.8
        for i in range(6):
            # Arrange 6 cycle nodes around hexagon in xy-plane
            angle = i * (2.0 * np.pi / 6.0)
            coords[i] = (
                radius * np.cos(angle),
                radius * np.sin(angle),
                0.15 * np.sin(2 * angle),
            )
        # Node 6 connected to node 2, positioned elevated toward center
        if num_qubits >= 7:
            x2, y2, z2 = coords[2]
            coords[6] = (x2 * 0.45, y2 * 0.45, 0.85)

    # Fallback for arbitrary topologies
    for i in range(num_qubits):
        if i not in coords:
            coords[i] = (float(i), 0.0, 0.0)

    return coords


def create_3d_quantum_graph_figure(
    config: ProcessorConfig,
    selected_node: Optional[int] = None,
    show_node_labels: bool = True,
    show_edge_labels: bool = False,
    observable_values: Optional[Dict[int, float]] = None,
    observable_name: str = "Magnetization ⟨Z⟩",
    height: int = 500,
    width: Optional[int] = None,
    camera_eye: Optional[Dict[str, float]] = None,
) -> go.Figure:
    """
    Build interactive Plotly 3D Figure representing physical quantum processor graph.
    """
    coords = get_processor_3d_coordinates(config.processor_id, config.num_qubits)
    coupling_edges = config.coupling_map

    # Identify neighbors of selected node for highlighting
    neighbors = set()
    if selected_node is not None:
        for q1, q2 in coupling_edges:
            if q1 == selected_node:
                neighbors.add(q2)
            elif q2 == selected_node:
                neighbors.add(q1)

    fig = go.Figure()

    # 1. Draw Coupling Edges
    # Regular edges
    edge_x, edge_y, edge_z = [], [], []
    # Highlighted edges (incident to selected node)
    hl_edge_x, hl_edge_y, hl_edge_z = [], [], []

    for q1, q2 in coupling_edges:
        if q1 in coords and q2 in coords:
            p1, p2 = coords[q1], coords[q2]
            is_incident = (selected_node is not None) and (q1 == selected_node or q2 == selected_node)
            if is_incident:
                hl_edge_x.extend([p1[0], p2[0], None])
                hl_edge_y.extend([p1[1], p2[1], None])
                hl_edge_z.extend([p1[2], p2[2], None])
            else:
                edge_x.extend([p1[0], p2[0], None])
                edge_y.extend([p1[1], p2[1], None])
                edge_z.extend([p1[2], p2[2], None])

    # Standard edges trace
    if edge_x:
        fig.add_trace(
            go.Scatter3d(
                x=edge_x,
                y=edge_y,
                z=edge_z,
                mode="lines",
                line=dict(color="#CBD5E1", width=3.5),
                hoverinfo="none",
                name="Qubit Coupling",
                showlegend=False,
            )
        )

    # Highlighted incident edges trace
    if hl_edge_x:
        fig.add_trace(
            go.Scatter3d(
                x=hl_edge_x,
                y=hl_edge_y,
                z=hl_edge_z,
                mode="lines",
                line=dict(color="#8B5CF6", width=6),
                hoverinfo="none",
                name="Active Interaction",
                showlegend=False,
            )
        )

    # 2. Draw Qubit Nodes (Spheres)
    node_indices = list(range(config.num_qubits))
    node_x = [coords[i][0] for i in node_indices]
    node_y = [coords[i][1] for i in node_indices]
    node_z = [coords[i][2] for i in node_indices]

    node_colors = []
    node_sizes = []
    hover_texts = []
    text_labels = []

    # Degree map
    degree_map = {i: 0 for i in node_indices}
    adj_map = {i: [] for i in node_indices}
    for q1, q2 in coupling_edges:
        if q1 in degree_map and q2 in degree_map:
            degree_map[q1] += 1
            degree_map[q2] += 1
            adj_map[q1].append(q2)
            adj_map[q2].append(q1)

    for i in node_indices:
        deg = degree_map[i]
        nbrs_str = ", ".join(f"Q{n}" for n in sorted(adj_map[i]))

        # Hover text
        obs_str = ""
        if observable_values and i in observable_values:
            obs_str = f"<br>{observable_name}: <b>{observable_values[i]:+.3f}</b>"
        
        hover = (
            f"<b>Qubit Q{i}</b><br>"
            f"Processor: {config.name}<br>"
            f"Degree: {deg}<br>"
            f"Coupled to: [{nbrs_str}]"
            f"{obs_str}"
        )
        hover_texts.append(hover)
        text_labels.append(f"Q{i}" if show_node_labels else "")

        # Color & Size hierarchy
        if i == selected_node:
            node_colors.append("#8B5CF6")  # Vibrant violet for active node
            node_sizes.append(20)
        elif i in neighbors:
            node_colors.append("#29B6D8")  # Cyan for nearest neighbors
            node_sizes.append(17)
        elif observable_values and i in observable_values:
            val = observable_values[i]
            # Diverging colormap interpolation between -1.0 and +1.0
            node_colors.append(val)
            node_sizes.append(16)
        else:
            node_colors.append("#5267F2")  # Primary blue
            node_sizes.append(15)

    # Determine marker configuration
    marker_dict = dict(
        size=node_sizes,
        opacity=0.95,
        line=dict(color="#FFFFFF", width=2.5),
    )

    if observable_values and any(isinstance(c, (int, float)) for c in node_colors):
        marker_dict["color"] = [c if isinstance(c, (int, float)) else 0.0 for c in node_colors]
        marker_dict["colorscale"] = "RdBu_r"
        marker_dict["cmin"] = -1.0
        marker_dict["cmax"] = 1.0
        marker_dict["colorbar"] = dict(
            title=dict(text=observable_name, font=dict(size=11, color="#172033")),
            tickfont=dict(size=10, color="#687386"),
            len=0.75,
            thickness=14,
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
            textfont=dict(size=12, color="#172033", family="sans-serif"),
            hovertext=hover_texts,
            hoverinfo="text",
            marker=marker_dict,
            name="Qubits",
            showlegend=False,
        )
    )

    # Clean White Scientific Canvas Layout
    camera = dict(
        eye=camera_eye if camera_eye else dict(x=1.6, y=1.6, z=1.2),
        center=dict(x=0, y=0, z=0),
    )

    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        scene=dict(
            bgcolor="#FFFFFF",
            xaxis=dict(showbackground=False, showgrid=True, gridcolor="#F1F5F9", zeroline=False, showticklabels=False, title=""),
            yaxis=dict(showbackground=False, showgrid=True, gridcolor="#F1F5F9", zeroline=False, showticklabels=False, title=""),
            zaxis=dict(showbackground=False, showgrid=True, gridcolor="#F1F5F9", zeroline=False, showticklabels=False, title=""),
            camera=camera,
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        height=height,
    )
    if width:
        fig.update_layout(width=width)

    return fig
