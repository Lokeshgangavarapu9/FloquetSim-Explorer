# Formal Hamiltonian Specification & Operator Algebra

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 10, Subphase 2.2  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Unified Continuous Hamiltonian

The physical quantum system is an $N$-spin chain ($N=4$, Hilbert space $\mathcal{H} = (\mathbb{C}^2)^{\otimes 4}$, dimension $\mathcal{D} = 16$) governed by the total Hamiltonian ($\hbar = 1$):
$$H = H_{ZZ} + H_X + H_Z$$

### 1.1 Longitudinal Many-Body Interaction ($H_{ZZ}$)
$$H_{ZZ} = \sum_{j=0}^{N-2} J_{j,j+1} Z_j Z_{j+1} + J_{\text{boundary}} Z_{N-1} Z_0$$
- **Coupling Constants:** Uniform nearest-neighbor coupling $J_{j,j+1} = J = 1.0\,\text{rad}\cdot\text{s}^{-1}$.
- **Boundary Term:** $J_{\text{boundary}} = 1.0\,\text{rad}\cdot\text{s}^{-1}$ (closed periodic boundary conditions).
- **Physical Dimensionality:** Angular frequency ($\text{rad}\cdot\text{s}^{-1}$). Sets the primary entanglement timescale $\tau_J = 1/J = 1.0\,\text{s}$.
- **Pauli Matrix Representation ($N=4$):**
  $$H_{ZZ} = J (Z_0 Z_1 I_2 I_3 + I_0 Z_1 Z_2 I_3 + I_0 I_1 Z_2 Z_3 + Z_0 I_1 I_2 Z_3)$$

### 1.2 Transverse Magnetic Field & Imperfection ($H_X$)
$$H_X = \sum_{j=0}^{N-1} (h_x + \delta h_x^j) X_j$$
- **Uniform Transverse Field:** $h_x = 1.0\,\text{rad}\cdot\text{s}^{-1}$.
- **Site-Dependent Transverse Perturbation:** $\delta h_x^j = \delta h_x \cdot \cos(2\pi j / N)$ or baseline constant $\delta h_x = 0.05\,\text{rad}\cdot\text{s}^{-1}$.
- **Physical Role:** Induces coherent quantum spin flips between $|\uparrow\rangle$ ($|0\rangle$) and $|\downarrow\rangle$ ($|1\rangle$).
- **Pauli Matrix Representation ($N=4$):**
  $$H_X = \sum_{j=0}^3 (h_x + \delta h_x^j) X_j$$

### 1.3 Longitudinal Symmetry-Breaking Field ($H_Z$)
$$H_Z = \sum_{j=0}^{N-1} h_z^j Z_j$$
- **Longitudinal Field:** $h_z^j = h_z = 0.1\,\text{rad}\cdot\text{s}^{-1}$.
- **Physical Role:** Breaks spin-flip $\mathbb{Z}_2$ symmetry and lifts ground state degeneracy.
- **Pauli Matrix Representation ($N=4$):**
  $$H_Z = h_z (Z_0 I_1 I_2 I_3 + I_0 Z_1 I_2 I_3 + I_0 I_1 Z_2 I_3 + I_0 I_1 I_2 Z_3)$$

---

## 2. Operator Algebra and Dimensional Verification

1. **Hermiticity:**  
   Because all Pauli matrices are Hermitian ($X_j^\dagger = X_j, Z_j^\dagger = Z_j$) and all coefficients $J, h_x, \delta h_x, h_z \in \mathbb{R}$, each operator sub-block and the total Hamiltonian are strictly Hermitian:
   $$H_{ZZ}^\dagger = H_{ZZ}, \quad H_X^\dagger = H_X, \quad H_Z^\dagger = H_Z \implies H^\dagger = H$$
   Eigenvalues of $H$ are strictly real.

2. **Non-Commutativity (The Trotter Engine):**
   $$[Z_j Z_{j+1}, X_j] = [Z_j, X_j] Z_{j+1} = 2i Y_j Z_{j+1} \neq 0$$
   Therefore:
   $$[H_{ZZ}, H_X] \neq 0$$
   This non-zero commutator proves that the matrix exponential of the sum cannot be factored into products of exponentials without error:
   $$e^{-i (H_{ZZ} + H_X + H_Z) t} \neq e^{-i H_X t} e^{-i H_{ZZ} t} e^{-i H_Z t}$$

3. **Dimensional Consistency:**
   Every term in $H$ has units of $\text{rad}\cdot\text{s}^{-1}$. In quantum mechanics with $\hbar = 1$, the exponent in the time-evolution operator is:
   $$-i H t \quad \implies \quad [\text{rad}\cdot\text{s}^{-1}] \times [\text{s}] = \text{dimensionless radians}$$
   All quantum circuit rotation gate angles $\theta = 2 \cdot \text{coeff} \cdot \Delta t$ are dimensionally verified as pure radians.
