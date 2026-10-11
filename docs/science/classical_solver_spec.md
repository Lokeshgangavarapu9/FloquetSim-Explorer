# Exact Classical Reference Solver Specification

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 10, Subphase 2.7  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Classical Reference Solver Architecture

The exact classical solver provides an unquestionable mathematical ground truth for validating Trotterized quantum circuits and isolating hardware noise degradation.

### Numerical Methodology:
- **Matrix Representation:** Dense $16 \times 16$ complex Hermitian matrix ($N=4$, $\mathcal{D} = 2^4 = 16$) constructed via NumPy Kronecker tensor products (`np.kron`).
- **Matrix Exponentiation:** High-precision matrix exponential evaluated using SciPy's Padé approximation with scaling and squaring:
  $$U_{\text{exact}}(t) = \text{scipy.linalg.expm}(-i H t)$$
- **Precision Target:** Double precision floating-point arithmetic (IEEE 754 float64 / complex128) achieving $< 10^{-14}$ numerical error.
- **Execution Budget:** Computation of $U_{\text{exact}}(t)$ for a $16 \times 16$ matrix takes $< 10$ milliseconds on a standard 2-core cloud CPU.

---

## 2. Kronecker Product Construction of $H$

Let the single-qubit Pauli matrices be:
$$I = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \quad X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \quad Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$

For an $N=4$ spin chain, the $j$-th single-qubit Pauli operator is:
$$\mathcal{O}_j = I^{\otimes j} \otimes \mathcal{O} \otimes I^{\otimes (3-j)}$$
and two-qubit operators are:
$$Z_j Z_k = \left( I^{\otimes j} \otimes Z \otimes I^{\otimes (3-j)} \right) \cdot \left( I^{\otimes k} \otimes Z \otimes I^{\otimes (3-k)} \right)$$

The total dense Hamiltonian matrix is assembled as:
$$H_{\text{dense}} = J \sum_{j=0}^2 Z_j Z_{j+1} + J Z_3 Z_0 + \sum_{j=0}^3 (h_x + \delta h_x^j) X_j + h_z \sum_{j=0}^3 Z_j$$

---

## 3. Numerical Invariant & Acceptance Checks

To ensure the classical solver is infallible, the implementation must satisfy the following checks:

1. **Hermiticity Check:**
   $$\| H_{\text{dense}} - H_{\text{dense}}^\dagger \|_{\infty} = 0.0$$
2. **Unitarity Check:**
   $$\| U_{\text{exact}}(t)^\dagger U_{\text{exact}}(t) - \mathbb{I}_{16} \|_{\infty} < 10^{-14}$$
3. **Determinant Conservation:**
   $$|\det(U_{\text{exact}}(t))| = 1.0 \pm 10^{-14}$$
4. **Statevector Norm Conservation:**
   $$\| |\psi_{\text{exact}}(t)\rangle \|_2 = \sqrt{\sum_{k=0}^{15} |\psi_k(t)|^2} = 1.0 \pm 10^{-14}$$
5. **Exact Expectation Values:**
   $$\langle Z_j(t) \rangle_{\text{exact}} = \langle \psi_{\text{exact}}(t) | Z_j | \psi_{\text{exact}}(t) \rangle \in [-1.0, +1.0]$$
   $$M_{\text{stag}}(t)_{\text{exact}} = \frac{1}{4} \sum_{j=0}^3 (-1)^j \langle Z_j(t) \rangle_{\text{exact}}$$
