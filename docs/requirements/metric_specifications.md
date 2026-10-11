# Scientific Metric Specifications & Observables Manual

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 9, Subphase 1.3  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Circuit & Compilation Metrics

These metrics characterize the structural complexity of compiled quantum circuits on specific hardware topologies:

| Metric Name | Symbol / Code Key | Mathematical / Operational Definition | Extraction Method |
| :--- | :--- | :--- | :--- |
| **Circuit Depth** | `circuit_depth` | Longest path of dependent operations in the circuit DAG. | `compiled_circuit.depth()` |
| **Total Gate Count** | `total_gates` | Total number of quantum gates in the transpiled circuit. | `sum(compiled_circuit.count_ops().values())` |
| **1-Qubit Gate Count** | `count_1q` | Number of single-qubit rotations (`rz`, `sx`, `x`). | Sum of ops with name in `['rz', 'sx', 'x']` |
| **2-Qubit Gate Count** | `count_2q` | Number of hardware-native entangling gates (`cx`, `ecr`). | Sum of ops with name in `['cx', 'ecr']` |
| **Routing SWAP Count** | `count_swap` | Explicit number of routing SWAP operations inserted by the compiler. | Sum of inserted `swap` gates, or $\frac{1}{3} \times$ routing CNOTs |
| **Active Physical Qubits**| `active_qubits` | Number of physical processor nodes occupied by the circuit layout. | `len(compiled_circuit.qubits)` |
| **Estimated Execution Time**| `execution_time_est` | $\sum t_{1Q} N_{1Q} + \sum t_{2Q} N_{2Q}$ using processor gate durations. | Calculated from processor config metadata |

---

## 2. Physical Quantum Observables

Observables are measured along the $Z$ quantization axis for an $N$-spin chain ($N=4$):

### 2.1 Local Longitudinal Magnetization ($\langle Z_j(t) \rangle$)
$$\langle Z_j(t) \rangle = \text{Tr}\left(\rho(t) Z_j\right) = \langle \psi(t) | Z_j | \psi(t) \rangle$$
- Extracted from measurement bitstrings: $\langle Z_j \rangle = \frac{N_0(j) - N_1(j)}{N_{\text{shots}}}$, where $N_0(j)$ is the count of shots where qubit $j$ was measured as $|0\rangle$ and $N_1(j)$ is the count for $|1\rangle$.
- Range: $[-1.0, +1.0]$.

### 2.2 Total Longitudinal Magnetization ($M_{\text{tot}}(t)$)
$$M_{\text{tot}}(t) = \frac{1}{N} \sum_{j=0}^{N-1} \langle Z_j(t) \rangle$$
- Represents the average net polarization of the spin chain.
- Range: $[-1.0, +1.0]$.

### 2.3 Spatial Staggered Magnetization ($M_{\text{stag}}(t)$)
$$M_{\text{stag}}(t) = \frac{1}{N} \sum_{j=0}^{N-1} (-1)^j \langle Z_j(t) \rangle$$
- Represents the antiferromagnetic order parameter along the chain.
- Range: $[-1.0, +1.0]$.
- Disambiguation Note: $M_{\text{stag}}(t)$ is a **spatial alternating sum** across qubit indices $j$, not a temporal alternating sum.

---

## 3. Disambiguated Simulation Error Metrics

To prevent confounding mathematical approximation with hardware noise, error metrics are partitioned as follows:

```
Exact Continuous Reference  ──►  <M(t)>_exact       (SciPy expm, 0 error)
         │
         │  [Lie-Trotter Commutator Discretization Error]
         ▼
Ideal Trotterized Circuit   ──►  <M(t)>_ideal(m)    (Aer Statevector, 0 noise)
         │
         │  [Physical Gate Noise & Decoherence Error]
         ▼
Noisy Hardware Simulation   ──►  <M(t)>_noisy(m)    (Aer Noisy Shots)
```

1. **Algorithmic Trotter Error ($\mathcal{E}_{\text{Trotter}}(m, t)$):**
   $$\mathcal{E}_{\text{Trotter}}(m, t) = \left| \langle M_{\text{stag}}(t) \rangle_{\text{ideal}}(m) - \langle M_{\text{stag}}(t) \rangle_{\text{exact}} \right|$$
   - Governed asymptotically by Lie-Trotter commutator theorem: $\lim_{m \to \infty} \mathcal{E}_{\text{Trotter}}(m) = 0$ bounded by $\mathcal{O}(t^2/m)$.

2. **Noise-Induced Hardware Error ($\mathcal{E}_{\text{noise}}(m, t)$):**
   $$\mathcal{E}_{\text{noise}}(m, t) = \left| \langle M_{\text{stag}}(t) \rangle_{\text{noisy}}(m) - \langle M_{\text{stag}}(t) \rangle_{\text{ideal}}(m) \right|$$
   - Accumulates with circuit depth and physical gate count: approximately scales as $\mathcal{O}(m \cdot N_{2Q} \cdot \varepsilon_{\text{gate}})$.

3. **Total Simulation Error ($\mathcal{E}_{\text{total}}(m, t)$):**
   $$\mathcal{E}_{\text{total}}(m, t) = \left| \langle M_{\text{stag}}(t) \rangle_{\text{noisy}}(m) - \langle M_{\text{stag}}(t) \rangle_{\text{exact}} \right|$$
   - Satisfies the triangle inequality: $\mathcal{E}_{\text{total}} \le \mathcal{E}_{\text{Trotter}} + \mathcal{E}_{\text{noise}}$.
   - Balances decaying Trotter error against growing hardware noise as $m$ increases.

4. **Statistical Shot Uncertainty ($\sigma_{\text{shot}}$):**
   $$\sigma_{\langle Z \rangle} = \sqrt{\frac{1 - \langle Z \rangle^2}{N_{\text{shots}}}}$$
   - For $N_{\text{shots}} = 2048$, maximum shot noise is $\approx \frac{1}{\sqrt{2048}} \approx 0.022$. All reported noisy expectation values must include $\pm \sigma_{\text{shot}}$ uncertainty bounds.
