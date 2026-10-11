"""
FloquetSim Explorer - Section 07: Reports, Results Files & About
Specification: Nagrik Scientific Research Interface Design Reference
Document cards for Research Report, Submission Manifest, Result Artifacts, System Provenance,
and About the Scientific Model with verified file actions and real environment versions.
"""

import os
import json
import streamlit as st
import pandas as pd
from ui.theme import (
    COLOR_CANVAS,
    COLOR_SURFACE,
    COLOR_RAISED,
    COLOR_BORDER,
    COLOR_CYAN,
    COLOR_AMBER,
    COLOR_VIOLET,
    COLOR_SUCCESS,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
)


def render_reports_view():
    """Render Section 07: Reports, Results Files & About."""
    st.markdown("## 📑 Reports, Result Files & Scientific About")
    st.caption("Inspect official project documentation, download reproducibility artifacts, review provenance manifests, and explore model methodology.")

    tab_rep, tab_art, tab_prov, tab_about = st.tabs([
        "📄 Benchmark Reports",
        "💾 Result Artifacts",
        "🔍 System Provenance",
        "ℹ️ About the Science",
    ])

    with tab_rep:
        st.markdown("#### Official Project Documentation")
        rep_col1, rep_col2 = st.columns(2)

        with rep_col1:
            st.markdown(
                f"""
                <div class="scientific-card">
                    <div style="font-weight: 700; font-size: 1.1rem; color: {COLOR_CYAN}; margin-bottom: 6px;">
                        📄 Research Report (report.md)
                    </div>
                    <div class="caption-text" style="margin-bottom: 14px;">
                        Complete scientific manuscript detailing Hamiltonian formulation, Baker-Campbell-Hausdorff 
                        Trotter bounds, physical coupling graph routing realities, and optimal error operating points.
                    </div>
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
                f"""
                <div class="scientific-card">
                    <div style="font-weight: 700; font-size: 1.1rem; color: {COLOR_AMBER}; margin-bottom: 6px;">
                        📑 Submission Manifest (SUBMISSION_MANIFEST.md)
                    </div>
                    <div class="caption-text" style="margin-bottom: 14px;">
                        Qiskit Fall Fest 2026 qualification package checklist, release metadata, hardware disclaimers, 
                        and 1-click cloud environment reproducibility specifications.
                    </div>
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
        st.markdown("#### Generated CSV Benchmarks & Publication Tables")
        csv_files = [
            ("trotter_sweep_results.csv", "Trotter step sweep (m=1..5) error trade-off data"),
            ("time_evolution_results.csv", "Dynamical trajectory & local polarization timeseries"),
            ("circuit_metrics_comparison.csv", "Transpilation circuit depth, gate counts, and SWAP overhead"),
        ]

        art_cols = st.columns(3)
        for idx, (fname, desc) in enumerate(csv_files):
            fpath = os.path.join("results", "tables", fname)
            with art_cols[idx]:
                st.markdown(
                    f"""
                    <div class="scientific-card">
                        <div style="font-weight: 700; font-size: 0.95rem; color: {COLOR_TEXT_PRIMARY}; margin-bottom: 4px; font-family:'JetBrains Mono', monospace;">
                            📊 {fname}
                        </div>
                        <div class="caption-text" style="margin-bottom: 12px;">
                            {desc}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if os.path.exists(fpath):
                    with open(fpath, "rb") as f:
                        fbytes = f.read()
                    st.download_button(
                        f"📥 Download {fname}",
                        data=fbytes,
                        file_name=fname,
                        mime="text/csv",
                        key=f"dl_{fname}",
                        use_container_width=True,
                    )
                else:
                    st.button(f"⚠️ {fname} not found", disabled=True, key=f"dis_{fname}", use_container_width=True)

    with tab_prov:
        st.markdown("#### Execution Provenance & Software Environment Manifest")
        import qiskit
        import qiskit_aer
        import numpy as np
        import scipy
        import pandas as pd
        import plotly
        import streamlit as st_mod

        env_versions = {
            "Qiskit": qiskit.__version__,
            "Qiskit Aer": qiskit_aer.__version__,
            "NumPy": np.__version__,
            "SciPy": scipy.__version__,
            "Pandas": pd.__version__,
            "Plotly": plotly.__version__,
            "Streamlit": st_mod.__version__,
        }

        p_cols = st.columns(4)
        v_items = list(env_versions.items())
        for idx, (pkg, ver) in enumerate(v_items):
            with p_cols[idx % 4]:
                st.metric(pkg, f"v{ver}")

        st.write("")
        prov_path = os.path.join("results", "provenance.json")
        if os.path.exists(prov_path):
            with open(prov_path, "r", encoding="utf-8") as f:
                prov_dict = json.load(f)
            st.markdown("##### Provenance Record (provenance.json):")
            st.json(prov_dict)

    with tab_about:
        st.markdown("#### Scientific Model & Computational Architecture")
        st.markdown(
            f"""
            <div class="scientific-card" style="font-size: 0.9rem; line-height: 1.7;">
                <div style="font-weight: 700; color: {COLOR_CYAN}; font-size: 1.1rem; margin-bottom: 8px;">
                    Interacting Transverse-Field Ising Model (TFIM)
                </div>
                FloquetSim Explorer simulates continuous quantum spin dynamics governed by the standard 1D Transverse-Field Ising Hamiltonian with periodic boundary conditions:
                <br><br>
                <code>H = H_ZZ + H_X + H_Z</code><br>
                • <code>H_ZZ = J * sum(Z_j Z_j+1) + J_boundary * Z_3 Z_0</code> (Longitudinal nearest-neighbor coupling)<br>
                • <code>H_X  = (hx + delta_hx) * sum(X_j)</code> (Transverse magnetic driving field)<br>
                • <code>H_Z  = hz * sum(Z_j)</code> (Longitudinal symmetry-breaking field)<br>
                <br>
                <b>Units and Physical Conventions:</b><br>
                All Hamiltonian coefficients are expressed in angular frequency (rad/s, with ħ = 1). Time is measured in seconds.<br>
                <br>
                <b>Trotterization & Noise Trade-Off:</b><br>
                The first-order Lie-Trotter product formula decomposes non-commuting unitary terms over m time steps:<br>
                <code>U_Trotter(t) = [ exp(-i H_ZZ Δt) exp(-i H_X Δt) exp(-i H_Z Δt) ]^m</code>, where Δt = t / m.<br>
                Higher m reduces algorithmic discretization error O(t²/m), but increases circuit depth and gate count, causing physical noise to accumulate. 
                FloquetSim Explorer identifies the exact optimal step count <b>m*</b> where combined error is minimized.
            </div>
            """,
            unsafe_allow_html=True,
        )
