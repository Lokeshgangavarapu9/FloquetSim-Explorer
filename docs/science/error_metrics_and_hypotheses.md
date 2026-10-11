# Error Metrics, Scientific Hypotheses, and Falsifiability Charter

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 10, Subphase 2.8  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Disambiguated Mathematical Error Metrics

For a chosen physical observable (staggered magnetization $M = M_{\text{stag}}(t)$ at target evolution time $t$), three mathematically distinct error quantities are defined:

1. **Algorithmic Discretization Error ($\varepsilon_{\text{Trotter}}(m)$):**
   $$\varepsilon_{\text{Trotter}}(m) = \left| M_{\text{ideal}}(m) - M_{\text{exact}} \right|$$
   - Measures pure mathematical Lie-Trotter product formula truncation error.
   - Evaluated using noiseless Qiskit Aer statevector simulation compared against the exact SciPy classical solver.
   - Theoretical bound: $\lim_{m \to \infty} \varepsilon_{\text{Trotter}}(m) = 0$ bounded asymptotically by $\mathcal{O}(t^2/m)$.

2. **Noise-Induced Hardware Error ($\varepsilon_{\text{Noise}}(m)$):**
   $$\varepsilon_{\text{Noise}}(m) = \left| M_{\text{noisy}}(m) - M_{\text{ideal}}(m) \right|$$
   - Measures pure physical error caused by gate infidelities, thermal relaxation ($T_1/T_2$), and measurement readout noise.
   - Evaluated by comparing noisy Aer simulation against noiseless Trotter statevector simulation.
   - Growth behavior: Increases monotonically with circuit depth $D(m)$ and total two-qubit gate count $N_{2Q}(m)$.

3. **Total Simulation Error ($\varepsilon_{\text{Total}}(m)$):**
   $$\varepsilon_{\text{Total}}(m) = \left| M_{\text{noisy}}(m) - M_{\text{exact}} \right|$$
   - Measures the total net deviation observed by the user on real or simulated noisy hardware.
   - Triangle inequality guarantee: $\varepsilon_{\text{Total}}(m) \le \varepsilon_{\text{Trotter}}(m) + \varepsilon_{\text{Noise}}(m)$.

---

## 2. Formal Falsifiable Scientific Hypotheses

Rather than demanding predetermined outcomes or forcing curves to exhibit specific minima, FloquetSim Explorer tests two rigorous, falsifiable scientific hypotheses:

### Hypothesis H1: Competing Error Trade-Off (Trotter Discretization vs. Noise Decay)
> **Hypothesis Statement:**  
> In the noiseless limit, increasing the Lie-Trotter step count $m$ asymptotically decreases algorithmic discretization error $\varepsilon_{\text{Trotter}}(m) \to 0$. In the presence of gate errors and decoherence, circuit depth and two-qubit gate counts scale linearly with $m$, compounding physical noise $\varepsilon_{\text{Noise}}(m)$. Depending on the ratio of commutator error magnitude to hardware gate infidelity, the total simulation error $\varepsilon_{\text{Total}}(m)$ may exhibit a non-monotonic turnover with an optimal operating point $m^* \in [1, 5]$, OR it may be dominated by noise and increase monotonically across all tested $m$.
>
> **Falsification Criteria:**  
> - H1's asymptotic convergence assertion is refuted if ideal Trotter error fails to decrease as $m$ increases toward large values.  
> - H1's trade-off assertion is supported if an interior minimum $m^*$ is observed, or partially supported if total error plateaus or increases monotonically with depth. The experiment reports empirical data objectively regardless of turnover presence.

### Hypothesis H2: Coupling Topology & Compiler Routing Overhead
> **Hypothesis Statement:**  
> When compiling an identical 4-spin closed-boundary Hamiltonian onto Processor A (5-qubit linear chain) and Processor B (7-qubit heavy-hex-inspired ring), differences in graph connectivity and diameter will induce measurable variations in transpiled circuit depth, CNOT count, and inserted SWAP overhead.
>
> **Falsification Criteria:**  
> - H2 is supported if the transpiler outputs distinct gate counts, SWAP counts, or depths between Processor A and Processor B.  
> - H2 is refuted if both architectures produce identical compiled DAGs and identical execution metrics across all transpilation runs with seed 42.

---

## 3. Removal of Curve-Forcing Constraints

- **Strict Monotonicity Purged:** It is formally prohibited to fail a test or alter simulation data because error does not decrease monotonically at every consecutive step.
- **Predetermined Minima Purged:** It is formally prohibited to force an artificial minimum $m^*$ (e.g. asserting $m^* = 3$ or $m^* = 4$) if the empirical noisy simulation produces a monotonic rise.
- All experimental reporting must present true calculated numbers from Qiskit Aer and SciPy.
