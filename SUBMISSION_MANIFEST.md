# FloquetSim Explorer — Official Submission Package & Manifest

**Competition:** SRM University-AP Qiskit Fall Fest 2026 (Phase 1 — Online Qualification Stage)  
**Primary Track:** Track S3: "Noise in Trotter Simulation"  
**Secondary Track:** Track S-OI: "Open Innovation (Simulation)"  
**Release Tag:** `v1.2.0-submission`  
**Date:** October 11, 2026  

---

## 1. Submission Identity & Metadata

- **Project Title:** FloquetSim Explorer: Geometry-Aware Quantum Simulation & Trotter-Noise Benchmark
- **Track Code:** `S3` (Primary) / `S-OI` (Secondary)
- **Problem Statement Name:** Noise in Trotter Simulation
- **Institutional Partner:** SRM University-AP × IBM Quantum × quanTA Centre (University of Saskatchewan)
- **Primary Technology Stack:** Python 3.10+, Qiskit 1.x, Qiskit Aer, SciPy, NetworkX, Pandas, Matplotlib, Streamlit

---

## 2. Mandatory Competition Artifacts Directory

| Required Submission Item | Repository File Path | Description & Compliance Check |
| :--- | :--- | :--- |
| **Primary Execution Script** | `main.py` | Standalone headless CLI driver; executes full benchmark in $< 20$ seconds. |
| **Processor Definitions** | `processors/` | `demo_processor_A.json` (5Q line) & `demo_processor_B.json` (7Q heavy-hex ring). |
| **Tabular Benchmark Results** | `results/tables/` | Machine-readable CSV outputs (`circuit_metrics_comparison.csv`, etc.). |
| **Publication Figures** | `results/figures/` | High-resolution 300 DPI comparative plots (`fig1` through `fig4`). |
| **Repository README** | `README.md` | Comprehensive landing page with quickstart, architecture, and disclaimers. |
| **Scientific Research Report** | `report.md` | Publication-grade academic paper detailing model, methods, and results. |
| **Environment Specification** | `requirements.txt` | Pinned, reproducible dependencies (Qiskit 1.0+ architecture). |
| **Cloud Dev Container** | `.devcontainer/devcontainer.json` | 1-click cloud sandbox configuration for GitHub Codespaces. |
| **Interactive Dashboard** | `app.py` | Browser-based Streamlit scientific dashboard. |

---

## 3. One-Click Cloud Evaluation Instructions

To reproduce the complete benchmark in a clean environment without installing any software locally:

1. Open the repository in **GitHub Codespaces**.
2. Run headless execution from the terminal:

   ```bash
   python main.py
   ```

3. Run the automated test suite:

   ```bash
   pytest tests/ -v
   ```

4. (Optional) Launch the interactive dashboard:

   ```bash
   streamlit run app.py
   ```

---

## 4. Formal AI-Assistance Disclosure

In accordance with Section 11 of the Hackathon Participant Instructions:  
*Google Antigravity / Gemini was utilized as an autonomous software architect, code generator, and technical documentation assistant under human oversight and direction. All physical models, mathematical proofs, circuit formulations, and benchmark results were independently verified via automated test suites and classical ground-truth calculations.*
