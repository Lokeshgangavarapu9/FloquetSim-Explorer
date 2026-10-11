# Full Factorial Experiment Matrix & Runtime Budget

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 11, Subphase 3.6  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Experimental Parameter Space

To systematically test Hypotheses H1 (Trotter-Noise trade-off) and H2 (Topological SWAP overhead), the experimental matrix executes a full factorial grid crossing hardware topologies, discretization steps, and simulation modes:

| Dimension | Parameter Name | Discrete Values Evaluated | Dimension Count |
| :--- | :--- | :--- | :--- |
| **Processors** | `processor_id` | `demo_processor_A` (5Q line), `demo_processor_B` (7Q ring) | 2 architectures |
| **Trotter Steps** | `trotter_steps` ($m$) | $m \in \{1, 2, 3, 4, 5\}$ steps per unit interval | 5 discretization levels |
| **Evolution Times** | `total_time` ($t_n$) | $t_n \in \{1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0\}\,\text{s}$ | 10 stroboscopic points |
| **Simulation Modes** | `simulation_mode` | `ideal_statevector` (ground truth comparison), `ideal_shots`, `noisy_shots` | 3 execution modes |
| **Measurement Shots**| `shots` | $N_{\text{shots}} = 2048$ (fixed seed 42) | 1 statistical sample size |

---

## 2. Computational Run Budget & Cloud Feasibility

### Point Counts:
1. **Trotter Discretization Sweep (Fixed Time $t=5.0\,\text{s}$):**
   - 2 processors $\times$ 5 Trotter steps ($m \in [1..5]$) $\times$ 3 simulation modes = **30 circuit evaluations**.
2. **Dynamical Time Evolution Sweep (Fixed $m=3$ Steps):**
   - 2 processors $\times$ 10 time points ($t \in [1..10]$) $\times$ 3 simulation modes = **60 circuit evaluations**.
3. **Exact Classical Baseline (SciPy `expm`):**
   - 10 matrix exponentiations on $16 \times 16$ dense Hamiltonian matrix = **10 matrix solves**.
4. **Total Core Simulation Runs:** **100 circuit executions**.

### Execution Time Budget:
- Exact SciPy solve (10 points): $\approx 0.05\,\text{s}$
- Ideal Statevector simulation (50 circuits): $\approx 0.8\,\text{s}$
- Shot-based simulation (50 ideal + 50 noisy @ 2048 shots): $\approx 12.0\,\text{s}$
- Transpilation passes with Sabre (50 circuits): $\approx 3.5\,\text{s}$
- Matplotlib figure rendering (4 figures @ 300 DPI): $\approx 4.0\,\text{s}$
- **Total Headless Execution Duration:** $\mathbf{\approx 20.5\,\text{s}}$

**Conclusion:** The entire experimental benchmark completes in approximately 21 seconds on a standard 2-core cloud VM, easily fulfilling the $< 60$ seconds acceptance requirement.

---

## 3. Results Manifest Schema (`results/provenance.json`)

```json
{
  "project": "FloquetSim Explorer",
  "version": "1.2.0",
  "timestamp": "ISO-8601 UTC timestamp",
  "environment": {
    "python_version": "string",
    "qiskit_version": "string",
    "qiskit_aer_version": "string",
    "scipy_version": "string",
    "platform": "string"
  },
  "seeds": {
    "seed_transpiler": 42,
    "seed_simulator": 42
  },
  "processors_evaluated": [
    {
      "processor_id": "demo_processor_A",
      "is_official": false,
      "provenance": "string"
    },
    {
      "processor_id": "demo_processor_B",
      "is_official": false,
      "provenance": "string"
    }
  ],
  "artifacts_generated": [
    "results/tables/circuit_metrics_comparison.csv",
    "results/tables/trotter_sweep_results.csv",
    "results/tables/time_evolution_results.csv",
    "results/figures/fig1_trotter_noise_tradeoff.png",
    "results/figures/fig2_magnetization_dynamics.png",
    "results/figures/fig3_circuit_overhead.png",
    "results/figures/fig4_fourier_spectrum.png"
  ]
}
```
