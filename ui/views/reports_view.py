"""
FloquetSim Explorer - Section 07: Reports, Results Files & About
Specification: Frontend UI Blueprint v1.2 FINAL, Page 8
Comprehensive scientific auditing, environmental provenance manifests, machine-readable artifacts,
and transparent disclosures regarding classical simulation and synthetic noise modeling.
"""

import os
import json
import streamlit as st
import pandas as pd


def render_reports_view():
    """Render Section 07: Reports, Results Files & About."""
    st.markdown("## 📑 Reports, Result Files & Scientific About")
    st.caption("Inspect audit logs, review environmental provenance manifests, download datasets, and understand the physical model.")

    tab_rep, tab_art, tab_prov, tab_about = st.tabs([
        "📄 Benchmark Reports",
        "💾 Result Artifacts",
        "🔍 System Provenance",
        "ℹ️ About the Science",
    ])

    with tab_rep:
        st.markdown("#### Official Competition Documentation")
        rep_col1, rep_col2 = st.columns(2)

        with rep_col1:
            st.markdown(
                """
                <div class="scientific-card">
                    <span style="font-weight: 600; font-size: 1.05rem; color: #5267F2;">
                        Research Report (report.md)
                    </span><br>
                    <span class="caption-text">Comprehensive scientific manuscript detailing Hamiltonian formulation, Baker-Campbell-Hausdorff Trotter error bounds, graph routing realities, and empirical optimal step counts.</span><br><br>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if os.path.exists("report.md"):
                with open("report.md", "r", encoding="utf-8") as f:
                    rep_text = f.read()
                st.download_button(
                    "📥 Download report.md",
                    data=rep_text,
                    file_name="report.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

        with rep_col2:
            st.markdown(
                """
                <div class="scientific-card">
                    <span style="font-weight: 600; font-size: 1.05rem; color: #8B5CF6;">
                        Submission Manifest (SUBMISSION_MANIFEST.md)
                    </span><br>
                    <span class="caption-text">Phase 1 qualification package checklist, release metadata, hardware disclaimers, and 1-click cloud reproducibility instructions.</span><br><br>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if os.path.exists("SUBMISSION_MANIFEST.md"):
                with open("SUBMISSION_MANIFEST.md", "r", encoding="utf-8") as f:
                    man_text = f.read()
                st.download_button(
                    "📥 Download SUBMISSION_MANIFEST.md",
                    data=man_text,
                    file_name="SUBMISSION_MANIFEST.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

    with tab_art:
        st.markdown("#### Generated Result Artifacts (`results/`)")

        tables_dir = "results/tables"
        figs_dir = "results/figures"

        st.markdown("##### Tabular Datasets (CSV)")
        if os.path.exists(tables_dir):
            csv_files = [f for f in os.listdir(tables_dir) if f.endswith(".csv")]
            if csv_files:
                for f_name in sorted(csv_files):
                    f_path = os.path.join(tables_dir, f_name)
                    df_item = pd.read_csv(f_path)
                    with st.expander(f"📊 {f_name} ({len(df_item)} rows)"):
                        try:
                            st.dataframe(df_item.head(10), use_container_width=True)
                        except Exception:
                            st.table(df_item.head(10))
                        st.download_button(
                            f"Download {f_name}",
                            data=open(f_path, "rb").read(),
                            file_name=f_name,
                            mime="text/csv",
                            key=f"dl_{f_name}",
                        )
            else:
                st.info("No CSV files found in results/tables/. Run the benchmark via CLI or Simulation Studio to generate them.")
        else:
            st.info("Results directory will be populated upon benchmark completion.")

        st.markdown("##### Publication Figures (300 DPI PNG)")
        if os.path.exists(figs_dir):
            png_files = [f for f in os.listdir(figs_dir) if f.endswith(".png")]
            if png_files:
                for p_name in sorted(png_files):
                    p_path = os.path.join(figs_dir, p_name)
                    st.caption(f"🖼️ {p_name}")
                    st.image(p_path, use_column_width=True)
            else:
                st.info("No figures found in results/figures/.")

    with tab_prov:
        st.markdown("#### Environmental Provenance & Audit Trail")
        prov_path = "results/provenance.json"
        if os.path.exists(prov_path):
            with open(prov_path, "r", encoding="utf-8") as pf:
                prov_data = json.load(pf)
            st.json(prov_data)
        else:
            st.info("Run `python main.py` to generate the complete environmental provenance manifest (`results/provenance.json`).")

    with tab_about:
        st.markdown("#### About FloquetSim Explorer")
        st.markdown(
            """
            **Project Title:** FloquetSim Explorer: Geometry-Aware Quantum Simulation & Trotter-Noise Benchmark  
            **Competition:** SRM University-AP Qiskit Fall Fest 2026 (Phase 1 Qualification)  
            **Track:** Track S3: "Noise in Trotter Simulation"  
            **Release Version:** `v1.2.0-submission`  

            ---

            ##### Scientific Model Summary
            The simulated system is a 4-spin quantum chain ($N=4$, $16 \\times 16$ Hilbert space) governed by the 
            interacting Transverse-Field Ising Model (TFIM) under continuous quench evolution:
            $$H = H_{ZZ} + H_X + H_Z$$
            where:
            - $H_{ZZ} = J \\sum_{j=0}^{2} Z_j Z_{j+1} + J Z_3 Z_0$ (closed periodic boundary).
            - $H_X = \\sum_{j=0}^3 (h_x + \\delta h_x^j) X_j$ ($h_x = 1.0$ rad/s, $\\delta h_x = 0.05$ rad/s).
            - $H_Z = h_z \\sum_{j=0}^3 Z_j$ ($h_z = 0.1$ rad/s).

            ##### Crucial Ethical & Scientific Boundaries
            1. **Classical Solvability:** A 4-spin quantum chain is trivially solvable on classical computers in milliseconds via dense matrix exponentiation (`scipy.linalg.expm`). No claims of quantum supremacy or physical quantum advantage are made.
            2. **Synthetic Noise Approximation:** All simulations employ Qiskit Aer's local simulator with parameterized depolarizing and readout noise channels from the starter guide. They do not represent physical IBM Quantum hardware calibration data.
            3. **Hardware Provenance:** Demonstration topologies (`demo_processor_A.json` and `demo_processor_B.json`) represent verified demonstration couplings for comparative compiler studies. Zero claims are made that a physical IBM device is actively connected.
            """
        )
