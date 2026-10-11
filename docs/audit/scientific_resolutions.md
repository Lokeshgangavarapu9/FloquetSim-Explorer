# Scientific Contradiction Audit & Resolution Memo

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 8, Subphase 0.4  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Resolution of Hamiltonian Perturbation Classification

### 1.1 The Contradiction in Early Drafts
In early conceptual drafts (Resource A, p. 7; Resource B, p. 3), the Hamiltonian kick term was ambiguously written as $(g X_j + \varepsilon X_j)$ or confused with longitudinal field components $h_j^z Z_j$. This presented two serious scientific flaws:
1. **Algebraic Identity:** $g X_j + \varepsilon X_j = (g + \varepsilon) X_j$. Since $X_j$ commutes with itself, adding a scalar multiple of $X_j$ to another scalar multiple of $X_j$ merely changes the global rotation angle; it introduces no non-commuting dynamics.
2. **Axis Confusion:** Conflating transverse perturbations with longitudinal fields violates the physical distinction between transverse driving (inducing spin flips) and longitudinal fields (inducing site-dependent phase shifts and breaking $\mathbb{Z}_2$ symmetry).

### 1.2 Unified, Dimensionally Sound Resolution
In Master Specification v1.2 (Sections 4 & 10), the physical model is rigorously partitioned into three distinct, non-commuting Hermitian operator sets with uniform angular frequency units ($\text{rad/s}$, $\hbar = 1$):

1. **Many-Body Longitudinal Interaction ($H_{ZZ}$):**
   $$H_{ZZ} = \sum_{j=0}^{N-2} J_{j,j+1} Z_j Z_{j+1} + J_{\text{boundary}} Z_{N-1} Z_0$$
   - Units: $J \in \text{rad}\cdot\text{s}^{-1}$ (baseline $J = 1.0\,\text{rad/s}$).
   - Role: Generates many-body quantum entanglement along the $Z$ quantization axis.

2. **Transverse Field and Imperfection ($H_X$):**
   $$H_X = \sum_{j=0}^{N-1} (h_x + \delta h_x^j) X_j$$
   - Units: $h_x, \delta h_x^j \in \text{rad}\cdot\text{s}^{-1}$ (baseline $h_x = 1.0\,\text{rad/s}$, $\delta h_x = 0.05\,\text{rad/s}$).
   - Role: Induces transverse spin precession. $\delta h_x^j$ is strictly a **transverse field imperfection/disorder**, operating on the $X$ axis.

3. **Longitudinal Field ($H_Z$):**
   $$H_Z = \sum_{j=0}^{N-1} h_z^j Z_j$$
   - Units: $h_z^j \in \text{rad}\cdot\text{s}^{-1}$ (baseline $h_z = 0.1\,\text{rad/s}$).
   - Role: Breaks spin-flip $\mathbb{Z}_2$ symmetry and integrability along the longitudinal axis.

4. **Commutation Algebra:**
   $$[H_X, H_{ZZ}] \neq 0, \quad [H_X, H_Z] \neq 0, \quad [H_{ZZ}, H_Z] = 0$$
   Because $[H_X, H_{ZZ}] \neq 0$, the time-evolution operator $\exp(-i (H_{ZZ} + H_X + H_Z) t)$ cannot be factored without discretization error, providing the authentic mathematical basis for Lie-Trotter approximation studies.

---

## 2. Graph Distance & Boundary Routing Audit

### 2.1 The 4-Cycle Myth Refuted
Early blueprints claimed that Processor B embeds a 4-spin loop "natively with 0 SWAPs." This statement has been mathematically refuted by graph analysis:

| Property | Processor A (5-Qubit Line) | Processor B (7-Qubit Heavy-Hex-Inspired) |
| :--- | :--- | :--- |
| **Coupling Graph Edges** | `[[0,1], [1,2], [2,3], [3,4]]` | `[[0,1], [1,2], [2,3], [3,4], [4,5], [5,0], [2,6]]` |
| **Graph Type** | Acyclic path graph $P_5$ | 6-cycle ring $C_6$ plus 1 external leaf at node 2 |
| **Girth (Shortest Cycle)** | $\infty$ (No cycles exist) | 6 (The cycle has length 6) |
| **Contains 4-Cycle Subgraph ($C_4$)?** | **NO** | **NO** |
| **Distance for Linear Edges $(0,1), (1,2), (2,3)$** | $\text{dist}_A = 1$ (native edges) | $\text{dist}_B = 1$ (native edges) |
| **Distance for Boundary Edge $(3,0)$** | $\text{dist}_A(0,3) = 3$ hops ($0-1-2-3$) | $\text{dist}_B(0,3) = 3$ hops ($0-1-2-3$ or $0-5-4-3$) |

### 2.2 Mathematical Conclusion on Routing
On the 6-node cycle of Processor B, nodes 0 and 3 are exact **antipodal opposite poles**. The shortest path in either direction around the ring requires exactly 3 hops.  
Therefore:
$$\text{dist}_A(0,3) = 3 \quad \text{and} \quad \text{dist}_B(0,3) = 3$$
Neither graph contains a direct edge between node 0 and node 3. When simulating closed periodic boundary conditions ($Z_3 Z_0$), **both processors must insert routing operations**. The exact SWAP overhead must be measured empirically using Qiskit's Sabre router without asserting predetermined zero-SWAP outcomes.

---

## 3. Discretization Error & Asymptotic Convergence

### 3.1 Purge of Monotonic Error Constraints
Previous drafts demanded that error decrease monotonically at every individual Trotter step $m \in [1, 5]$. This has been purged:
- **Theoretical Reality:** The Baker-Campbell-Hausdorff (BCH) expansion guarantees an overall asymptotic bound on operator error:
  $$\| U_{\text{Trotter}}(m, t) - U_{\text{exact}}(t) \| \le \frac{C t^2}{m} \quad \text{as } m \to \infty$$
- However, for small finite $m$ and specific projection onto expectation values $\langle Z(t) \rangle$, observable errors can oscillate due to coherent interference before entering the asymptotic $1/m$ scaling regime.
- Furthermore, under gate noise, physical decoherence accumulates linearly with circuit depth. The total error curve $\mathcal{E}_{\text{total}}(m)$ represents an empirical balance to be measured, not forced.

---

## 4. Audit Sign-off

- **Perturbation Classification:** Verified (Transverse $X$ vs Longitudinal $Z$).
- **Graph Distances:** Proven ($\text{dist}(0,3) = 3$ on both graphs).
- **Monotonicity Constraints:** Purged and replaced with asymptotic bounds.
