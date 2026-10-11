# Missing-Resource Assessment & Modular Fallback Strategy

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 8, Subphase 0.5  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Formal Confirmation of Missing Official Hardware Files

An exhaustive audit of all provided participant packages, starter notebooks, and public distribution repositories confirms:
- **`processor_A.json` is NOT present** as a standalone file.
- **`processor_B.json` is NOT present** as a standalone file.
- The official Starter Notebook (`Challenge Guide Phase 1`, **DOC-3**, p. 15) provides only an illustrative 5-qubit dictionary snippet (`toy_5q_line`) and leaves empty placeholders for teams to ingest when received from organizers.

To avoid blocking development while maintaining 100% academic honesty, FloquetSim Explorer implements an **honest modular fallback architecture**.

---

## 2. Standardized JSON Schema Design

All processor configurations (whether provisional demonstration fixtures or future official files) adhere strictly to the standardized schema established in Section 12 of the Challenge Guide (**DOC-3**) and Master Specification v1.2:

```json
{
  "processor_id": "string",
  "name": "string",
  "num_qubits": "integer",
  "coupling_map": "list of [q1, q2] pairs",
  "basis_gates": ["rz", "sx", "x", "cx"],
  "ports": [0, 4],
  "is_official": "boolean",
  "hardware_provenance": "string",
  "noise": {
    "type": "string",
    "gate_error_1q": "float",
    "gate_error_2q": "float",
    "readout_error": ["float", "float"]
  }
}
```

---

## 3. Provisional Demonstration Configurations Specification

### 3.1 `processors/demo_processor_A.json` (5-Qubit Linear Baseline)
- **Geometry:** 5-qubit linear chain: `[[0,1], [1,2], [2,3], [3,4]]`.
- **Basis Gates:** `["rz", "sx", "x", "cx"]`.
- **Illustrative Noise Rates:** $p_{1Q} = 0.001$, $p_{2Q} = 0.01$, readout errors $[0.01, 0.02]$ (exact values from Starter Notebook p. 13).
- **Provenance Tag:** `"is_official": false`, `"hardware_provenance": "Provisional Demonstration Topology for SRM AP Qiskit Fall Fest 2026"`.

### 3.2 `processors/demo_processor_B.json` (7-Qubit Heavy-Hex-Inspired Graph)
- **Geometry:** 6-node cycle plus 1 external leaf: `[[0,1], [1,2], [2,3], [3,4], [4,5], [5,0], [2,6]]`.
- **Basis Gates:** `["rz", "sx", "x", "cx"]`.
- **Illustrative Noise Rates:** Identical baseline noise to isolate topological effects from noise parameter drift.
- **Provenance Tag:** `"is_official": false`, `"hardware_provenance": "Provisional Demonstration Topology for SRM AP Qiskit Fall Fest 2026"`.

---

## 4. Dynamic Fallback Loader Protocol (`src/processors.py`)

The hardware loader in `src/processors.py` enforces the following precedence and disclosure rules:

```
[Request Processor 'processor_A']
               │
               ▼
 Does 'processors/processor_A.json' exist?
      ├── YES ──► Load official file. Log: "[INFO] Loaded Official Organizer Processor A."
      │
      └── NO  ──► Check 'processors/demo_processor_A.json'
                    ├── YES ──► Load demonstration fixture.
                    │           Log: "[NOTICE] Official file absent. Loaded Provisional Demonstration Topology."
                    │           Set manifest flag: is_official = False.
                    │           Attach UI warning banner.
                    │
                    └── NO  ──► Raise FileNotFoundError with remediation instructions.
```

---

## 5. Explicit Policy Against Hardware Misrepresentation

1. **Zero False Claims:** Under no circumstances will demonstration configurations be described as "real IBM quantum device calibrations" or "official organizer files."
2. **Prominent Provenance Display:** All exported CSV tables, JSON manifests, console logs, and dashboard views will display explicit tags:  
   `[PROVISIONAL DEMONSTRATION TOPOLOGY (NON-OFFICIAL)]`.
3. **Seamless Drop-In:** If official files are released by hackathon organizers, copying them to `processors/processor_A.json` and `processors/processor_B.json` will automatically promote the system to official mode without modifying a single line of application code.
