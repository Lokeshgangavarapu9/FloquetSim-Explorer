# README Draft - Part 3: Project Status, Limitations & Disclaimers

## Project Status & Development Milestones

Development strictly tracks the 15 phases of Master Engineering Specification v1.2:

| Component / Subsystem | Lifecycle Status | Notes & Verification Gate |
| :--- | :--- | :--- |
| **Phase 0: Resource & Scientific Audit** | `PASSED` | Completed and ratified in `docs/audit/phase0_analysis_report.md`. |
| **Phase 1: Project Definition & Requirements** | `PASSED` | Completed and ratified in `docs/requirements/project_definition.md`. |
| **Phase 2: Scientific Model & Math Formulation** | `PASSED` | Completed and ratified in `docs/science/hamiltonian_spec.md`. |
| **Phase 3: Hardware Design & Schema** | `PASSED` | Completed; demonstration JSON fixtures created. |
| **Phase 4: Initial README Preparation** | `IN PROGRESS` | Skeleton README draft actively established. |
| **Phases 5–10: Scientific Kernel & Headless CLI** | `PLANNED` | Implementation scheduled in `src/` and `main.py`. |
| **Phase 11–12: Interactive Streamlit Dashboard** | `PLANNED` | Dashboard scheduled in `app.py`. |
| **Phases 13–14: Final Reporting & Submission Audit** | `PLANNED` | Final `report.md` and release bundle scheduled. |

---

## Hardware Provenance Notice & Official File Fallback

> **IMPORTANT NOTICE REGARDING PROCESSOR DEFINITIONS:**  
> Standalone official `processor_A.json` and `processor_B.json` files were not provided in the public competition distribution kit. In accordance with Section 11 of the Master Specification, this repository utilizes **Provisional Demonstration Topologies** (`demo_processor_A.json` and `demo_processor_B.json`) strictly adhering to the organizer JSON schema.
> 
> The hardware loader automatically searches for official `processor_A.json` and `processor_B.json` first; if present, they are loaded seamlessly. When demonstration fixtures are active, console outputs, data manifests, and the dashboard prominently display `[PROVISIONAL DEMONSTRATION TOPOLOGY (NON-OFFICIAL)]`. Zero claims are made that these configurations represent physical IBM device calibrations.

---

## Scientific Limitations & Ethical Boundaries

1. **Classical Simulation Scope (No Quantum Supremacy Claims):**  
   The simulated quantum spin chain has $N = 4$ qubits, corresponding to a $16 \times 16$ Hilbert space. This system is trivially and exactly solvable on classical computers in milliseconds. This project does not claim quantum advantage or supremacy; it serves as a rigorous compiler efficiency and NISQ noise benchmarking testbed.
2. **Synthetic Noise Approximation:**  
   Noise simulations employ a standard Qiskit Aer depolarizing, thermal relaxation ($T_1/T_2$), and readout error model. While grounded in realistic superconducting parameter magnitudes ($p_2 = 0.01$), it does not model non-Markovian 1/f noise, crosstalk, or dynamic calibration drifts of physical QPUs.
