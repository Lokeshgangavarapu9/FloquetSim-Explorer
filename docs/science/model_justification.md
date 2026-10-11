# Physical Model Justification: Interacting Transverse-Field Ising Spin Chain

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 10, Subphase 2.1  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Selection of Physical Model

The core quantum simulation model selected for Track S3 is an **interacting 1D Transverse-Field Ising Model (TFIM)** with $N=4$ quantum spins undergoing dynamical quench evolution:
$$H = H_{ZZ} + H_X + H_Z$$

### Why the Interacting TFIM is the Optimal Choice:
1. **Genuine Many-Body Entanglement:** Unlike non-interacting single-qubit precessions, the nearest-neighbor $Z_j Z_{j+1}$ coupling generates non-trivial many-body quantum correlations across the chain.
2. **Authentic Lie-Trotter Commutator Error:** The transverse driving term $H_X = \sum_j (h_x + \delta h_x^j) X_j$ does not commute with the interaction term $H_{ZZ} = \sum_j J Z_j Z_{j+1}$ ($[H_X, H_{ZZ}] \neq 0$). This non-commutativity directly necessitates Lie-Trotter product formula approximations and guarantees non-zero algorithmic Trotter discretization error.
3. **Non-Integrability & Realism:** The inclusion of longitudinal fields $h_z \sum_j Z_j$ and site-dependent transverse perturbations $\delta h_x^j$ breaks pure spin-flip $\mathbb{Z}_2$ symmetry and integrability, modeling realistic experimental quantum spin simulators.
4. **Exact Classical Solvability for Benchmarking:** For $N=4$ spins, the Hilbert space dimension is $2^4 = 16$. The exact continuous time-evolution operator $U(t) = \exp(-i H t)$ can be computed to double machine precision ($< 10^{-14}$) via SciPy dense matrix exponentiation in $< 10$ milliseconds. This provides an unambiguous ground truth to measure simulation accuracy.

---

## 2. Reframing from Floquet Time Crystals to Dynamical Quenches

Early exploratory planning documents (Resource A & B) ambiguously claimed to demonstrate "discrete time-crystalline (DTC) period doubling" while writing continuous static Hamiltonian exponentials. In v1.2, this formulation is scientifically rectified:
- **Primary Scientific Framework:** The primary simulation is framed as **dynamical quench and precession dynamics** of an interacting quantum spin chain under Trotterized time evolution.
- **Why This Is Defensible:** Genuine discrete time-crystalline order requires stroboscopic pulsed driving with strong disorder-induced many-body localization (MBL) or prethermalization over long times ($T \gg 20$). Claiming true DTC order on an unlocalized 4-qubit system without disordered longitudinal fields would be physically ungrounded.
- **Exploratory Status:** Fourier spectral peak analysis is preserved strictly as an **optional exploratory study** under pulsed drive conditions, avoiding unverified claims in the main benchmark.
