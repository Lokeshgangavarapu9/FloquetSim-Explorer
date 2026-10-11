# Hardware Fallback & Provenance Strategy

**Project:** FloquetSim Explorer  
**Specification:** Master Engineering Specification v1.2, Section 11, Subphase 3.2  
**Date:** October 11, 2026  
**Auditor:** Google Antigravity (Autonomous AI Development Agent)

---

## 1. Context & Architectural Challenge

Official hackathon guidelines reference `processor_A.json` and `processor_B.json`. However, these standalone files were not provided in the public competition kit. Halting development waiting for external organizers would violate hackathon deadlines, while fabricating files and claiming they are official IBM calibrations would violate scientific ethics and academic integrity rules.

---

## 2. The Transparent Modular Fallback Solution

FloquetSim Explorer resolves this challenge by creating two explicit, provisional demonstration fixtures:
1. `processors/demo_processor_A.json`: 5-qubit linear baseline graph ($0-1-2-3-4$).
2. `processors/demo_processor_B.json`: 7-qubit heavy-hex-inspired graph ($0-1-2-3-4-5-0 + 2-6$).

### Explicit Provenance Metadata:
Both files contain strict provenance fields:
```json
{
  "is_official": false,
  "hardware_provenance": "Provisional demonstration topology for SRM AP Qiskit Fall Fest 2026."
}
```

---

## 3. Dynamic Resolution Architecture

When any module requests a processor definition (via `src/processors.py`):
1. **Official Path Search:** The loader searches for `processors/processor_A.json` (or `processor_B.json`).
2. **Official Activation:** If found, the official file is loaded, setting `is_official: true` and logging:  
   `[INFO] Loaded official organizer processor configuration.`
3. **Demonstration Fallback:** If absent, the loader falls back to `processors/demo_processor_A.json`, setting `is_official: false` and logging:  
   `[NOTICE] Official file absent. Loaded Provisional Demonstration Topology.`
4. **Display Warnings:** All console runs, exported CSV tables, JSON manifests, and dashboard UI headers prominently display:  
   `[PROVISIONAL DEMONSTRATION TOPOLOGY (NON-OFFICIAL)]`.

This ensures the software is 100% functional, 100% honest, and immediately upgradeable without code changes if official files arrive.
