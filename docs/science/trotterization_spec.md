# Lie-Trotter Product Formula & Discretization Specification

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 10, Subphase 2.5  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Lie-Trotter Product Formula Decomposition

To execute the time-evolution operator $U(t) = \exp(-i H t)$ of the continuous Hamiltonian $H = H_{ZZ} + H_X + H_Z$ on a gate-based quantum processor, the total duration $t$ is discretized into $m$ Trotter steps of duration:
$$\Delta t = \frac{t}{m}$$

Using the first-order Lie-Trotter product formula, the discrete unitary $U_{\text{Trotter}}(m, t)$ is synthesized as:
$$U_{\text{Trotter}}(m, t) = \left[ U_{\text{step}}(\Delta t) \right]^m$$
where each Trotter slice $U_{\text{step}}(\Delta t)$ is composed of three mutually non-interfering sub-layers:
$$U_{\text{step}}(\Delta t) = \left( \prod_{j=0}^{N-1} e^{-i (h_x + \delta h_x^j)\Delta t X_j} \right) \left( \prod_{\langle j,k \rangle} e^{-i J_{jk} \Delta t Z_j Z_k} \right) \left( \prod_{j=0}^{N-1} e^{-i h_z^j \Delta t Z_j} \right)$$

---

## 2. Quantum Gate Syntheses & Dimensionless Angles

In Qiskit, standard rotation gates $R_X(\theta)$, $R_Z(\theta)$, and $R_{ZZ}(\theta)$ are defined with a factor of $1/2$ in the generator exponent:
$$R_X(\theta) = \exp\left(-i \frac{\theta}{2} X\right), \quad R_Z(\theta) = \exp\left(-i \frac{\theta}{2} Z\right), \quad R_{ZZ}(\theta) = \exp\left(-i \frac{\theta}{2} Z \otimes Z\right)$$

To reproduce the Hamiltonian unitary terms $\exp(-i \text{coeff} \cdot \Delta t \cdot \mathcal{O})$, the gate rotation angles must be defined with an explicit factor of 2:

| Hamiltonian Term | Quantum Gate Mapping | Dimensionless Rotation Angle ($\theta \in \mathbb{R}$) |
| :--- | :--- | :--- |
| **Transverse Kick Term** $\exp(-i (h_x + \delta h_x^j)\Delta t X_j)$ | Single-qubit $R_X$ gate on qubit $j$ | $\theta_X^j = 2 (h_x + \delta h_x^j) \Delta t$ |
| **Ising Interaction Term** $\exp(-i J_{jk} \Delta t Z_j Z_k)$ | Two-qubit $R_{ZZ}$ gate on pair $(j, k)$ | $\theta_{ZZ}^{jk} = 2 J_{jk} \Delta t$ |
| **Longitudinal Term** $\exp(-i h_z^j \Delta t Z_j)$ | Single-qubit $R_Z$ gate on qubit $j$ | $\theta_Z^j = 2 h_z^j \Delta t$ |

### Basis Gate Decomposition of $R_{ZZ}(\theta)$

On physical architectures whose basis gate set is `['rz', 'sx', 'x', 'cx']`, each two-qubit $R_{ZZ}(\theta)$ interaction is decomposed natively into:
$$R_{ZZ}(\theta)_{j,k} = \text{CX}(j, k) \cdot R_Z(\theta)_k \cdot \text{CX}(j, k)$$
This introduces exactly two native CNOT gates per interacting spin pair per Trotter step.

---

## 3. Theoretical Asymptotic Error Bounds

By the Baker-Campbell-Hausdorff (BCH) formula, the operator approximation error for the first-order Lie-Trotter product formula is governed by:
$$U_{\text{exact}}(t) - U_{\text{Trotter}}(m, t) = \frac{t^2}{2m} \sum_{A, B \in \{H_X, H_{ZZ}, H_Z\}} [A, B] + \mathcal{O}\left(\frac{t^3}{m^2}\right)$$

In operator norm, this establishes the rigorous asymptotic bound:
$$\| U_{\text{Trotter}}(m, t) - U_{\text{exact}}(t) \| \le \frac{C t^2}{m} \quad \text{as } m \to \infty$$
where $C = \frac{1}{2} \| [H_X, H_{ZZ}] \| + \frac{1}{2} \| [H_X, H_Z] \|$.

### Removal of Monotonicity Constraints

- **Asymptotic Limit:** In the noiseless limit as $m \to \infty$, the simulation converges asymptotically to the exact unitary limit.
- **Finite-Step Fluctuations:** For finite, small Trotter steps ($m \in [1, 5]$) and localized observables $\langle Z_0(t) \rangle$, the error curve is **not required to decrease monotonically** at every consecutive integer step. Destructive phase interference between non-commuting terms can produce non-monotonic ripples before reaching the asymptotic $1/m$ envelope.
- Demanding strict per-step monotonic decrease is scientifically invalid and is formally rejected as an acceptance criterion.
