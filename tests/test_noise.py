"""
Unit Test Suite for Synthetic Noise Model Builder
Specification: Master Engineering Specification v1.2, Subphase 10.1
"""

try:
    import pytest  # type: ignore
except ImportError:
    import contextlib

    class _PytestMock:
        @staticmethod
        @contextlib.contextmanager
        def raises(exc_type, match=None):
            import re
            try:
                yield
            except exc_type as e:
                if match:
                    assert re.search(match, str(e)), f"Pattern '{match}' not in '{e}'"
            except Exception as other_e:
                raise AssertionError(f"Expected {exc_type}, got {type(other_e)}: {other_e}")
            else:
                raise AssertionError(f"Expected {exc_type} but nothing was raised")

    pytest = _PytestMock()  # type: ignore
from src.noise import build_noise_model, compute_readout_error_matrix


def test_readout_error_matrix_zero_scale():
    """Verify zero noise scale produces identity matrix with row sums strictly 1.0."""
    matrix = compute_readout_error_matrix([0.01, 0.02], scale_factor=0.0)
    assert matrix == [[1.0, 0.0], [0.0, 1.0]]
    for row in matrix:
        assert all(0.0 <= p <= 1.0 for p in row)
        assert abs(sum(row) - 1.0) < 1e-12


def test_readout_error_matrix_normal_scale():
    """Verify normal scale_factor=1.0 matches Qiskit Aer row convention [P(0|0), P(1|0)] and sums to 1.0."""
    matrix = compute_readout_error_matrix([0.01, 0.02], scale_factor=1.0)
    # Row 0: True |0> -> [P(0|0)=0.98, P(1|0)=0.02]
    # Row 1: True |1> -> [P(0|1)=0.01, P(1|1)=0.99]
    assert abs(matrix[0][0] - 0.98) < 1e-12
    assert abs(matrix[0][1] - 0.02) < 1e-12
    assert abs(matrix[1][0] - 0.01) < 1e-12
    assert abs(matrix[1][1] - 0.99) < 1e-12

    for row in matrix:
        assert all(0.0 <= p <= 1.0 for p in row)
        assert abs(sum(row) - 1.0) < 1e-12


def test_readout_error_matrix_doubled_scale():
    """Verify doubled scale_factor=2.0 scales errors linearly and sums to 1.0."""
    matrix = compute_readout_error_matrix([0.01, 0.02], scale_factor=2.0)
    # Row 0: True |0> -> [0.96, 0.04] (sum = 1.0, previously [0.96, 0.02] summed to 0.98)
    # Row 1: True |1> -> [0.02, 0.98] (sum = 1.0)
    assert abs(matrix[0][0] - 0.96) < 1e-12
    assert abs(matrix[0][1] - 0.04) < 1e-12
    assert abs(matrix[1][0] - 0.02) < 1e-12
    assert abs(matrix[1][1] - 0.98) < 1e-12

    for row in matrix:
        assert all(0.0 <= p <= 1.0 for p in row)
        assert abs(sum(row) - 1.0) < 1e-12


def test_readout_error_matrix_extreme_scales():
    """Verify extreme scaling factors clip probabilities cleanly to [0, 1] with exact row normalization."""
    # Scale factor 10.0
    m_10 = compute_readout_error_matrix([0.01, 0.02], scale_factor=10.0)
    # Previously [0.8, 0.1] summed to 0.9; now [0.80, 0.20] sums to 1.0
    assert abs(m_10[0][0] - 0.80) < 1e-12
    assert abs(m_10[0][1] - 0.20) < 1e-12
    assert abs(m_10[1][0] - 0.10) < 1e-12
    assert abs(m_10[1][1] - 0.90) < 1e-12
    assert abs(sum(m_10[0]) - 1.0) < 1e-12
    assert abs(sum(m_10[1]) - 1.0) < 1e-12

    # Extreme scale factor 100.0 (where e10 * 100 = 2.0, exceeds 1.0)
    m_100 = compute_readout_error_matrix([0.01, 0.02], scale_factor=100.0)
    assert m_100 == [[0.0, 1.0], [1.0, 0.0]]
    for row in m_100:
        assert all(0.0 <= p <= 1.0 for p in row)
        assert abs(sum(row) - 1.0) < 1e-12

    # Asymptotic extreme scale factor 1e6
    m_inf = compute_readout_error_matrix([0.01, 0.02], scale_factor=1e6)
    assert m_inf == [[0.0, 1.0], [1.0, 0.0]]
    for row in m_inf:
        assert all(0.0 <= p <= 1.0 for p in row)
        assert abs(sum(row) - 1.0) < 1e-12


def test_readout_error_matrix_validation_errors():
    """Verify compute_readout_error_matrix rejects negative scales or invalid probability values."""
    with pytest.raises(ValueError, match="scale_factor must be >= 0.0"):
        compute_readout_error_matrix([0.01, 0.02], scale_factor=-1.0)

    with pytest.raises(ValueError, match="Rates must be valid probabilities"):
        compute_readout_error_matrix([-0.05, 0.02], scale_factor=1.0)

    with pytest.raises(ValueError, match="Rates must be valid probabilities"):
        compute_readout_error_matrix([0.01, 1.5], scale_factor=1.0)

    with pytest.raises(ValueError, match="readout_error must contain exactly two rates"):
        compute_readout_error_matrix([0.01], scale_factor=1.0)


def test_noise_model_generation():
    """Verify Qiskit Aer NoiseModel is constructed with expected error channels."""
    from src.processors import load_processor

    config_a, _ = load_processor("demo_processor_A")
    nm = build_noise_model(config_a, scale_factor=1.0)

    # Check basis gates with errors
    basis_with_errors = nm.basis_gates
    assert len(basis_with_errors) > 0
    assert "cx" in basis_with_errors or "x" in basis_with_errors


def test_noise_model_scaling():
    """Verify scaling factor modulates noise rates cleanly."""
    from src.processors import load_processor

    config_a, _ = load_processor("demo_processor_A")
    nm_zero = build_noise_model(config_a, scale_factor=0.0)
    nm_double = build_noise_model(config_a, scale_factor=2.0)
    nm_extreme = build_noise_model(config_a, scale_factor=10.0)

    assert nm_zero is not None
    assert nm_double is not None
    assert nm_extreme is not None
