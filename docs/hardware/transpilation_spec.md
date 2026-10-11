# Transpilation Pipeline & Deterministic Seeding Specification

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 11, Subphase 3.4  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Transpilation Pass Architecture

In Qiskit 1.x, mapping abstract quantum spin circuits onto physical coupling topologies requires systematic transpilation passes managing layout, routing, translation, and optimization:

```
[Abstract Parameterized Circuit (RZZ, RX, RZ)]
                        │
                        ▼
            [1. Initial Layout Selection]
        SabreLayout (heuristic) with fixed seed=42
                        │
                        ▼
            [2. Routing / SWAP Insertion]
         SabreSwap with fixed seed_transpiler=42
                        │
                        ▼
            [3. Basis Gate Decomposition]
         Decompose RZZ(θ) -> CX - RZ(θ) - CX
         Decompose to native basis ['rz', 'sx', 'x', 'cx']
                        │
                        ▼
            [4. Gate Optimization Passes]
         Optimization Level 1 (Deterministic Baseline)
                        │
                        ▼
       [Hardware-Compliant Physical QuantumCircuit]
```

---

## 2. Deterministic Seeding Policy

Because the Sabre routing algorithm relies on stochastic heuristic search across lookahead layers, unseeded compilation causes random fluctuations in circuit depth and SWAP counts across runs.

To guarantee bit-for-bit reproducible benchmarks:
- **Mandatory Seed Parameter:** `seed_transpiler = 42` must be explicitly passed to all `qiskit.transpile()` calls.
- **PassManager Seeding:** Both `SabreLayout(seed=42)` and `SabreSwap(seed=42)` must receive the exact seed.
- **Zero Variance Invariant:** Transpiling an identical input circuit 10 consecutive times with seed 42 must produce:
  $$\text{Var}(\text{circuit\_depth}) = 0.0, \quad \text{Var}(N_{2Q}) = 0.0, \quad \text{Var}(N_{\text{SWAP}}) = 0.0$$

---

## 3. Basis Gate Translation & Rule Mapping

All Hamiltonian interaction layers are translated into the hardware basis gate set `['rz', 'sx', 'x', 'cx']`:

1. **Single-Qubit $R_X(\theta)$:**
   Decomposes natively into:
   $$R_X(\theta) = R_Z(\pi/2) \cdot \sqrt{X} \cdot R_Z(\theta + \pi) \cdot \sqrt{X} \cdot R_Z(3\pi/2)$$
   or is natively supported by hardware drivers.
2. **Single-Qubit $R_Z(\theta)$:**
   Implemented as a virtual $Z$-gate (frame change) with duration $t = 0\,\text{ns}$ and zero gate error on superconducting hardware.
3. **Two-Qubit $R_{ZZ}(\theta)$:**
   Decomposes into two CNOT gates and one $R_Z$ rotation:
   $$R_{ZZ}(\theta)_{j,k} = \text{CX}(j, k) \to R_Z(\theta)_k \to \text{CX}(j, k)$$
4. **Routing SWAP:**
   Decomposes into three alternating CNOT gates:
   $$\text{SWAP}(j, k) = \text{CX}(j, k) \cdot \text{CX}(k, j) \cdot \text{CX}(j, k)$$
   Each inserted SWAP gate adds exactly 3 two-qubit operations and increases circuit depth by 3 layers.
