# Complete Document Inspection Report

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 8, Subphase 0.2  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Mathematical Model & Equation Extraction

Across the supplied documents, the following formulations of the quantum system were extracted and audited:

### 1.1 Legacy Formulation in Resource A & B (Disputed)
In Resource A (p. 7) and Resource B (p. 3):
$$U_{\text{cycle}} = \exp\left(-i \tau \sum_j (g X_j + \varepsilon X_j)\right) \cdot \exp\left(-i \tau \sum_j J Z_j Z_{j+1}\right)$$
- **Audit Finding:** $(g X_j + \varepsilon X_j) = (g + \varepsilon) X_j$. Because $X_j$ commutes with itself, adding $\varepsilon X_j$ to $g X_j$ does not create a non-commuting perturbation or longitudinal disorder; it merely alters the rotation angle to $2(g+\varepsilon)\tau$.
- **Audit Finding on Stroboscopic Operator:** If the physical drive is delta kicks, $U_{\text{cycle}}$ is already exact and does not inherently require sub-Trotterization unless approximating a continuous Hamiltonian.

### 1.2 Unified Continuous Formulation in Resource E (Master Spec v1.2, Approved)
Master Spec v1.2 (Sections 2 & 4) unifies the system as an interacting Transverse-Field Ising Model (TFIM) under continuous quench evolution:
$$H = H_{ZZ} + H_X + H_Z$$
where:
$$H_{ZZ} = \sum_{j=0}^{N-2} J_{j,j+1} Z_j Z_{j+1} + J_{\text{boundary}} Z_{N-1} Z_0 \quad (J \in \text{rad/s})$$
$$H_X = \sum_{j=0}^{N-1} (h_x + \delta h_x^j) X_j \quad (h_x, \delta h_x \in \text{rad/s})$$
$$H_Z = \sum_{j=0}^{N-1} h_z^j Z_j \quad (h_z \in \text{rad/s})$$
- **Non-Commutativity:** $[H_X, H_{ZZ}] \neq 0$ creates genuine Lie-Trotter commutator errors.
- **Dimensional Units:** All Hamiltonian coefficients share units of angular frequency ($\text{rad}\cdot\text{s}^{-1}$ with $\hbar = 1$).
- **Gate Angles:** Rotation angles in quantum gates are dimensionless radians:
  $$\theta_X^j = 2(h_x + \delta h_x^j)\Delta t, \quad \theta_{ZZ}^{jk} = 2 J_{jk}\Delta t, \quad \theta_Z^j = 2 h_z^j \Delta t$$
- **Lie-Trotter Product Formula ($m$ steps, $\Delta t = t/m$):**
  $$U_{\text{Trotter}}(m, t) = \left[ \prod_{j=0}^{N-1} e^{-i (h_x + \delta h_x^j)\Delta t X_j} \prod_{\langle j,k \rangle} e^{-i J_{jk}\Delta t Z_j Z_k} \prod_{j=0}^{N-1} e^{-i h_z^j \Delta t Z_j} \right]^m$$

---

## 2. Processor Topology & Graph Extraction

### 2.1 Processor A (5-Qubit Linear Baseline)
- **Vertices:** $V_A = \{0, 1, 2, 3, 4\}$
- **Edges:** $E_A = \{(0,1), (1,2), (2,3), (3,4)\}$
- **Properties:** Graph diameter = 4, girth = $\infty$ (acyclic tree).
- **Sub-graph for $N=4$ Spins:** Logical spins $\{q_0, q_1, q_2, q_3\}$ map natively to $\{0, 1, 2, 3\}$. Nearest-neighbor open chain edges $(0,1), (1,2), (2,3)$ have physical distance 1 (0 SWAPs).
- **Boundary Term $(3,0)$:** $\text{dist}_A(0,3) = 3$ hops. Requires compiler-inserted SWAP gates to couple spin 3 and spin 0.

