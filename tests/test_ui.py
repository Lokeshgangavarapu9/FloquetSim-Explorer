"""
FloquetSim Explorer - Frontend & Dependency Compatibility Tests
Specification: Master Engineering Specification v1.2, Quality & Validation Suite
Verifies that pyarrow and NumPy 1.x compatibility is maintained and
that Streamlit views (especially Scientific Results) render without ImportError.
"""

import pytest
import pandas as pd
import numpy as np


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


def test_scientific_results_view_imports():
    """Verify that all modules imported by results_view load cleanly without error."""
    import ui.views.results_view as rv
    assert hasattr(rv, "render_results_view")
    assert hasattr(rv, "get_cached_time_data")
    assert hasattr(rv, "get_cached_trotter_data")


def test_streamlit_apptest_scientific_results_navigation():
    """Verify that Streamlit AppTest can navigate to Scientific Results without ImportError."""
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file("app.py", default_timeout=35)
    at.run()
    assert not at.exception, f"Initial run exception: {[e.value for e in at.exception]}"

    # Switch to Scientific Results
    at.radio(key="main_nav_radio").set_value("Scientific Results").run()
    assert not at.exception, f"Scientific Results exceptions: {[e.value for e in at.exception]}"
    assert at.session_state["nav_destination"] == "Scientific Results"
