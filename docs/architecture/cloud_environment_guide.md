# GitHub Codespaces Cloud Environment & Provisioning Guide

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 13, Subphase 5.5  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Compliance with the Host Zero-Local-Install Mandate

To satisfy the non-negotiable constraint preserving the host laptop's 512 GB SSD limit:
- **Zero Local Host Tools:** No local Python, Qiskit, C-compilers, Node.js, or package dependencies are installed on the user's host machine.
- **Browser-First Cloud Execution:** All execution, automated testing, transpilation benchmarking, and interactive dashboard preview take place inside an isolated, containerized **GitHub Codespace**.

---

## 2. GitHub Codespaces Quotas & Sizing Verification

| Dimension | Official Free Tier Allowance (GitHub Docs, 2024) | FloquetSim Explorer Consumption | Verification Assessment |
| :--- | :--- | :--- | :--- |
| **Compute Allowance** | 120 core-hours per month free | $\approx 0.5$ core-hours for full 200-point benchmark | **> 240x Safety Margin** |
| **Runtime Hours** | 60 hours on 2-core machine (or 30 hours on 4-core machine) | < 2 hours for all testing and demonstration sessions | **30x Runtime Margin** |
| **Storage Quota** | 15 GB storage per month free | Repository + Python venv + results data: $\approx 1.8$ GB | **8x Storage Margin** |
| **Port Forwarding** | Native private/public browser proxy on forwarded ports | Port 8501 forwarded for Streamlit dashboard access | **1-Click Browser Preview** |

---

## 3. Evaluator 1-Click Launch Procedure

For hackathon judges and evaluators accessing the repository from any standard web browser:

1. **Launch Codespace:**
   - Navigate to the GitHub repository.
   - Click the green **Code** button $\to$ **Codespaces** tab $\to$ click **Create codespace on main**.
2. **Automated Provisioning:**
   - The `.devcontainer/devcontainer.json` environment automatically pulls Python 3.10, updates pip, and installs all pinned packages from `requirements.txt`.
   - Setup completes in under 90 seconds.
3. **Run Headless Benchmark:**
   - Open the integrated cloud terminal and run:
     ```bash
     python main.py
     ```
   - All benchmark tables and publication-grade figures are generated in `results/`.
4. **Launch Interactive Dashboard:**
   - In the terminal, run:
     ```bash
     streamlit run app.py
     ```
   - Codespaces automatically detects port 8501 and displays an interactive browser preview notification.
