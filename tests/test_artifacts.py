"""
Unit Test Suite for Results Artifacts and File Schema Integrity
Specification: Master Engineering Specification v1.2, Subphase 10.4
"""

import json
from pathlib import Path
import pytest
import pandas as pd


def test_results_directory_structure():
    """Verify results directory and subdirectories exist."""
    results_dir = Path("results")
    assert results_dir.is_dir()
    assert (results_dir / "tables").is_dir()
    assert (results_dir / "figures").is_dir()


def test_csv_artifact_schemas_when_generated():
    """Verify that when CSV tables exist, they have valid schemas without NaNs."""
    tables_dir = Path("results/tables")
    csv_files = list(tables_dir.glob("*.csv"))

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        assert not df.empty, f"CSV {csv_file} is empty"
        assert not df.isnull().values.any(), f"CSV {csv_file} contains NaN values"


def test_provenance_json_schema_when_generated():
    """Verify provenance JSON adheres to required metadata schema."""
    prov_file = Path("results/provenance.json")
    if prov_file.is_file():
        with open(prov_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["project"] == "FloquetSim Explorer"
        assert "environment" in data
        assert "seeds" in data
