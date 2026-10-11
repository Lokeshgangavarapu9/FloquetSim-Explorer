# Initial State, Boundary Conditions, and Graph Distance Analysis

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 10, Subphase 2.4  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Initial Quantum State Selection

The quantum spin chain simulation supports two standard, easily preparable initial product states:

1. **Ferromagnetic Polarized State ($|0000\rangle$ — Default Baseline):**
   $$|\psi(0)\rangle = |0\rangle^{\otimes 4} = |0000\rangle$$
   - Preparation: Natural ground state of standard quantum registers with zero gate overhead ($I^{\otimes 4}$).
   - Observable Signature: Initial local magnetization $\langle Z_j(0) \rangle = +1.0$ for all $j \in \{0, 1, 2, 3\}$. Total magnetization $M_{\text{tot}}(0) = +1.0$.

2. **Antiferromagnetic Néel State ($|0101\rangle$ — Staggered Baseline):**
   $$|\psi(0)\rangle = |0101\rangle = X_1 X_3 |0000\rangle$$
   - Preparation: Requires two single-qubit $X$ gates applied to qubits 1 and 3.
   - Observable Signature: Initial staggered magnetization $M_{\text{stag}}(0) = \frac{1}{4}(1 - (-1) + 1 - (-1)) = +1.0$.

---

## 2. Spatial Boundary Conditions: Closed Periodic Chain

To ensure an active topological testbed that forces quantum compilers to resolve routing constraints, the 4-spin chain is configured with **closed periodic boundary conditions**:
$$H_{ZZ} = J \left( Z_0 Z_1 + Z_1 Z_2 + Z_2 Z_3 + Z_3 Z_0 \right)$$
where $J_{\text{boundary}} = J = 1.0\,\text{rad/s}$.

The interaction graph of this physical model is a **4-cycle ($C_4$)** with edges:
$$E_{\text{model}} = \{(0,1), (1,2), (2,3), (3,0)\}$$

---

## 3. Rigorous Graph Distance Analysis on Hardware Coupling Maps

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

### 3.1 Processor A (5-Qubit Line)

- Physical Qubits: $\{0, 1, 2, 3, 4\}$.
- Physical Edges: `{(0,1), (1,2), (2,3), (3,4)}`.
- Logical mapping: $q_0 \to 0, q_1 \to 1, q_2 \to 2, q_3 \to 3$.
- Linear edges $(0,1), (1,2), (2,3)$ are native physical edges ($\text{dist}_A = 1$).
- **Boundary edge $(3,0)$:** The shortest path between physical nodes 0 and 3 on the line is $0-1-2-3$, which has length:
  $$\text{dist}_A(0,3) = 3 \text{ hops}$$
- Processor A does not have a closed loop. Compiling the $Z_3 Z_0$ term requires routing SWAP gates.

### 3.2 Processor B (7-Qubit Ring + Branch)

- Physical Qubits: $\{0, 1, 2, 3, 4, 5, 6\}$.
- Physical Edges: `{(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (2,6)}`.
- Cycle length (girth): $g = 6$ (a 6-node ring).
- Logical mapping on ring: $q_0 \to 0, q_1 \to 1, q_2 \to 2, q_3 \to 3$.
- Linear edges $(0,1), (1,2), (2,3)$ are native physical edges ($\text{dist}_B = 1$).
- **Boundary edge $(3,0)$:** On a 6-node ring, node 0 and node 3 are exact **antipodes**:
  - Clockwise path: $0 \to 1 \to 2 \to 3$ (3 hops).
  - Counter-clockwise path: $0 \to 5 \to 4 \to 3$ (3 hops).
  - Thus:
  $$\text{dist}_B(0,3) = 3 \text{ hops}$$
- Processor B contains a 6-cycle, **NOT a 4-cycle**. There is no direct physical edge between node 0 and node 3.

---

## 4. Key Scientific Conclusion on Routing Overhead

1. **Neither processor natively embeds a 4-cycle ($C_4$) with 0 SWAPs.**
2. Both architectures require quantum routing to execute the boundary interaction $Z_3 Z_0$.
3. The empirical SWAP overhead depends on compiler layout, routing heuristics (SabreSwap), and whether the compiler utilizes the alternative path ($0-5-4-3$) on Processor B.
4. **Zero-SWAP claims are formally rejected.** All routing metrics must be extracted empirically from Qiskit transpilation passes.
