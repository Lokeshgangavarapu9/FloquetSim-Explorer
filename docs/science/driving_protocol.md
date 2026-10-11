# Dynamical Evolution Protocol & Stroboscopic Sampling

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 10, Subphase 2.3  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Continuous Time Evolution Operator

The continuous quantum state evolution under the static Transverse-Field Ising Hamiltonian $H = H_{ZZ} + H_X + H_Z$ is governed by the Schrödinger equation:
$$i \frac{d}{dt} |\psi(t)\rangle = H |\psi(t)\rangle$$

The formal solution for any duration $t \ge 0$ is given by the unitary evolution operator:
$$U_{\text{exact}}(t) = \exp(-i H t)$$

### Unitarity Verification:
Because $H$ is Hermitian ($H^\dagger = H$):
$$U_{\text{exact}}(t)^\dagger U_{\text{exact}}(t) = \exp(i H t) \exp(-i H t) = \mathbb{I}_{16}$$
$$\det(U_{\text{exact}}(t)) = \exp(-i \text{Tr}(H) t) = 1 \quad (\text{since } \text{Tr}(X) = \text{Tr}(Z) = 0 \implies \text{Tr}(H) = 0)$$
Probability norm is strictly conserved: $\langle \psi(t) | \psi(t) \rangle = \langle \psi(0) | \psi(0) \rangle = 1.0$.

---

## 2. Stroboscopic Observation Protocol

To study the dynamical behavior of the quantum spin chain, the continuous trajectory is sampled at discrete stroboscopic observation intervals $t_n$:
$$t_n = n \cdot \tau, \quad n \in \{1, 2, \dots, N_{\text{cycles}}\}$$
where:
- Stroboscopic sampling interval: $\tau = 1.0\,\text{s}$ (scaled time unit matching $1/J$).
- Observation window: $N_{\text{cycles}} = 10$ points (time horizon $t \in [1.0, 10.0]\,\text{s}$).

The exact state at each stroboscopic step $n$ is:
$$|\psi_{\text{exact}}(n)\rangle = \left[ U_{\text{exact}}(\tau) \right]^n |\psi(0)\rangle = U_{\text{exact}}(n\tau) |\psi(0)\rangle$$

---

## 3. Relation to Lie-Trotter Approximation

When implementing this evolution on a digital quantum computer:
- For any target observation time $t$, the evolution is divided into $m$ Lie-Trotter discretization steps, each of duration $\Delta t = t / m$.
- The quantum circuit synthesizes:
  $$U_{\text{Trotter}}(m, t) = \left[ U_{\text{step}}(\Delta t) \right]^m$$
- As $m \to \infty$, $U_{\text{Trotter}}(m, t) \to U_{\text{exact}}(t)$.
- The core experimental study evaluates how the observable expectation value $\langle Z_0(t_n) \rangle$ behaves under varying Trotter steps $m \in \{1, 2, 3, 4, 5\}$ in the presence of hardware noise.
