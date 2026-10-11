# Competition Track Alignment Specification

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 9, Subphase 1.1  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Track Identification & Dual-Alignment Strategy

FloquetSim Explorer is aligned with the official competition tracks published by the SRM University-AP Hackathon & Competitions Cell:

- **Primary Submission Track:** **Track S3 — "Noise in Trotter Simulation"**  
  - Domain: Quantum Simulation  
  - Core Focus: Lie-Trotter product formula simulation of interacting spin Hamiltonians, investigating the accumulation of hardware noise against discretization step count $m$.
  - Evaluation Alignment: Directly addresses the Track S3 prompt without requiring custom organizer approval.
  
- **Secondary Qualification Track:** **Track S-OI — "Open Innovation (Simulation)"**  
  - Domain: Quantum Simulation  
  - Secondary Focus: Topology-aware quantum compilation and comparative heavy-hex vs linear routing benchmarks for non-equilibrium quantum spin chains.

---

## 2. Official Evaluation Rubric Mapping

| Evaluation Rubric Category | Hackathon Criteria Focus | FloquetSim Explorer Implementation & Deliverable | Score Target |
| :--- | :--- | :--- | :--- |
| **Solution Correctness & Performance** | Does the quantum simulation work? Are results reasonable and supported by exact baseline? | Exact SciPy matrix exponentiation (`scipy.linalg.expm`) ground truth for $N=4$ spin chain; Lie-Trotter circuit with verified gate rotation angles; asymptotic convergence check. | Maximum (Exemplary) |
| **A/B Architecture Analysis** | Are differences between Processor A and B measured and explained with evidence? | Comparative compilation of identical spin model onto 5Q linear vs 7Q heavy-hex ring; empirical extraction of circuit depth, CNOT count, and Sabre SWAP overhead. | Maximum (Exemplary) |
| **Reproducibility** | Can judges clone the repository and reproduce results in a clean environment? | Deterministic seeding (`seed_transpiler=42`, `seed_simulator=42`); headless CLI script (`python main.py`); frozen `requirements.txt`; GitHub Codespaces 1-click devcontainer. | Maximum (Exemplary) |
| **Technical Reasoning** | Does the team explain why the observed behavior occurs? | Detailed `report.md` explaining physical graph distances ($\text{dist}(0,3)=3$), Lie-Trotter commutator bounds, and decoherence channels. | Maximum (Exemplary) |
| **Documentation & Presentation** | Are README, graphs, tables, and reports clear and complete? | Publication-quality 300 DPI figures (`results/figures/`), clean CSV tables (`results/tables/`), comprehensive `README.md`, and optional Streamlit dashboard. | Maximum (Exemplary) |

---

## 3. Scope Boundaries & Anti-Scope Charter

- **Included:** 1D TFIM spin chain ($N=4$), Lie-Trotter product formula sweeps ($m \in [1, 5]$), time evolution ($t \in [1, 10]$), Processor A vs Processor B comparison, exact classical reference, headless CLI, Streamlit dashboard.
- **Excluded (Out of Scope):** Unsubstantiated time-crystal period-doubling claims; claims of quantum supremacy or classical intractable simulation; fabrication of IBM device noise calibration data.
