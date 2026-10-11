"""
FloquetSim Explorer - Parameterized Lie-Trotter Quantum Circuit Builder
Specification: Master Engineering Specification v1.2, Subphase 6.2
Rotation angles are strictly dimensionless radians: theta = 2 * coeff * dt.
"""

from typing import Optional
from qiskit import QuantumCircuit


def build_trotter_step_circuit(
    num_spins: int,
    dt: float,
    J: float = 1.0,
    J_boundary: float = 1.0,
    hz: float = 0.1,
    hx: float = 1.0,
    delta_hx: float = 0.05,
) -> QuantumCircuit:
    """
    Build a single first-order Lie-Trotter discretization slice of duration dt.
    U_step(dt) = exp(-i H_X dt) * exp(-i H_ZZ dt) * exp(-i H_Z dt)
    All rotation angles satisfy Qiskit convention: R_P(theta) = exp(-i theta/2 P),
    requiring theta = 2 * coeff * dt.
    """
    qc = QuantumCircuit(num_spins, name=f"TrotterStep_dt_{dt:.4f}")

    # 1. Longitudinal field R_Z layer
    theta_z = 2.0 * hz * dt
    if abs(theta_z) > 1e-12:
        for j in range(num_spins):
            qc.rz(theta_z, j)

    # 2. Longitudinal Ising R_ZZ interaction layer
    theta_zz = 2.0 * J * dt
    # Nearest-neighbor chain terms
    for j in range(num_spins - 1):
        if abs(theta_zz) > 1e-12:
            qc.rzz(theta_zz, j, j + 1)

    # Periodic boundary condition term
    if num_spins > 2 and J_boundary != 0.0:
        theta_boundary = 2.0 * J_boundary * dt
        if abs(theta_boundary) > 1e-12:
            qc.rzz(theta_boundary, num_spins - 1, 0)

    # 3. Transverse kick R_X layer
    for j in range(num_spins):
        theta_x = 2.0 * (hx + delta_hx) * dt
        if abs(theta_x) > 1e-12:
            qc.rx(theta_x, j)

    return qc


def build_trotter_circuit(
    num_spins: int = 4,
    trotter_steps: int = 3,
    total_time: float = 5.0,
    J: float = 1.0,
    J_boundary: float = 1.0,
    hz: float = 0.1,
    hx: float = 1.0,
    delta_hx: float = 0.05,
    initial_state: str = "0000",
    measure: bool = False,
) -> QuantumCircuit:
    """
    Synthesize complete m-step Lie-Trotter quantum circuit over total duration t.
    U_Trotter(m, t) = [ U_step(t / m) ]^m
    """
    if trotter_steps < 1:
        raise ValueError(f"trotter_steps must be >= 1, got {trotter_steps}")
    if total_time < 0.0:
        raise ValueError(f"total_time must be >= 0.0, got {total_time}")
    if len(initial_state) != num_spins:
        raise ValueError(f"initial_state length must equal num_spins={num_spins}, got '{initial_state}'")

    dt = total_time / trotter_steps

    if measure:
        qc = QuantumCircuit(num_spins, num_spins, name=f"TFIM_m{trotter_steps}_t{total_time:.1f}")
    else:
        qc = QuantumCircuit(num_spins, name=f"TFIM_m{trotter_steps}_t{total_time:.1f}")

    # State preparation: Qiskit little-endian (bit 0 is right-most)
    # initial_state string is read from left-to-right as q0, q1, ..., q_{N-1}
    for j, bit in enumerate(initial_state):
        if bit == "1":
            qc.x(j)
        elif bit != "0":
            raise ValueError(f"Invalid bit in initial_state: '{bit}' (expected '0' or '1')")

    if total_time > 0.0 and trotter_steps > 0:
        step_qc = build_trotter_step_circuit(
            num_spins=num_spins,
            dt=dt,
            J=J,
            J_boundary=J_boundary,
            hz=hz,
            hx=hx,
            delta_hx=delta_hx,
        )
        for _ in range(trotter_steps):
            qc.compose(step_qc, qubits=list(range(num_spins)), inplace=True)

    if measure:
        qc.measure(list(range(num_spins)), list(range(num_spins)))

    return qc
