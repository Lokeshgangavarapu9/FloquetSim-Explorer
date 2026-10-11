# Mandatory Deliverables & Headless Execution Charter

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 9, Subphase 1.2  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Official Phase 1 Deliverables Matrix

In strict adherence to Page 3, Section 7 of the Hackathon Participant Instructions (**DOC-1**), FloquetSim Explorer guarantees the delivery of every required artifact:

| Mandatory Deliverable | Required Location | Functional Purpose | Headless Creation Mechanism | Status Classification |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Execution Script** | `main.py` (and/or `main.ipynb`) | End-to-end execution of simulation, transpilation, and export | Executes via CLI: `python main.py` | **MANDATORY (P0)** |
| **Processor Definitions** | `processors/` | Processor A and B coupling graphs and noise models | Auto-detected JSON files (`demo_processor_*.json`) | **MANDATORY (P0)** |
| **Tabular Benchmark Data** | `results/tables/*.csv` | Machine-readable comparison tables for circuit metrics and sweeps | Exported by `main.py` via Pandas | **MANDATORY (P0)** |
| **Publication Figures** | `results/figures/*.png` | 300 DPI comparative plots of Trotter error, dynamics, and overhead | Rendered by `main.py` via Matplotlib | **MANDATORY (P0)** |
| **Repository README** | `README.md` | Public repository landing page, architecture guide, quickstart | Static Markdown with verified links | **MANDATORY (P0)** |
| **Scientific Report** | `report.md` | In-depth academic paper covering model, methods, results, and discussion | Authored in publication-grade Markdown | **MANDATORY (P0)** |
| **Environment Manifest** | `requirements.txt` | Pinned, mutually compatible package dependencies | Frozen pip manifest | **MANDATORY (P0)** |
| **Cloud Configuration** | `.devcontainer/devcontainer.json` | 1-click cloud provisioning in GitHub Codespaces | Verified Docker Dev Container | **MANDATORY (P0)** |
| **Interactive Dashboard** | `app.py` | Browser-based interactive exploration of parameters and charts | Streamlit web application | **PLANNED ENHANCEMENT (P1)** (Non-blocking) |

---

## 2. Headless CLI Execution Mandate

The automated competition evaluation pipeline executes submissions inside headless environments without display servers or browser sessions. Therefore:

1. **Zero UI Coupling in Scientific Core:** The scientific core in `src/` must have **zero imports** from `streamlit`, `tkinter`, or display libraries.
2. **One-Command Headless Benchmark:**
   ```bash
   python main.py --trotter-steps 1,2,3,4,5 --time 5.0 --shots 2048 --seed 42
   ```
   Executing this command in a standard shell must:
   - Load Processor A and Processor B configurations.
   - Compute exact classical benchmarks via SciPy matrix exponentiation.
   - Construct and transpile quantum circuits across $m \in [1, 5]$ with deterministic seeds.
   - Run ideal and noisy Qiskit Aer simulations.
   - Generate all CSV tables in `results/tables/`.
   - Render all 300 DPI PNG figures in `results/figures/`.
   - Complete execution in under 60 seconds on a standard 2-core cloud VM.
   - Exit cleanly with exit code `0`.
3. **Dashboard Decoupling:** The Streamlit dashboard (`app.py`) acts purely as a presentation consumer of `src/`. If the dashboard is never launched, 100% of the competition deliverables are still generated and verified by `main.py`.
