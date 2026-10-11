# Application Framework Decision Memo: Streamlit Ratification

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 13, Subphase 5.2  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Trade-Off Analysis: Option A vs. Option B

To satisfy hackathon evaluation rubrics while strictly obeying the non-negotiable **zero-local-installation constraint** on the user's 512 GB laptop, two application architectures were evaluated:

| Evaluation Dimension | Option A: Next.js 14 + FastAPI (Dual-Runtime) | Option B: Monolithic Streamlit Dashboard (Single-Runtime) |
| :--- | :--- | :--- |
| **Runtime Dependencies** | Node.js 18+ (npm, yarn) AND Python 3.10+ | Pure Python 3.10+ only |
| **Build & Setup Complexity** | High: Separate `npm install`, `npm run build`, and `pip install` | Zero: Single `pip install -r requirements.txt` |
| **Local Host SSD Footprint** | Large: $\approx 850\,\text{MB}$ for `node_modules` + $\approx 900\,\text{MB}$ for venv | Minimal: $\approx 1.2\,\text{GB}$ total container footprint |
| **Cloud Port Forwarding** | Complex: Two forwarded ports (Next.js 3000 + FastAPI 8000) + CORS | Seamless: Single port 8501 forwarded natively in Codespaces |
| **Interactivity & Plotting** | Plotly.js / React components over HTTP JSON payload | Native `@st.cache_data`, Matplotlib, and Plotly charts |
| **Maintenance & Bug Surface** | High: Dual language type synchronization, network serialization | Low: Direct Python object binding from `src/` modules |
| **Headless Grading Risk** | Moderate: Judges might assume UI is required to grade | Zero: Headless `main.py` is the primary execution path |

---

## 2. Formal Architectural Decision (DEC-004)

> **RATIFICATION:**  
> **Option B (Monolithic Streamlit Dashboard with Decoupled Python Core)** is formally selected as the primary production application architecture for FloquetSim Explorer.

### Key Architectural Safeguards:
1. **Decoupled Scientific Engine:** All Hamiltonian math, circuit synthesis, classical exact solvers, transpilation, and simulation logic reside in pure, modular Python files under `src/`.
2. **Zero Code Duplication:** `app.py` and `main.py` import the exact same modules from `src/`. No simulation calculations are reimplemented inside the UI.
3. **Future REST Expansion:** The clean functional interface in `src/` preserves the ability to add FastAPI endpoints (`backend/app.py`) in future phases without modifying the underlying scientific kernel.
