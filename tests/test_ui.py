"""
FloquetSim Explorer - Frontend & Dependency Compatibility Tests
Specification: Master Engineering Specification v1.2 & UI/UX Visual Blueprint
Verifies that pyarrow and NumPy 1.x compatibility is maintained,
that Plotly 3D graph figures render for all topologies and color modes,
and that Streamlit AppTest navigates across all seven application destinations without exceptions.
"""

import pytest
import pandas as pd
import numpy as np
from src.processors import load_processor
from ui.graph_3d import create_3d_quantum_graph_figure, get_processor_3d_coordinates


def test_pyarrow_numpy_compatibility():
    """Verify that pyarrow imports successfully and is compatible with installed NumPy."""
    try:
        import pyarrow as pa
    except ImportError as e:
        pytest.fail(f"pyarrow failed to import with active NumPy {np.__version__}: {e}")

    # Test basic Arrow table creation from pandas DataFrame
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0], "b": ["x", "y", "z"]})
    table = pa.Table.from_pandas(df)
    assert table.num_rows == 3
    assert table.num_columns == 2


def test_all_view_modules_import():
    """Verify that all seven view modules and the theme engine load cleanly."""
    import ui.theme as theme
    import ui.views.dashboard as v_dash
    import ui.views.home as v_home
    import ui.views.studio as v_studio
    import ui.views.graph_3d_view as v_g3d
    import ui.views.results_view as v_res
    import ui.views.topology_view as v_topo
    import ui.views.comparison_view as v_cmp
    import ui.views.reports_view as v_rep

    assert hasattr(theme, "apply_theme")
    assert hasattr(v_dash, "render_dashboard_view")
    assert hasattr(v_home, "render_home_view")
    assert hasattr(v_studio, "render_studio_view")
    assert hasattr(v_g3d, "render_graph_3d_view")
    assert hasattr(v_res, "render_results_view")
    assert hasattr(v_topo, "render_topology_view")
    assert hasattr(v_cmp, "render_comparison_view")
    assert hasattr(v_rep, "render_reports_view")


def test_3d_graph_figure_generation_both_processors():
    """Verify 3D graph generation and stable coordinates for Processor A and B."""
    # Processor A (5-qubit linear chain)
    cfg_a, _ = load_processor("demo_processor_A")
    coords_a = get_processor_3d_coordinates(cfg_a.processor_id, cfg_a.num_qubits)
    assert len(coords_a) == 5
    fig_a = create_3d_quantum_graph_figure(cfg_a, selected_node=1, color_mode="Default")
    assert len(fig_a.data) >= 2  # Edges + Nodes

    # Processor B (7-qubit heavy-hex unicyclic topology)
    cfg_b, _ = load_processor("demo_processor_B")
    coords_b = get_processor_3d_coordinates(cfg_b.processor_id, cfg_b.num_qubits)
    assert len(coords_b) == 7
    fig_b = create_3d_quantum_graph_figure(
        cfg_b,
        selected_node=2,
        color_mode="By Degree",
        observable_values={0: -0.5, 1: 0.5, 2: -0.8, 3: 0.8, 4: 0.0, 5: 0.0, 6: 0.0},
    )
    assert len(fig_b.data) >= 2


def test_2d_graph_figure_generation_both_processors():
    """Verify 2D planar graph generation and stable coordinates for Processor A and B."""
    from ui.graph_3d import create_2d_quantum_graph_figure, get_processor_2d_coordinates

    # Processor A (5-qubit linear chain)
    cfg_a, _ = load_processor("demo_processor_A")
    coords_2d_a = get_processor_2d_coordinates(cfg_a.processor_id, cfg_a.num_qubits)
    assert len(coords_2d_a) == 5
    fig_2d_a = create_2d_quantum_graph_figure(cfg_a, selected_node=1, color_mode="Default")
    assert len(fig_2d_a.data) >= 2

    # Processor B (7-qubit cycle + leaf)
    cfg_b, _ = load_processor("demo_processor_B")
    coords_2d_b = get_processor_2d_coordinates(cfg_b.processor_id, cfg_b.num_qubits)
    assert len(coords_2d_b) == 7
    fig_2d_b = create_2d_quantum_graph_figure(
        cfg_b,
        selected_node=2,
        color_mode="By Degree",
        observable_values={0: -0.5, 1: 0.5, 2: -0.8, 3: 0.8, 4: 0.0, 5: 0.0, 6: 0.0},
    )
    assert len(fig_2d_b.data) >= 2


def test_streamlit_apptest_navigation_all_sections():
    """Verify that Streamlit AppTest can navigate across all seven destinations cleanly."""
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file("app.py", default_timeout=35)
    at.run()
    assert not at.exception, f"Initial Dashboard view exceptions: {[e.value for e in at.exception]}"

    destinations = [
        "Landing Page",
        "Simulation Studio",
        "Interactive Quantum Graph",
        "Scientific Results",
        "Processor Topology Explorer",
        "Experiment Comparison",
        "Reports & About",
    ]

    for dest in destinations:
        at.radio(key="main_nav_radio").set_value(dest).run()
        assert not at.exception, f"Exceptions in section '{dest}': {[e.value for e in at.exception]}"
        assert at.session_state["nav_destination"] == dest


def test_site_resolved_data_presence_in_sweep():
    """Verify that run_time_dynamics_sweep produces site-resolved magnetization columns."""
    from src.experiments import run_time_dynamics_sweep
    df_sweep = run_time_dynamics_sweep(
        processor_id="demo_processor_A",
        time_list=[0.1, 0.5],
        trotter_step=2,
        shots=128,
        noise_scale=0.0,
    )
    for q_idx in range(4):
        assert f"exact_z_{q_idx}" in df_sweep.columns
        assert f"ideal_z_{q_idx}" in df_sweep.columns
        assert f"noisy_z_{q_idx}" in df_sweep.columns
        # Values must be within physical magnetization bounds [-1, 1]
        assert df_sweep[f"exact_z_{q_idx}"].between(-1.0001, 1.0001).all()


def test_3d_quantum_graph_figure_holographic_features():
    """Verify dual-layer edges, selected node halo, HUD annotation, and hover template."""
    cfg_a, _ = load_processor("demo_processor_A")
    fig = create_3d_quantum_graph_figure(
        cfg_a,
        selected_node=2,
        observable_values={0: -0.6, 1: 0.6, 2: -0.4, 3: 0.4, 4: 0.0},
        current_time=1.25,
    )
    # Check trace count: glow edges + core edges + halo + core nodes + node labels
    assert len(fig.data) >= 4
    # Check that annotations contain HUD telemetry
    annotations = fig.layout.annotations
    hud_found = any("demo_processor_A" in str(a.text) or cfg_a.name in str(a.text) for a in annotations)
    assert hud_found
    # Check that current time appears in HUD
    time_hud_found = any("t</b> = 1.25" in str(a.text) for a in annotations)
    assert time_hud_found


