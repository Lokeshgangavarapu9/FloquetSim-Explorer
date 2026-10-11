"""
FloquetSim Explorer - Quantum Processor Schema Validator
Specification: Master Engineering Specification v1.2, Subphase 3.1
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class NoiseConfig:
    type: str = "depolarizing_synthetic"
    gate_error_1q: float = 0.001
    gate_error_2q: float = 0.01
    readout_error: List[float] = field(default_factory=lambda: [0.01, 0.02])
    t1_us: float = 100.0
    t2_us: float = 80.0
    gate_time_1q_ns: float = 35.0
    gate_time_2q_ns: float = 300.0


@dataclass
class ProcessorConfig:
    processor_id: str
    name: str
    num_qubits: int
    coupling_map: List[List[int]]
    basis_gates: List[str]
    is_official: bool
    hardware_provenance: str
    ports: List[int] = field(default_factory=list)
    qubit_properties: Dict[str, Any] = field(default_factory=dict)
    noise: NoiseConfig = field(default_factory=NoiseConfig)

    def validate(self) -> None:
        """Validate processor configuration invariants."""
        if self.num_qubits < 1:
            raise ValueError(f"num_qubits must be >= 1, got {self.num_qubits}")
        if not self.coupling_map:
            raise ValueError("coupling_map cannot be empty")
        for edge in self.coupling_map:
            if len(edge) != 2:
                raise ValueError(f"Each coupling edge must have exactly 2 nodes, got {edge}")
            q1, q2 = edge
            if not (0 <= q1 < self.num_qubits and 0 <= q2 < self.num_qubits):
                raise ValueError(
                    f"Edge {edge} references invalid qubit index for num_qubits={self.num_qubits}"
                )
        if not self.basis_gates:
            raise ValueError("basis_gates cannot be empty")
        if self.noise.t2_us > 2.0 * self.noise.t1_us:
            raise ValueError(
                f"Physical violation: T2 ({self.noise.t2_us} us) cannot exceed 2 * T1 ({2.0 * self.noise.t1_us} us)"
            )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProcessorConfig":
        """Instantiate and validate ProcessorConfig from a parsed dictionary."""
        noise_data = data.get("noise", {})
        noise_config = NoiseConfig(
            type=noise_data.get("type", "depolarizing_synthetic"),
            gate_error_1q=float(noise_data.get("gate_error_1q", 0.001)),
            gate_error_2q=float(noise_data.get("gate_error_2q", 0.01)),
            readout_error=noise_data.get("readout_error", [0.01, 0.02]),
            t1_us=float(noise_data.get("t1_us", 100.0)),
            t2_us=float(noise_data.get("t2_us", 80.0)),
            gate_time_1q_ns=float(noise_data.get("gate_time_1q_ns", 35.0)),
            gate_time_2q_ns=float(noise_data.get("gate_time_2q_ns", 300.0)),
        )

        config = cls(
            processor_id=data["processor_id"],
            name=data["name"],
            num_qubits=int(data["num_qubits"]),
            coupling_map=data["coupling_map"],
            basis_gates=data["basis_gates"],
            is_official=bool(data.get("is_official", False)),
            hardware_provenance=data.get("hardware_provenance", "Unspecified provenance"),
            ports=data.get("ports", []),
            qubit_properties=data.get("qubit_properties", {}),
            noise=noise_config,
        )
        config.validate()
        return config
