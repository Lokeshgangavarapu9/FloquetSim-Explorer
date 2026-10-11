# Project Definition Document (PDD)

**Project Name:** FloquetSim Explorer  
**Competition:** SRM University-AP Qiskit Fall Fest 2026 (Phase 1 — Online Qualification)  
**Track:** Track S3 ("Noise in Trotter Simulation")  
**Specification:** Master Engineering Specification v1.2, Section 9, Subphase 1.5  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)  
**Status:** **FROZEN & RATIFIED**

---

## 1. Project Purpose & Core Research Question

**FloquetSim Explorer** is a full-stack quantum simulation and hardware benchmarking platform designed to investigate how quantum processor connectivity, circuit compilation overhead, Trotter approximation error, and hardware noise affect the digital simulation of interacting quantum spin chains.

### Core Research Question:
> *How does quantum processor coupling topology govern the competing trade-off between Trotter discretization error and physical gate noise accumulation in quantum spin chain simulations?*

---

## 2. Formal Scope Boundaries

| Dimension | In-Scope Boundaries (Locked) | Out-of-Scope (Prohibited) |
| :--- | :--- | :--- |
| **Physical Model** | 1D Transverse-Field Ising Model ($H = H_{ZZ} + H_X + H_Z$) with $N=4$ spins, continuous quench dynamics, and closed boundary loop ($Z_3 Z_0$). | Infinite spin chains ($N > 10$), continuous time-dependent Floquet drive, ungrounded discrete time-crystalline period doubling. |
| **Discretization** | First-order Lie-Trotter product formula swept across $m \in [1, 5]$ steps and evolution times $t \in [1, 10]$ seconds. | Higher-order Suzuki product formulas ($S_4, S_6$), arbitrary Trotter slicing without physical justification. |
| **Classical Reference** | Exact double-precision dense matrix exponentiation using `scipy.linalg.expm` on the $16 \times 16$ Hamiltonian matrix. | Classical tensor network heuristics (MPS/DMRG), unverified classical approximations. |
| **Hardware Topologies** | Processor A (5-qubit linear baseline: $0-1-2-3-4$) vs Processor B (7-qubit heavy-hex ring: $0-1-2-3-4-5-0 + 2-6$). | Physical IBM Quantum hardware execution (Phase 1 requires simulation), Phase 2 Processor C and D topologies. |
| **Processor Assets** | Standalone official JSONs auto-detected; fallback to `demo_processor_A.json` and `demo_processor_B.json` with prominent notice. | Fabricating official IBM hardware calibration data or claiming demo files are official. |
| **Compilation Pipeline** | Qiskit 1.x transpiler with deterministic seeding (`seed_transpiler=42`), SabreLayout, SabreSwap, basis gate decomposition to `['rz', 'sx', 'x', 'cx']`. | Unseeded stochastic compilation, manual gate synthesis without compiler transparency. |
| **Simulation Engine** | Qiskit Aer (`AerSimulator`) executing ideal statevector, ideal shots, and noisy shots with synthetic depolarizing and relaxation noise. | Cloud IBM QPU execution (permitted only as auxiliary in Phase 2). |
| **Software Architecture** | Decoupled Python core in `src/`, standalone headless CLI entrypoint `main.py`, single-runtime Streamlit dashboard `app.py`. | Complex dual-runtime web frameworks (Next.js / FastAPI), multi-tier databases, local host installations. |
| **Execution Environment** | GitHub Codespaces (120 core-hours/month, 15 GB storage, zero local laptop install). | Local package installations on user's 512 GB laptop SSD. |

---

## 3. High-Level System Architecture

```
                       ┌──────────────────────────────────────────────┐
                       │          GitHub Codespaces Container         │
                       │          (Python 3.10 / 2-Core VM)           │
                       └──────────────────────┬───────────────────────┘
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    ▼                                                   ▼
     ┌─────────────────────────────┐                     ┌─────────────────────────────┐
     │  Headless CLI (`main.py`)   │                     │  Streamlit UI (`app.py`)    │
     │  - Automated grading driver │                     │  - Interactive exploration  │
     │  - Exports CSVs & PNGs      │                     │  - Real-time Plotly charts  │
     └──────────────┬──────────────┘                     └──────────────┬──────────────┘
                    │                                                   │
                    └─────────────────────────┬─────────────────────────┘
                                              │ Imports
                                              ▼
                             ┌─────────────────────────────────┐
                             │       Core Scientific Engine    │
                             │             (`src/`)            │
                             │  - `hamiltonian.py`             │
                             │  - `circuits.py`                │
                             │  - `classical_solver.py`        │
                             │  - `processors.py`              │
                             │  - `transpiler.py`              │
                             │  - `simulation.py`              │
                             │  - `observables.py`             │
                             │  - `metrics.py`                 │
                             │  - `noise.py`                   │
                             │  - `mitigation.py` (Optional)   │
                             └─────────────────────────────────┘
```

---

## 4. Phase 1 Sign-off & Lock

The project scope, deliverables, metrics, and compliance policies are formally frozen. Proceeding to Phase 2 (Scientific Model and Mathematical Formulation).
