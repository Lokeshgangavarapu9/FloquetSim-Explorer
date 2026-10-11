# Processor Topology & Graph Embedding Validation Report

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 11, Subphase 3.3  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Graph Theoretical Characterization of Hardware Topologies

Using standard graph theory, the demonstration processor graphs are characterized as follows:

| Topological Dimension | Processor A (`demo_processor_A`) | Processor B (`demo_processor_B`) |
| :--- | :--- | :--- |
| **Number of Vertices ($|V|$)** | 5 qubits: $\{0, 1, 2, 3, 4\}$ | 7 qubits: $\{0, 1, 2, 3, 4, 5, 6\}$ |
| **Number of Edges ($|E|$)** | 4 edges: $\{(0,1), (1,2), (2,3), (3,4)\}$ | 7 edges: $\{(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (2,6)\}$ |
| **Graph Classification** | Linear tree / Simple Path Graph ($P_5$) | Unicyclic graph (6-node cycle $C_6$ + 1 leaf at node 2) |
| **Maximum Node Degree** | 2 (Nodes 1, 2, 3) | 3 (Node 2 is connected to 1, 3, and 6) |
| **Minimum Node Degree** | 1 (Leaf nodes 0, 4) | 1 (Leaf node 6) |
| **Graph Diameter** | 4 hops (between node 0 and node 4) | 3 hops (between any antipodal pair on the 6-cycle) |
| **Girth (Shortest Cycle)** | $\infty$ (Acyclic graph) | 6 (The 6-cycle $0-1-2-3-4-5-0$) |

---

## 2. Logical-to-Physical Qubit Mapping & Distance Analysis

For an $N=4$ spin chain with logical qubits $\{q_0, q_1, q_2, q_3\}$, the standard default layout assigns logical qubits to physical nodes $[0, 1, 2, 3]$.

```
LOGICAL INTERACTION GRAPH (4-Cycle C4):
        (q0) ──────── (q1)
          │             │
          │             │
        (q3) ──────── (q2)

PHYSICAL EMBEDDING ON PROCESSOR A (Linear Path P5):
        [q0] ─── [q1] ─── [q2] ─── [q3] ─── (4, unused)
         0        1        2        3

PHYSICAL EMBEDDING ON PROCESSOR B (Ring C6 + Branch):
        [q0] ─── [q1] ─── [q2] ─── [q3]
         0        1        2        3
         │                 │        │
        (5) ───────────── (4)      (6)
```

### 2.1 Nearest-Neighbor Interaction Terms ($Z_0 Z_1, Z_1 Z_2, Z_2 Z_3$)
- On Processor A: Edges $(0,1)$, $(1,2)$, and $(2,3)$ are direct physical edges. Physical distance = 1 hop.
- On Processor B: Edges $(0,1)$, $(1,2)$, and $(2,3)$ are direct physical edges. Physical distance = 1 hop.
- **Routing for open linear terms:** **0 SWAPs** required on both processors.

### 2.2 Boundary Periodic Term ($Z_3 Z_0$)
- On Processor A (5Q Line): The shortest path between node 0 and node 3 is $0 \to 1 \to 2 \to 3$:
  $$\text{dist}_A(0,3) = 3 \text{ hops}$$
- On Processor B (6-Node Ring): Node 0 and node 3 are exact antipodal opposite poles:
  - Path clockwise: $0 \to 1 \to 2 \to 3$ (3 hops).
  - Path counter-clockwise: $0 \to 5 \to 4 \to 3$ (3 hops).
  $$\text{dist}_B(0,3) = 3 \text{ hops}$$

---

## 3. Mathematical Verification of Acceptance Criteria

1. **Absence of 4-Cycle Subgraph ($C_4$):**  
   Neither Processor A (acyclic) nor Processor B (girth 6) contains an induced 4-cycle subgraph. It is mathematically impossible for either architecture to execute the 4-spin closed periodic Hamiltonian without routing overhead.
2. **Rejection of Zero-SWAP Assumption:**  
   The myth that Processor B achieves native 0 SWAPs for a closed loop is disproven. Both architectures have distance 3 between boundary spins. The empirical SWAP count will be measured objectively by Qiskit's Sabre router.
