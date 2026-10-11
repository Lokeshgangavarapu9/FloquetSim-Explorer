# Execution, Environment, and Academic Compliance Charter

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 9, Subphase 1.4  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Zero-Local-Installation Constraint Codification

To protect the user's host laptop (512 GB SSD storage limit):
1. **Host Boundary Enforcement:** No local package managers (`pip`, `npm`, `conda`), compilers, or runtime services shall be installed on the user's host operating system.
2. **Cloud Execution Environment:** All testing, linting, scientific simulation, and dashboard demonstrations are configured for **GitHub Codespaces**.
3. **Reproducibility Guarantee:** A fully automated `.devcontainer/devcontainer.json` configuration provides a 1-click cloud sandbox with all dependencies pre-pinned, requiring zero user host configuration.

---

## 2. Cloud Budget & Resource Quota Planning

Based on verified GitHub Codespaces free-tier allowances (GitHub Docs, 2024):

| Resource Dimension | Official Free Tier Allowance | FloquetSim Explorer Project Budget | Safety Margin |
| :--- | :--- | :--- | :--- |
| **Compute Core-Hours** | 120 core-hours per month | Total simulation budget: $\le 0.5$ core-hours across all sweeps | **> 240x Headroom** |
| **Virtual Machine** | Standard 2-core (4 GB RAM) | 4-qubit Hilbert space ($16 \times 16$ matrices) consumes < 500 MB RAM | **8x Memory Headroom** |
| **Storage Allocation** | 15 GB storage per month | Git repository + Python venv + results data: $\approx 1.8$ GB | **8x Storage Headroom** |
| **Port Forwarding** | Native private/public port forwarding | Port 8501 forwarded for Streamlit dashboard access | **Native Browser Access** |

---

## 3. Deterministic Random Seed Policy

To ensure 100% bit-for-bit reproducibility during automated evaluation:
1. **Transpiler Seeding:** All calls to `qiskit.transpile()` or `PassManager.run()` must explicitly supply `seed_transpiler=42`. This eliminates stochastic variance in Sabre layout and routing heuristics.
2. **Simulator Seeding:** All calls to `AerSimulator.run()` must explicitly supply `seed_simulator=42`. This ensures identical measurement shot distributions across evaluation runs.
3. **CLI Seed Override:** `main.py` provides an optional `--seed` flag (default: 42) allowing judges to verify statistical consistency across custom seeds.

---

## 4. Formal AI-Assistance Disclosure Statement

In strict compliance with Section 11 of the Hackathon Participant Instructions (**DOC-1**):

> **AI Assistance Disclosure:**  
> The FloquetSim Explorer project utilized Google Antigravity / Gemini as an autonomous AI software architect, code generator, and technical documentation assistant under human direction and verification. All quantum circuit formulations, Hamiltonian operators, numerical simulations, and performance metrics were derived from peer-reviewed scientific literature and independently validated through automated unit tests (`pytest`), classical exact reference solvers (`scipy.linalg.expm`), and deterministic Qiskit Aer simulation pipelines. The human project participant understands, verifies, and takes full responsibility for all submitted code, data, and conclusions.

---

## 5. Standardized Lifecycle Status Taxonomy

To eliminate premature claims of completion or overclaiming, every component in documentation and tracking registers must use one of the following five standardized statuses:

- `VERIFIED REQUIREMENT`: Rule or deliverable verified from official competition documents.
- `PLANNED`: Feature specified and scheduled in roadmap; no working code written yet.
- `IMPLEMENTED`: Code written and committed to repository; awaiting full testing.
- `TESTED`: Automated test suite executed against implementation.
- `PASSED`: Acceptance criteria 100% satisfied with zero test warnings or failures.
- `UNRESOLVED RESOURCE`: Missing asset (e.g., official processor JSONs) managed via fallback.
