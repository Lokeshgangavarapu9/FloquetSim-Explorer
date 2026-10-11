"""
FloquetSim Explorer - Hardware Abstraction & Dynamic Processor Loader
Specification: Master Engineering Specification v1.2, Subphase 7.1 & 7.2
Handles dynamic detection of official processor JSONs with transparent fallback to demo fixtures.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from qiskit.transpiler import CouplingMap
from src.schema import ProcessorConfig

logger = logging.getLogger("FloquetSim.Processors")


def resolve_processor_filepath(processor_id_or_path: str, search_dir: str = "processors") -> Tuple[Path, bool]:
    """
    Resolve path to processor JSON file. Checks for official file first, then fallback.
    Returns: (resolved_path, is_official_file)
    """
    target = Path(processor_id_or_path)
    if target.is_file():
        # Direct file path provided
        return target, not target.name.startswith("demo_")

    p_dir = Path(search_dir)

    # Check for direct official name match (e.g. processor_A or processor_A.json)
    official_name = processor_id_or_path if processor_id_or_path.endswith(".json") else f"{processor_id_or_path}.json"
    official_path = p_dir / official_name
    if official_path.is_file():
        return official_path, True

    # If asking for 'A' or 'demo_processor_A' or 'processor_A'
    norm_id = processor_id_or_path.replace(".json", "")
    if norm_id in ["A", "processor_A", "demo_processor_A"]:
        off_file = p_dir / "processor_A.json"
        if off_file.is_file():
            return off_file, True
        demo_file = p_dir / "demo_processor_A.json"
        if demo_file.is_file():
            return demo_file, False

    if norm_id in ["B", "processor_B", "demo_processor_B"]:
        off_file = p_dir / "processor_B.json"
        if off_file.is_file():
            return off_file, True
        demo_file = p_dir / "demo_processor_B.json"
        if demo_file.is_file():
            return demo_file, False

    # Generic search in p_dir
    candidate = p_dir / f"{norm_id}.json"
    if candidate.is_file():
        return candidate, not candidate.name.startswith("demo_")

    raise FileNotFoundError(
        f"Could not locate processor definition for '{processor_id_or_path}' in '{search_dir}'. "
        f"Available fixtures: {list(p_dir.glob('*.json'))}"
    )


def load_processor(processor_id_or_path: str, search_dir: str = "processors") -> Tuple[ProcessorConfig, CouplingMap]:
    """
    Load, parse, and validate processor configuration JSON.
    Returns: (ProcessorConfig dataclass, Qiskit CouplingMap)
    """
    filepath, is_official_found = resolve_processor_filepath(processor_id_or_path, search_dir)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    config = ProcessorConfig.from_dict(data)

    # Ensure bidirectional coupling edges for Qiskit CouplingMap
    cmap_edges = []
    for edge in config.coupling_map:
        cmap_edges.append(edge)
        # Add reverse edge if not present to ensure symmetric two-qubit interaction capability
        rev_edge = [edge[1], edge[0]]
        if rev_edge not in config.coupling_map:
            cmap_edges.append(rev_edge)

    coupling_map = CouplingMap(cmap_edges)

    if not config.is_official:
        logger.warning(
            f"[NOTICE] Using Provisional Demonstration Topology '{config.processor_id}' "
            f"({config.name}). Zero claims of physical IBM calibration."
        )

    return config, coupling_map


def get_processor_status(config: ProcessorConfig) -> Dict[str, Any]:
    """
    Generate human-readable and machine-readable provenance metadata.
    """
    is_official = config.is_official
    status_label = "OFFICIAL ORGANIZER FIXTURE" if is_official else "PROVISIONAL DEMONSTRATION TOPOLOGY (NON-OFFICIAL)"
    disclaimer = (
        "Official hardware configuration certified by hackathon organizers."
        if is_official
        else "Provisional demonstration configuration strictly conforming to competition JSON schema. "
        "Not calibrated physical IBM Quantum QPU data."
    )

    return {
        "processor_id": config.processor_id,
        "name": config.name,
        "num_qubits": config.num_qubits,
        "is_official": is_official,
        "status_label": status_label,
        "hardware_provenance": config.hardware_provenance,
        "disclaimer_notice": disclaimer,
    }
