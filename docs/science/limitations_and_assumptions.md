# Scientific Assumptions, Limitations & Non-Supremacy Register

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 21, Subphase 13.5  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Physical Model Approximations

1. **System Size Limitation ($N=4$ Spins):**  
   The simulation evaluates an open or closed 1D chain of 4 quantum spins. The Hilbert space dimension is $2^4 = 16$. This allows double-precision classical verification via SciPy matrix exponentiation, but does not simulate macroscopic thermodynamic-limit phenomena.
2. **First-Order Lie-Trotter Approximation:**  
   The quantum circuits implement the first-order product formula $U_{\text{Trotter}} = (e^{-i H_X dt} e^{-i H_{ZZ} dt} e^{-i H_Z dt})^m$. Higher-order symmetric Suzuki formulas ($S_2, S_4$) are deferred to future work.
3. **Quench Precession vs. Discrete Time Crystals:**  
   The primary physical dynamics are framed as quench and precession dynamics under a continuous TFIM. Period-doubling discrete time-crystalline (DTC) behavior is strictly treated as an optional exploratory study under pulsed driving conditions, avoiding ungrounded physics claims.

---

## 2. Hardware Modeling Assumptions

1. **Provisional Demonstration Topologies:**  
   Because official organizer files (`processor_A.json`, `processor_B.json`) were missing from the public kit, benchmarks run on `demo_processor_A.json` (5-qubit line) and `demo_processor_B.json` (7-qubit heavy-hex ring). These demonstrate the compiler pipeline but do not represent physical IBM Quantum hardware calibrations.
2. **Synthetic Depolarizing Noise Channel:**  
   The noise model simulates uniform single-qubit ($p_1 = 0.001$) and two-qubit ($p_2 = 0.01$) depolarizing channels, thermal relaxation ($T_1=100\,\mu\text{s}, T_2=80\,\mu\text{s}$), and measurement confusion ($p_{\text{ro}} = 0.015$). Real superconducting quantum processors exhibit non-Markovian 1/f noise, spectator crosstalk, and daily calibration drifts that are not captured in this model.

---

## 3. Computational Boundary (No Quantum Supremacy Claimed)

The entire $16 \times 16$ system is solved classically in milliseconds. The value of this project lies in **compiler benchmarking, routing overhead characterization, and pedagogical NISQ exploration**, not in claiming quantum computational advantage over classical supercomputers.
