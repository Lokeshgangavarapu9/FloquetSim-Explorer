# README Draft - Part 2: Proposed Methodology & Mathematical Model

## Mathematical Model & Methodology

### 1. Interacting 1D Transverse-Field Ising Hamiltonian
The simulated physical system is a 4-spin quantum chain ($N=4$) evolving under quench dynamics with periodic boundary conditions:
$$H = H_{ZZ} + H_X + H_Z$$
where all parameters share consistent angular frequency units ($\text{rad}\cdot\text{s}^{-1}$ with $\hbar = 1$):
- **Ising Interaction:** $H_{ZZ} = J \sum_{j=0}^{2} Z_j Z_{j+1} + J Z_3 Z_0$ with $J = 1.0\,\text{rad/s}$.
- **Transverse Field & Imperfection:** $H_X = \sum_{j=0}^{3} (h_x + \delta h_x^j) X_j$ with $h_x = 1.0\,\text{rad/s}$, $\delta h_x = 0.05\,\text{rad/s}$.
- **Longitudinal Field:** $H_Z = h_z \sum_{j=0}^{3} Z_j$ with $h_z = 0.1\,\text{rad/s}$.

Because $[H_{ZZ}, H_X] \neq 0$, exact factorization is impossible, providing the authentic mathematical basis for Lie-Trotter discretization.

---

### 2. Lie-Trotter Discretization
Continuous time evolution for duration $t$ is discretized into $m$ steps with time slice $\Delta t = t/m$:
$$U_{\text{Trotter}}(m, t) = \left[ \left(\prod_{j=0}^3 e^{-i(h_x + \delta h_x^j)\Delta t X_j}\right) \left(\prod_{\langle j,k \rangle} e^{-i J_{jk}\Delta t Z_j Z_k}\right) \left(\prod_{j=0}^3 e^{-i h_z \Delta t Z_j}\right) \right]^m$$
Rotation angles in quantum gates are dimensionless radians:
$$\theta_X^j = 2(h_x + \delta h_x^j)\Delta t, \quad \theta_{ZZ}^{jk} = 2 J_{jk}\Delta t, \quad \theta_Z^j = 2 h_z \Delta t$$
Asymptotic operator error is bounded by:
$$\| U_{\text{Trotter}}(m, t) - U_{\text{exact}}(t) \| \le \frac{C t^2}{m} \quad \text{as } m \to \infty$$

---

### 3. Exact Classical Reference Solver
Ground truth expectation values are computed classically using double-precision dense matrix exponentiation via SciPy:
$$U_{\text{exact}}(t) = \text{scipy.linalg.expm}(-i H t)$$
Evaluated on the $16 \times 16$ dense Hamiltonian matrix with guaranteed unitarity deviation $< 10^{-14}$.

---

### 4. Transpilation & Compiler Routing
Circuits are synthesized to the hardware basis gate set `['rz', 'sx', 'x', 'cx']` and mapped onto target hardware coupling maps:
- **Processor A:** 5-qubit linear path ($0-1-2-3-4$, diameter 4).
- **Processor B:** 7-qubit ring with leaf ($0-1-2-3-4-5-0 + 2-6$, diameter 3, girth 6).
- **Sabre Router:** Uses `SabreLayout` and `SabreSwap` with fixed deterministic random seed `seed_transpiler=42`.
