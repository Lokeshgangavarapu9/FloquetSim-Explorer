# FloquetSim Explorer: Geometry-Aware Quantum Simulation & Trotter-Noise Benchmark

[![SRM University-AP Qiskit Fall Fest 2026](https://img.shields.io/badge/SRM%20University--AP-Qiskit%20Fall%20Fest%202026-blue)](https://srmap.edu.in)
[![Track S3](https://img.shields.io/badge/Track-S3%3A%20Noise%20in%20Trotter%20Simulation-purple)](https://qiskit.org)
[![Qiskit Version](https://img.shields.io/badge/Qiskit-1.x%20Ready-613380)](https://qiskit.org)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new)

> An open-source, evidence-based investigation into how physical quantum processor coupling topology and compiler routing dictate the competing trade-off between Trotter discretization error and hardware decoherence in interacting quantum spin chains.

---

## Hardware Provenance Notice & Official File Fallback

> **[PROVISIONAL DEMONSTRATION TOPOLOGY (NON-OFFICIAL)]**  
> Standalone official `processor_A.json` and `processor_B.json` files were not provided in the public competition distribution kit. In accordance with Section 11 of Master Specification v1.2, this repository utilizes **Provisional Demonstration Topologies** (`demo_processor_A.json` and `demo_processor_B.json`) strictly conforming to the organizer JSON schema.
>
> The hardware loader automatically checks for official `processor_A.json` and `processor_B.json` first; if present, they are loaded seamlessly. When demonstration fixtures are active, all outputs display this disclaimer. Zero claims are made that these configurations represent physical IBM device calibrations.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Core Research Question & Hypotheses](#2-core-research-question--hypotheses)
3. [Physical Model & Hamiltonian Formulation](#3-physical-model--hamiltonian-formulation)
4. [Lie-Trotter Product Formula Discretization](#4-lie-trotter-product-formula-discretization)
5. [Processor Topologies & Routing Realities](#5-processor-topologies--routing-realities)
6. [System Architecture](#6-system-architecture)
7. [Repository Layout](#7-repository-layout)
8. [Zero-Install Cloud Quickstart (GitHub Codespaces)](#8-zero-install-cloud-quickstart-github-codespaces)
9. [Headless CLI Execution Guide](#9-headless-cli-execution-guide)
10. [Interactive Streamlit Dashboard](#10-interactive-streamlit-dashboard)
11. [Testing & Scientific Verification](#11-testing--scientific-verification)
12. [Project Lifecycle Status](#12-project-lifecycle-status)
13. [Scientific Limitations & Ethical Boundaries](#13-scientific-limitations--ethical-boundaries)
14. [AI-Assistance Disclosure](#14-ai-assistance-disclosure)
15. [References](#15-references)

---

## 1. Executive Summary

When simulating interacting quantum many-body systems on noisy intermediate-scale quantum (NISQ) processors, algorithms face a fundamental tension:

- **Trotter Approximation Error:** Discretizing continuous time evolution through Lie-Trotter product formulas requires increasing the step count $m$ to reduce mathematical discretization error ($\mathcal{O}(t^2/m)$).
- **Physical Hardware Noise:** Real quantum processors suffer from gate infidelities and decoherence. Increasing $m$ linearly inflates circuit depth and two-qubit gate counts, compounding physical noise.
- **Topological Routing Overhead:** Physical processors have sparse, constrained qubit coupling graphs. Interacting logical qubits that are physically separated require compiler-inserted SWAP gates (each adding 3 CNOTs), accelerating state degradation.

**FloquetSim Explorer** characterizes this trade-off by compiling an identical 4-spin closed-boundary Hamiltonian onto two distinct processor graphs—a 5-qubit linear baseline vs. a 7-qubit heavy-hex-inspired ring—comparing empirical compiler metrics, Trotter error, and simulated decoherence.

---

## 2. Core Research Question & Hypotheses

### Primary Research Question

> *How does quantum processor coupling topology govern the competing trade-off between Trotter discretization error and physical gate noise accumulation in quantum spin chain simulations?*

### Falsifiable Scientific Hypotheses

- **Hypothesis H1 (Error Competition):** As Trotter steps $m$ increase, ideal Trotter error converges toward zero asymptotically; in the presence of physical gate noise, total simulation error balances decaying mathematical error against growing physical decoherence, which may produce a non-monotonic error profile across $m \in [1, 5]$.
- **Hypothesis H2 (Topological Routing Overhead):** Compiling an identical 4-spin closed-boundary Hamiltonian onto Processor A (5-qubit line) versus Processor B (7-qubit heavy-hex ring) induces measurable variations in circuit depth, CNOT count, and inserted SWAP overhead due to differing graph diameters and alternative routing pathways.

---

## 3. Physical Model & Hamiltonian Formulation

The simulated physical system is a 4-spin quantum chain ($N=4$, Hilbert space dimension $2^4 = 16$) governed by an interacting Transverse-Field Ising Model (TFIM) under continuous quench evolution:
$$H = H_{ZZ} + H_X + H_Z$$
where all parameters share consistent angular frequency units ($\text{rad}\cdot\text{s}^{-1}$ with $\hbar = 1$):

- **Ising Interaction:** $H_{ZZ} = J \sum_{j=0}^{2} Z_j Z_{j+1} + J Z_3 Z_0$ with $J = 1.0\,\text{rad/s}$ (closed periodic boundary).
- **Transverse Field & Imperfection:** $H_X = \sum_{j=0}^{3} (h_x + \delta h_x^j) X_j$ with $h_x = 1.0\,\text{rad/s}$, $\delta h_x = 0.05\,\text{rad/s}$.
- **Longitudinal Field:** $H_Z = h_z \sum_{j=0}^{3} Z_j$ with $h_z = 0.1\,\text{rad/s}$.

Because $[H_{ZZ}, H_X] \neq 0$, the time-evolution operator cannot be factored without discretization error, providing the authentic basis for Trotterization.

---

## 4. Lie-Trotter Product Formula Discretization

Continuous evolution for duration $t$ is discretized into $m$ Trotter steps of duration $\Delta t = t/m$:
$$U_{\text{Trotter}}(m, t) = \left[ \left(\prod_{j=0}^3 e^{-i(h_x + \delta h_x^j)\Delta t X_j}\right) \left(\prod_{\langle j,k \rangle} e^{-i J_{jk}\Delta t Z_j Z_k}\right) \left(\prod_{j=0}^3 e^{-i h_z \Delta t Z_j}\right) \right]^m$$

Rotation angles in quantum gates are strictly dimensionless radians:
$$\theta_X^j = 2(h_x + \delta h_x^j)\Delta t, \quad \theta_{ZZ}^{jk} = 2 J_{jk}\Delta t, \quad \theta_Z^j = 2 h_z \Delta t$$

Asymptotic operator error is bounded by:
$$\| U_{\text{Trotter}}(m, t) - U_{\text{exact}}(t) \| \le \frac{C t^2}{m} \quad \text{as } m \to \infty$$

---

## 5. Processor Topologies & Routing Realities

```text
PROCESSOR A (5-Qubit Linear Chain):
  (0) ─── (1) ─── (2) ─── (3) ─── (4)

PROCESSOR B (7-Qubit Heavy-Hex-Inspired):
        (1) ─── (2) ─── (3)
       /         │         \
     (0)        (6)        (4)
       \                   /
        (5) ───────────── ┘
```

- **Processor A (`demo_processor_A`):** 5-qubit path graph $P_5$. Nearest-neighbor pairs $(0,1), (1,2), (2,3)$ have distance 1. The periodic boundary pair $(3,0)$ has distance $\text{dist}_A(0,3) = 3$ hops.
- **Processor B (`demo_processor_B`):** 7-qubit unicyclic graph (6-node cycle $C_6$ + leaf at node 2). Nodes 0 and 3 are antipodes with distance $\text{dist}_B(0,3) = 3$ hops.
- **Routing Reality:** Neither graph contains an induced 4-cycle ($C_4$). Both incur routing overhead when compiling the closed boundary term $Z_3 Z_0$. Routing overhead is measured empirically using Qiskit's Sabre router with fixed seeds.

---

## 6. System Architecture

FloquetSim Explorer decouples the scientific execution core from presentation layers:

```text
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
                            └─────────────────────────────────┘
```

---

## 7. Repository Layout

```text
FloquetSim-Explorer/
├── .devcontainer/
│   └── devcontainer.json         # 1-click cloud container setup (Codespaces)
├── docs/
│   ├── audit/                    # Phase 0 audits & verification logs
│   ├── hardware/                 # Processor schemas & topology analyses
│   ├── requirements/             # Track alignment & compliance charters
│   └── science/                  # Hamiltonian & solver specifications
├── processors/
│   ├── demo_processor_A.json     # 5-qubit linear demonstration fixture
│   └── demo_processor_B.json     # 7-qubit heavy-hex-inspired fixture
├── results/
│   ├── figures/                  # 300 DPI publication plots (PNG)
│   └── tables/                   # Benchmark metrics & sweep data (CSV)
├── src/                          # Core scientific simulation engine
│   ├── __init__.py
│   ├── schema.py                 # Dataclass processor configuration validator
│   ├── hamiltonian.py            # SparsePauliOp operator builder
│   ├── circuits.py               # Lie-Trotter circuit generator
│   ├── classical_solver.py       # SciPy expm exact reference solver
│   ├── processors.py             # Dynamic processor loader & fallback
│   ├── transpiler.py             # Deterministic Sabre compiler
│   ├── simulation.py             # AerSimulator execution dispatcher
│   ├── observables.py            # Pauli expectation value extraction
│   ├── metrics.py                # Hardware & error metric extractors
│   ├── noise.py                  # Synthetic demonstration noise model
│   ├── experiments.py            # Sweep orchestration engine
│   ├── reporting.py              # CSV export & publication figure renderer
│   ├── provenance.py             # Metadata & execution manifest logger
│   └── mitigation.py             # Optional ZNE & spectral analysis module
├── tests/                        # Comprehensive automated pytest test suite
│   ├── test_science.py           # Hamiltonian & Trotter convergence tests
│   ├── test_transpilation.py     # Transpiler determinism & A/B routing tests
│   ├── test_processors.py        # Schema validation & fallback tests
│   ├── test_noise.py             # Noise model & channel scaling tests
│   ├── test_physics_validation.py# Physical limits & conservation invariants
│   ├── test_reproducibility.py   # Multi-seed determinism tests
│   ├── test_artifacts.py         # CSV schema & file integrity tests
│   └── test_edge_cases.py        # Error handling & boundary tests
├── app.py                        # Interactive Streamlit dashboard
├── main.py                       # Standalone headless CLI entrypoint
├── requirements.txt              # Frozen dependency manifest
├── README.md                     # Repository landing documentation
└── report.md                     # Scientific research report
```

---

## 8. Zero-Install Cloud Quickstart (GitHub Codespaces)

To preserve the host laptop's 512 GB SSD limit, this project runs entirely inside **GitHub Codespaces** (120 core-hours/month free tier):

1. Click **Code** $\to$ **Codespaces** $\to$ **Create codespace on main**.
2. The `.devcontainer` automatically provisions Python 3.10, installs `requirements.txt`, and prepares the environment in $< 90$ seconds.
3. Open a cloud terminal and execute the headless benchmark:

   ```bash
   python main.py
   ```

---

## 9. Headless CLI Execution Guide

The primary benchmark is executed headlessly via `main.py`:

```bash
# Standard benchmark sweep (m=1..5, t=5.0s, shots=2048, seed=42)
python main.py

# Custom sweep
python main.py --trotter-steps 1,2,3,4,5 --time 5.0 --shots 2048 --seed 42 --output-dir results/
```

### Outputs Generated

- `results/tables/circuit_metrics_comparison.csv`
- `results/tables/trotter_sweep_results.csv`
- `results/tables/time_evolution_results.csv`
- `results/figures/fig1_trotter_noise_tradeoff.png`
- `results/figures/fig2_magnetization_dynamics.png`
- `results/figures/fig3_circuit_overhead.png`
- `results/figures/fig4_fourier_spectrum.png`
- `results/provenance.json`

---

## 10. Interactive Streamlit Dashboard

To launch the browser-based visualization dashboard:

```bash
streamlit run app.py --server.headless=true --server.port=8501
```

Codespaces automatically forwards port 8501 for instant browser preview.

---

## 11. Testing & Scientific Verification

The project includes an automated test suite executed via `pytest`:

```bash
pytest tests/ -v
```

- **Unitarity Check:** Validates exact solver $\det(U) = 1$, $U^\dagger U = I$ to $< 10^{-14}$.
- **Trotter Convergence:** Verifies ideal Trotter error converges toward zero asymptotically as $m \to \infty$.
- **Transpiler Determinism:** Asserts zero variance in depth, 2Q gates, and SWAP counts across repeated seeded runs.
- **Boundary Routing Invariant:** Confirms both Processor A and Processor B incur non-zero routing overhead for closed boundary conditions.

---

## 12. Project Lifecycle Status

| Phase | Milestone Description | Status |
| :---: | :--- | :---: |
| **0** | Resource Audit & Scientific Resolutions | **PASSED** |
| **1** | Project Definition & Competition Requirements | **PASSED** |
| **2** | Scientific Model & Mathematical Formulation | **PASSED** |
| **3** | Experimental Design & Processor Configuration | **PASSED** |
| **4** | Initial Repository README Preparation | **PASSED** |
| **5** | Architecture & Development Environment | **PASSED** |
| **6** | Scientific Kernel Development (`src/`) | **PASSED** |
| **7** | Processor Loading & Circuit Transpilation | **PASSED** |
| **8** | Noisy Simulation & Experimental Sweeps | **PASSED** |
| **9** | Results Generation & Scientific Reporting | **PASSED** |
| **10** | Core Testing & Validation Suite | **PASSED** |
| **11** | Streamlit Scientific Dashboard (`app.py`) | **PASSED** |
| **12** | End-to-End System Integration | **PASSED** |
| **13** | Final Documentation & Academic Report | **PASSED** |
| **14** | Submission Package Audit & Release | **PASSED** |

---

## 13. Scientific Limitations & Ethical Boundaries

1. **Classical Solvability:** The $N=4$ spin chain is trivially solvable on classical computers in milliseconds. No claims of quantum supremacy or advantage are made.
2. **Synthetic Noise Approximation:** Simulations use standard depolarizing and relaxation noise channels from the starter guide; they do not represent physical IBM hardware calibrations.

---

## 14. AI-Assistance Disclosure

In accordance with Section 11 of the Hackathon Participant Instructions:  
*Google Antigravity / Gemini was utilized as an autonomous AI software architect, code generator, and technical documentation assistant under human oversight and direction. All mathematical equations, circuit formulations, and benchmark results were independently verified via automated test suites and classical ground-truth calculations.*

---

## 15. References

1. H. F. Trotter, *On the product of semi-groups of operators*, Proc. Amer. Math. Soc. **10**(4), 545–551 (1959).
2. M. Suzuki, *General theory of fractal path integrals with applications to many-body theories*, J. Math. Phys. **32**(2), 400–407 (1991).
3. S. Lloyd, *Universal quantum simulators*, Science **273**(5278), 1073–1078 (1996).
4. Y. Kim et al., *Evidence for the utility of quantum computing before fault tolerance*, Nature **618**, 500–505 (2023).
5. G. Li, Y. Ding, & Y. Xie, *Tackling the qubit mapping problem for NISQ-era quantum devices*, ASPLOS, 1001–1014 (2019).
6. IBM Quantum, *Qiskit 1.0 Release and Migration Guide*, IBM Corporation (2024).
