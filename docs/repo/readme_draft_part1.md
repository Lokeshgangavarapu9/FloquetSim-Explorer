# README Draft - Part 1: Overview & Research Questions

## Project Overview

**FloquetSim Explorer** is an open-source quantum simulation and architecture benchmarking platform developed for the **SRM University-AP Qiskit Fall Fest 2026** under **Track S3: "Noise in Trotter Simulation"**.

When simulating interacting quantum many-body systems on noisy intermediate-scale quantum (NISQ) processors, quantum algorithms face a fundamental tension:
- **Trotter Approximation Error:** Approximating continuous time evolution through discrete Lie-Trotter product formulas requires increasing the step count $m$ to reduce mathematical discretization error ($\mathcal{O}(t^2/m)$).
- **Physical Hardware Noise:** Real quantum processors suffer from gate infidelities and decoherence. Increasing $m$ linearly inflates circuit depth and entangling gate counts, compounding physical noise.
- **Topological Routing Overhead:** Physical processors have sparse, constrained qubit coupling graphs. Interacting logical qubits that are physically separated require compiler-inserted SWAP gates (each adding 3 CNOTs), further accelerating state degradation.

FloquetSim Explorer provides a rigorous, reproducible software framework to characterize this competing trade-off, comparing a 5-qubit linear baseline against a 7-qubit heavy-hex-inspired graph using Qiskit 1.x and Qiskit Aer.

---

## Core Research Question & Hypotheses

### Primary Research Question:
> *How does quantum processor coupling topology govern the competing trade-off between Trotter discretization error and physical gate noise accumulation in quantum spin chain simulations?*

### Falsifiable Scientific Hypotheses:
- **Hypothesis H1 (Error Competition):** As Trotter steps $m$ increase, ideal Trotter error converges toward zero asymptotically; in the presence of physical gate noise, total simulation error balances decaying mathematical error against growing physical decoherence, which may produce a non-monotonic error profile across $m \in [1, 5]$.
- **Hypothesis H2 (Topological Routing Overhead):** Compiling an identical 4-spin closed-boundary Hamiltonian onto Processor A (5-qubit line) versus Processor B (7-qubit heavy-hex ring) induces measurable variations in circuit depth, CNOT count, and inserted SWAP overhead due to differing graph diameters and alternative routing pathways.
