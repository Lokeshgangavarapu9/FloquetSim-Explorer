# Approved Repository Structure & Module Boundaries

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 13, Subphase 5.3  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Directory Tree & File Inventory

The FloquetSim Explorer repository adheres to a clean, modular hierarchy designed for automated grading, containerized execution, and reproducibility:

```
c:\Users\LOKESH\quantum quiskit/
├── .devcontainer/
│   └── devcontainer.json         # Codespaces Docker container definition (Python 3.10)
├── docs/                         # Formal engineering specifications and audit logs
│   ├── audit/                    # Resource inventories, document audits, evidence matrix
│   ├── architecture/             # Execution specs, framework memos, cloud guides
│   ├── hardware/                 # Processor schema, fallback specs, topology validations
│   ├── requirements/             # Track alignment, mandatory deliverables, compliance
│   ├── science/                  # Hamiltonian specs, driving protocol, error metrics
│   ├── decision_log.md           # Persistent record of autonomous architectural decisions
│   └── phase_status.md           # Master 15-phase and 90-subphase progress tracker
├── processors/                   # Quantum hardware definition fixtures
│   ├── demo_processor_A.json     # 5-qubit linear baseline topology fixture
│   └── demo_processor_B.json     # 7-qubit heavy-hex-inspired ring topology fixture
├── results/                      # Standardized output artifacts directory
│   ├── figures/                  # 300 DPI publication plots (.png)
│   ├── tables/                   # Benchmark metrics and sweep datasets (.csv)
│   └── provenance.json           # Execution environment metadata manifest
├── src/                          # Modular scientific simulation engine
│   ├── __init__.py               # Package initializer
│   ├── schema.py                 # Dataclass processor configuration validator
│   ├── hamiltonian.py            # Pauli operator synthesis module
│   ├── circuits.py               # Lie-Trotter parameterized quantum circuit builder
│   ├── classical_solver.py       # Exact SciPy matrix exponentiation ground-truth solver
│   ├── processors.py             # Dynamic processor loader and fallback manager
│   ├── transpiler.py             # Deterministic Sabre transpiler and routing analyzer
│   ├── simulation.py             # AerSimulator execution dispatcher
│   ├── observables.py            # Pauli Z expectation values and spatial magnetization
│   ├── metrics.py                # Circuit complexity and simulation error calculators
│   ├── noise.py                  # Parameterized Qiskit Aer synthetic noise model builder
│   ├── experiments.py            # Parameter sweep orchestrator for CLI and UI
│   ├── reporting.py              # CSV export and publication figure rendering
│   └── mitigation.py             # Optional ZNE and spectral analysis module
├── tests/                        # Comprehensive automated pytest test suite
│   ├── __init__.py
│   ├── test_science.py           # Hamiltonian hermiticity, exact solver, and Trotter tests
│   ├── test_transpilation.py     # Transpiler determinism and empirical SWAP counting
│   ├── test_processors.py        # Schema validation and dynamic loader fallback tests
│   ├── test_noise.py             # NoiseModel validation and CPTP sanity checks
│   ├── test_physics_validation.py# Physical limiting cases and conservation invariants
│   ├── test_reproducibility.py   # Multi-seed deterministic reproducibility tests
│   ├── test_artifacts.py         # CSV schema and PNG header integrity tests
│   └── test_edge_cases.py        # Boundary value and failure resilience tests
├── .gitignore                    # Git hygiene rules (ignoring caches, logs, temp files)
├── app.py                        # Interactive Streamlit scientific dashboard
├── main.py                       # Standalone headless CLI benchmark entrypoint
├── requirements.txt              # Pinned, reproducible Python dependencies
├── README.md                     # Public repository documentation and landing page
└── report.md                     # Comprehensive academic research report
```

---

## 2. Module Boundary Invariants

1. **Pure Science in `src/`:** All scientific computation modules in `src/` must be free of side effects, GUI dependencies, and interactive input prompts.
2. **Headless Authority in `main.py`:** `main.py` is the primary executable required by automated grading; it executes the benchmark headlessly without invoking web servers.
3. **Reactive Presentation in `app.py`:** `app.py` acts purely as an interactive viewer and parameter controller, importing functions directly from `src/`.
