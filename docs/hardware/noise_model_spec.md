# Synthetic Demonstration Noise Model Specification

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 11, Subphase 3.5  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Noise Model Provenance & Disclaimer

> **EXPLICIT DISCLAIMER:**  
> The noise parameters specified herein represent **Illustrative Synthetic Demonstration Noise Models** chosen for numerical stability, reproducibility, and physical visibility in a 4-qubit simulation. They are derived from the official starter notebook illustrative examples (**DOC-3**, p. 13) and **DO NOT represent calibrated physical hardware measurements** of any live IBM Quantum cloud QPU.

---

## 2. Quantum Error Channel Formulations

The noise model in Qiskit Aer (`qiskit_aer.noise.NoiseModel`) combines three standard physical error mechanisms:

### 2.1 Single-Qubit Depolarizing Error Channel ($\mathcal{E}_{1Q}$)
Applied to all single-qubit gates (`['x', 'sx']`):
$$\mathcal{E}_{1Q}(\rho) = (1 - p_1) \rho + \frac{p_1}{3} \left( X \rho X + Y \rho Y + Z \rho Z \right)$$
- **Baseline Error Rate:** $p_1 = 0.001$ (0.1% infidelity).

### 2.2 Two-Qubit Depolarizing Error Channel ($\mathcal{E}_{2Q}$)
Applied to all two-qubit CNOT / ECR gates (`['cx']`):
$$\mathcal{E}_{2Q}(\rho) = (1 - p_2) \rho + \frac{p_2}{15} \sum_{P_1, P_2 \in \{I, X, Y, Z\} \setminus \{I \otimes I\}} (P_1 \otimes P_2) \rho (P_1 \otimes P_2)$$
- **Baseline Error Rate:** $p_2 = 0.01$ (1.0% infidelity, matching Starter Notebook p. 13).
- **Impact of SWAP Gates:** Because a SWAP gate decomposes into 3 CNOT gates, each inserted SWAP compounds the error:
  $$\mathcal{E}_{\text{SWAP}} \approx 1 - (1 - p_2)^3 \approx 3 p_2 = 0.03 \text{ (3% infidelity per SWAP)}$$

### 2.3 Thermal Relaxation & Dephasing Channel ($T_1, T_2$)
Simulates energy relaxation and phase decoherence during finite gate execution times:
- Longitudinal relaxation time: $T_1 = 100.0\,\mu\text{s}$.
- Transverse dephasing time: $T_2 = 80.0\,\mu\text{s}$.
- Physical invariant: $T_2 \le 2 T_1$ is strictly satisfied ($80\,\mu\text{s} \le 200\,\mu\text{s}$).
- Gate durations: Single-qubit $t_{1Q} = 35\,\text{ns}$; Two-qubit $t_{2Q} = 300\,\text{ns}$.

### 2.4 Measurement Readout Error Channel
Applied at measurement time to model classical bit-flip confusion:
$$\mathbf{P}_{\text{readout}} = \begin{pmatrix} P(0|0) & P(0|1) \\ P(1|0) & P(1|1) \end{pmatrix} = \begin{pmatrix} 0.99 & 0.01 \\ 0.02 & 0.98 \end{pmatrix}$$
- Symmetrized average readout error: $p_{\text{ro}} = 0.015$.

---

## 3. Parametric Noise Scaling Factor ($\lambda$)

To investigate noise resilience and test whether an error minimum $m^*$ emerges under varying hardware conditions, the noise builder supports a uniform noise scaling multiplier $\lambda \ge 0$:
$$p_1(\lambda) = \lambda \cdot p_1, \quad p_2(\lambda) = \lambda \cdot p_2$$
- $\lambda = 0.0$: Ideal noiseless simulation (pure Trotter discretization error).
- $\lambda = 1.0$: Baseline demonstration noise.
- $\lambda = 2.0$: Elevated noise regime.
