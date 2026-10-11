# Observable Specifications & Measurement Estimators

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 10, Subphase 2.6  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Physical Observables Definitions

All physical quantities measured in the FloquetSim Explorer quantum spin simulation are Hermitian observables acting along the longitudinal ($Z$) quantization axis:

### 1.1 Local Longitudinal Magnetization ($\langle Z_j \rangle$)
$$\langle Z_j \rangle = \text{Tr}\left( \rho Z_j \right)$$
- Evaluates the individual spin polarization of qubit $j \in \{0, 1, 2, 3\}$.
- Eigenvalues: $+1$ (spin up, $|0\rangle$) and $-1$ (spin down, $|1\rangle$).
- Bounds: $\langle Z_j \rangle \in [-1.0, +1.0]$.

### 1.2 Total Magnetization ($M_{\text{tot}}$)
$$M_{\text{tot}} = \frac{1}{N} \sum_{j=0}^{N-1} \langle Z_j \rangle$$
- Evaluates the global spatial magnetization of the entire spin chain.
- Bounds: $M_{\text{tot}} \in [-1.0, +1.0]$.

### 1.3 Spatial Staggered Magnetization ($M_{\text{stag}}$)
$$M_{\text{stag}} = \frac{1}{N} \sum_{j=0}^{N-1} (-1)^j \langle Z_j \rangle$$
- Evaluates the antiferromagnetic spatial ordering across neighboring spins:
  $$M_{\text{stag}} = \frac{1}{4} \left( \langle Z_0 \rangle - \langle Z_1 \rangle + \langle Z_2 \rangle - \langle Z_3 \rangle \right)$$
- Bounds: $M_{\text{stag}} \in [-1.0, +1.0]$.
- **Critical Distinction:** $M_{\text{stag}}$ alternates over **spatial spin index $j$**, NOT temporal observation steps $n$.

---

## 2. Extraction from Measurement Bitstrings

For execution on shot-based quantum backends (Qiskit Aer with $N_{\text{shots}} = 2048$):

1. **Bitstring Measurement Conventions:**  
   Qiskit measurement bitstrings are indexed from right to left (little-endian: bit $0$ is the rightmost character). For a bitstring $b = b_{N-1} \dots b_1 b_0$ observed with count $C(b)$:
   $$s_j(b) = \begin{cases} +1 & \text{if } b_j = \text{'0'} \\ -1 & \text{if } b_j = \text{'1'} \end{cases}$$

2. **Expectation Value Estimators:**
   $$\langle Z_j \rangle = \frac{1}{N_{\text{shots}}} \sum_{b} C(b) \cdot s_j(b) = \frac{N_{\text{shots}}^{(0)}(j) - N_{\text{shots}}^{(1)}(j)}{N_{\text{shots}}}$$
   $$M_{\text{tot}} = \frac{1}{N} \sum_{j=0}^{N-1} \langle Z_j \rangle, \quad M_{\text{stag}} = \frac{1}{N} \sum_{j=0}^{N-1} (-1)^j \langle Z_j \rangle$$

3. **Statevector Exact Inner Product:**
   When running noiseless statevector simulation with state $|\psi\rangle \in \mathbb{C}^{16}$:
   $$\langle Z_j \rangle = \langle \psi | Z_j | \psi \rangle = \psi^\dagger \left( I^{\otimes j} \otimes Z \otimes I^{\otimes (N-1-j)} \right) \psi$$

---

## 3. Temporal Trajectories and Exploratory Spectral Analysis

1. **Stroboscopic Trajectories:**  
   Measurements are recorded at discrete time points $t_n = n \cdot \tau$ for $n = 1, \dots, 10$, generating time-series vectors:
   $$\vec{M}_{\text{tot}} = [M_{\text{tot}}(t_1), M_{\text{tot}}(t_2), \dots, M_{\text{tot}}(t_{10})]$$
   $$\vec{M}_{\text{stag}} = [M_{\text{stag}}(t_1), M_{\text{stag}}(t_2), \dots, M_{\text{stag}}(t_{10})]$$

2. **Exploratory Discrete Fourier Transform (DFT):**  
   To inspect frequency content without ungrounded time-crystal assertions, the standard discrete power spectrum is defined as:
   $$S(\omega) = \frac{1}{N_{\text{points}}} \left| \sum_{k=1}^{N_{\text{points}}} M_{\text{stag}}(t_k) e^{-i \omega t_k} \right|^2$$
   This is classified strictly as an **optional exploratory enhancement**. It is not required for the core Phase 1 submission.
