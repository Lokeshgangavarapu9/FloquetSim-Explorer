"""
FloquetSim Explorer - Experiment Provenance Tracking Module
Specification: Master Engineering Specification v1.2, Subphase 9.3
Logs environment metadata, dependency versions, random seeds, and processor configurations.
"""

import sys
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List


def generate_provenance_manifest(
    output_dir: str = "results",
    seed_transpiler: int = 42,
    seed_simulator: int = 42,
    processors_used: List[str] = None,
) -> Dict[str, Any]:
    """
    Gather environmental provenance and write results/provenance.json.
    """
    if processors_used is None:
        processors_used = ["demo_processor_A", "demo_processor_B"]

    # Try importing versions safely
    def _get_pkg_version(pkg_name: str) -> str:
        try:
            import importlib.metadata
            return importlib.metadata.version(pkg_name)
        except Exception:
            try:
                mod = __import__(pkg_name)
                return getattr(mod, "__version__", "unknown")
            except Exception:
                return "not installed"

    manifest = {
        "project": "FloquetSim Explorer",
        "version": "1.2.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "qiskit_version": _get_pkg_version("qiskit"),
            "qiskit_aer_version": _get_pkg_version("qiskit_aer"),
            "numpy_version": _get_pkg_version("numpy"),
            "scipy_version": _get_pkg_version("scipy"),
            "pandas_version": _get_pkg_version("pandas"),
        },
        "seeds": {
            "seed_transpiler": seed_transpiler,
            "seed_simulator": seed_simulator,
        },
        "processors": processors_used,
        "artifacts_generated": [
            "results/tables/circuit_metrics_comparison.csv",
            "results/tables/trotter_sweep_results.csv",
            "results/tables/time_evolution_results.csv",
            "results/figures/fig1_trotter_noise_tradeoff.png",
            "results/figures/fig2_magnetization_dynamics.png",
            "results/figures/fig3_circuit_overhead.png",
            "results/figures/fig4_fourier_spectrum.png",
        ],
    }

    out_path = Path(output_dir) / "provenance.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest
