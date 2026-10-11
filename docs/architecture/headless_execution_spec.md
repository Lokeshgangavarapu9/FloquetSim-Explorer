# Headless Scientific Execution Specification

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 13, Subphase 5.1  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Architectural Separation of Concerns

To guarantee that the automated hackathon grading pipeline can evaluate the submission without requiring a display server, window manager, or browser process, FloquetSim Explorer strictly decouples the scientific execution path from presentation interfaces:

```
                          ┌───────────────────────────┐
                          │   CLI Invocation          │
                          │   `python main.py [args]` │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │   `src/cli.py`            │
                          │   - argparse CLI parser   │
                          │   - parameter validation  │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │   `src/experiments.py`    │
                          │   - orchestrate sweeps    │
                          │   - dispatch simulation   │
                          └─────────────┬─────────────┘
                                        │
             ┌──────────────────────────┼──────────────────────────┐
             ▼                          ▼                          ▼
┌─────────────────────────┐┌─────────────────────────┐┌─────────────────────────┐
│  `src/classical_solver` ││    `src/transpiler`     ││    `src/simulation`     │
│  - SciPy expm reference ││    - Sabre routing      ││    - Aer noisy & ideal  │
└─────────────────────────┘└─────────────────────────┘└─────────────────────────┘
             │                          │                          │
             └──────────────────────────┼──────────────────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │   `src/reporting.py`      │
                          │   - export CSV tables     │
                          │   - render 300 DPI PNGs   │
                          │   - write provenance.json │
                          └───────────────────────────┘
```

---

## 2. CLI Interface Arguments

`main.py` is the universal headless entrypoint accepting standard command-line options:

```bash
python main.py [OPTIONS]
```

| Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--processor` | string | `all` | Target processor (`demo_processor_A`, `demo_processor_B`, or `all`). |
| `--trotter-steps` | string | `1,2,3,4,5` | Comma-delimited list of Trotter discretization steps $m$. |
| `--time` | float | `5.0` | Target evolution time $t$ in seconds. |
| `--shots` | integer | `2048` | Number of measurement shots per circuit execution. |
| `--seed` | integer | `42` | Deterministic random seed for transpiler and Aer simulator. |
| `--output-dir` | path | `results` | Root destination folder for tables and figures. |
| `--quick` | flag | `False` | Run accelerated smoke-test sweep ($m \in [1, 2]$, 512 shots) for CI. |

---

## 3. Headless Verification Invariant

When `python main.py` is invoked:
1. It must not import `streamlit` or any GUI module.
2. It must execute completely within `< 60` seconds on a standard 2-core cloud VM.
3. It must write all standardized CSV tables to `results/tables/`.
4. It must write all 300 DPI publication plots to `results/figures/`.
5. It must write `results/provenance.json` with execution metadata.
6. It must return exit code `0` upon successful completion.
