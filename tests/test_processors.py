"""
Unit Test Suite for Processor Loading and Schema Validation
Specification: Master Engineering Specification v1.2, Subphase 10.1
"""

import pytest
from src.processors import load_processor, get_processor_status, resolve_processor_filepath
from src.schema import ProcessorConfig


def test_load_demo_processors():
    """Verify loading demo_processor_A and demo_processor_B."""
    config_a, cmap_a = load_processor("demo_processor_A")
    assert config_a.num_qubits == 5
    assert not config_a.is_official
    assert len(cmap_a.get_edges()) > 0

    config_b, cmap_b = load_processor("demo_processor_B")
    assert config_b.num_qubits == 7
    assert not config_b.is_official
    assert len(cmap_b.get_edges()) > 0


def test_processor_status_metadata():
    """Verify processor status reports correct provenance disclaimers."""
    config_a, _ = load_processor("demo_processor_A")
    status = get_processor_status(config_a)
    assert status["is_official"] is False
    assert "PROVISIONAL" in status["status_label"]
    assert "Not calibrated" in status["disclaimer_notice"]


def test_invalid_processor_id_raises():
    """Verify non-existent processor identifier raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_processor("non_existent_processor_xyz")