### 2.2 Processor B (7-Qubit Heavy-Hex-Inspired Graph)
- **Vertices:** $V_B = \{0, 1, 2, 3, 4, 5, 6\}$
- **Edges:** $E_B = \{(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (2,6)\}$
- **Properties:** Graph diameter = 3, girth = 6. Comprises a 6-node cycle plus one external branch at node 2.
- **Topological Reality:** Nodes 0 and 3 are on opposite poles of the 6-node ring:
  - Path 1: $0 - 1 - 2 - 3$ (3 hops)
  - Path 2: $0 - 5 - 4 - 3$ (3 hops)
  - Thus, $\text{dist}_B(0,3) = 3$.
- **Critical Correction:** Neither Processor A nor Processor B contains an induced 4-cycle ($C_4$). Both incur routing overhead when closing the boundary loop ($Z_3 Z_0$). SWAP counts must be measured empirically via Qiskit's Sabre router rather than fabricated.

---

## 3. UI/UX Wireframe & System Data-Flow Inspection

### 3.1 Initial Proposal in Resource B (Next.js + FastAPI)
- Proposed Next.js 14 frontend connecting over REST/WebSocket to FastAPI backend.
- **Bottlenecks Identified:** Requires dual runtimes (Node.js 18+ and Python 3.10+), npm packages, port management, and cross-runtime build scripts. This directly conflicts with the user's 512 GB laptop zero-local-install constraint and adds unnecessary failure points.

### 3.2 Approved Streamlit Production Architecture in Resource E
- Monolithic Streamlit dashboard (`app.py`) backed by a decoupled Python core (`src/`).
- Operates inside a single Python cloud container (GitHub Codespaces).
- Native Plotly/Matplotlib embedding, reactive `@st.cache_data`, and one-click cloud port forwarding (port 8501).

---

## 4. Hardware and Observable Metrics Extraction

- **Circuit Depth:** Total sequential gate layers in compiled `QuantumCircuit`.
- **1-Qubit Gate Count:** Total `['rz', 'sx', 'x']` operations.
- **2-Qubit Gate Count:** Total native CNOT/ECR operations.
- **SWAP Gate Overhead:** Explicit count of routing SWAPs (each decomposing to 3 CNOTs).
- **Physical Observables:**
  - Local longitudinal magnetization: $\langle Z_j(t) \rangle$
  - Total magnetization: $M_{\text{tot}}(t) = \frac{1}{N}\sum_{j=0}^{N-1} \langle Z_j(t) \rangle$
  - Spatial staggered magnetization: $M_{\text{stag}}(t) = \frac{1}{N}\sum_{j=0}^{N-1} (-1)^j \langle Z_j(t) \rangle$
- **Error Metrics:**
  - Trotter error: $\mathcal{E}_{\text{Trotter}}(m) = |\langle M(t) \rangle_{\text{ideal}}(m) - \langle M(t) \rangle_{\text{exact}}|$
  - Noise-induced error: $\mathcal{E}_{\text{noise}}(m) = |\langle M(t) \rangle_{\text{noisy}}(m) - \langle M(t) \rangle_{\text{ideal}}(m)|$
  - Total simulation error: $\mathcal{E}_{\text{total}}(m) = |\langle M(t) \rangle_{\text{noisy}}(m) - \langle M(t) \rangle_{\text{exact}}|$

---

## 5. Summary of Document Inconsistencies & Resolutions

| Dimension | Legacy Claim (Resource A/B) | Master Spec v1.2 Formulation | Resolution Status |
| :--- | :--- | :--- | :--- |
| **Physical Model** | Delta-kicked Floquet with promised time crystals | Continuous TFIM ($H = H_{ZZ} + H_X + H_Z$) under quench evolution | **Resolved & Unified** |
| **Error Curve** | Mandatory non-monotonic error turnover minimum $m^*$ | Empirical hypothesis; asymptotic convergence in ideal limit | **Resolved & Purged** |
| **Processor B SWAPs** | Claimed native 0 SWAPs for 4-spin loop | Both graphs have $\text{dist}(0,3) = 3$; SWAPs measured empirically | **Resolved & Corrected** |
| **Two-Qubit Noise** | Asserted 0.015 error rate as real hardware | Illustrative synthetic baseline $0.01$ (from starter notebook) | **Resolved & Clarified** |
