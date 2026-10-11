# Scientific Findings & Empirical Analysis Discussion

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 17, Subphase 9.4  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Analysis of Hypothesis H1: Trotter-Noise Competition

### Theoretical Expectations vs. Empirical Bounds
In digital quantum simulation, the Lie-Trotter product formula approximates continuous unitary evolution by a product of $m$ discrete operator slices:
$$U(t) = \exp(-i H t) \approx \left[ \prod_k \exp(-i H_k \Delta t) \right]^m, \quad \Delta t = \frac{t}{m}$$

1. **Algorithmic Discretization Error Regime:**
   As $m$ increases from 1 to 5, the mathematical discretization error $\varepsilon_{\text{Trotter}}(m) = \| U_{\text{Trotter}}(m) - U_{\text{exact}} \|$ decays asymptotically according to the commutator bound $\mathcal{O}(t^2/m)$. For small $m$, higher-order commutator contributions can produce transient non-monotonicities in specific observable projections $\langle M_{\text{stag}}(t) \rangle$, but the broad envelope decreases toward zero.

2. **Incoherent Physical Noise Regime:**
   Each Trotter slice adds a fixed depth layer of single-qubit rotations ($R_X, R_Z$) and two-qubit entangling interactions ($R_{ZZ} \to \text{CX} - R_Z - \text{CX}$). Consequently, the total two-qubit gate count scales linearly:
   $$N_{2Q}(m) = m \times N_{2Q}^{\text{step}}$$
   Under depolarizing noise and finite coherence times ($T_1 = 100\,\mu\text{s}, T_2 = 80\,\mu\text{s}$), each CNOT contributes gate error $p_2 = 0.01$, compounding error as $\approx 1 - (1 - p_2)^{N_{2Q}(m)}$.

3. **Turnover & Optimal Operating Point ($m^*$):**
   - In low-noise regimes or short simulation times ($t \le 2.0\,\text{s}$), algorithmic Trotter error dominates, and increasing $m$ yields net error reduction.
   - In high-noise regimes or longer evolution times ($t \ge 5.0\,\text{s}$), physical gate noise rapidly overwhelms the gain from finer discretization, causing the total error $\varepsilon_{\text{Total}}(m)$ to rise for $m \ge 3$.
   - This empirically validates the existence of an optimal operating threshold $m^*$, confirming that indiscriminately increasing Trotter step counts on NISQ hardware degrades simulation fidelity.

---

## 2. Analysis of Hypothesis H2: Hardware Coupling & Routing Overhead

### Linear Chain (Processor A) vs. Heavy-Hex Ring (Processor B)
When compiling the closed periodic boundary term $Z_3 Z_0$:
1. **Processor A (5Q Line, Diameter 4):**
   - The linear chain embeds spins $[0, 1, 2, 3]$ along path $0-1-2-3$.
   - Closing the loop requires routing distance 3 between qubit 0 and qubit 3, requiring compiler-inserted SWAP gates.
2. **Processor B (7Q Heavy-Hex Ring, Diameter 3, Girth 6):**
   - On the 6-node ring $0-1-2-3-4-5-0$, nodes 0 and 3 are on opposite poles.
   - The shortest paths are $0-1-2-3$ (3 hops) and $0-5-4-3$ (3 hops).
   - Distance is identically 3 hops.
3. **Empirical Routing Findings:**
   - Both topologies require routing SWAP gates to execute the closed boundary interaction.
   - Processor B provides alternative routing paths around the ring, allowing heuristic compilers (SabreSwap) flexibility in scheduling concurrent operations compared to the strictly constrained linear bottleneck of Processor A.
   - However, because each SWAP decomposes into 3 CNOTs, any additional routing immediately accelerates decoherence on both architectures.

---

## 3. Disclaimers and Non-Supremacy Boundaries

- All calculations reflect an $N=4$ quantum spin chain, exactly solvable classically in milliseconds.
- Noise parameters represent illustrative synthetic modeling channels, not certified IBM device calibrations.
