"""
FloquetSim Explorer - Interactive Scientific Web Application
Specification: Frontend UI Blueprint v1.2 FINAL (Sections 01 - 07)
A premium, minimal, user-friendly scientific frontend with a white canvas,
interactive 3D quantum graph visualizations, and modular navigation destinations.
"""

import streamlit as st
from ui.theme import apply_theme
from ui.views.home import render_home_view
from ui.views.studio import render_studio_view
from ui.views.graph_3d_view import render_graph_3d_view
from ui.views.results_view import render_results_view
from ui.views.topology_view import render_topology_view
from ui.views.comparison_view import render_comparison_view
from ui.views.reports_view import render_reports_view

# Page Configuration - White background scientific theme
st.set_page_config(
    page_title="FloquetSim Explorer | Quantum Spin Dynamics",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply Global Design System
apply_theme()

# Navigation Destination List
NAV_DESTINATIONS = [
    "Home",
    "Simulation Studio",
    "Interactive 3D Graph",
    "Scientific Results",
    "Processor Topology Explorer",
    "Experiment Comparison",
    "Reports and About",
]

# Initialize Session State Navigation
if "nav_destination" not in st.session_state:
    st.session_state["nav_destination"] = "Home"

# -------------------------------------------------------------
# SIDEBAR: Clean Navigation & Project Identity
# -------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 12px 0 20px 0;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.6rem;">⚛️</span>
                <span style="font-size: 1.25rem; font-weight: 700; color: #172033; letter-spacing: -0.02em;">FloquetSim</span>
            </div>
            <span style="font-size: 0.78rem; color: #687386; font-weight: 500;">
                SRM University-AP Fall Fest 2026
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Navigation**")
    
    # Format labels with icons
    icon_map = {
        "Home": "🏠 Home",
        "Simulation Studio": "🔬 Simulation Studio",
        "Interactive 3D Graph": "🌐 Interactive 3D Graph",
        "Scientific Results": "📊 Scientific Results",
        "Processor Topology Explorer": "🗺️ Processor Topology",
        "Experiment Comparison": "⚖️ Experiment Comparison",
        "Reports and About": "📑 Reports & About",
    }

    current_idx = NAV_DESTINATIONS.index(st.session_state["nav_destination"]) if st.session_state["nav_destination"] in NAV_DESTINATIONS else 0

    selected_nav = st.radio(
        "Navigation",
        options=NAV_DESTINATIONS,
        format_func=lambda x: icon_map.get(x, x),
        index=current_idx,
        label_visibility="collapsed",
        key="main_nav_radio",
    )

    # Sync state if user clicks sidebar radio
    if selected_nav != st.session_state["nav_destination"]:
        st.session_state["nav_destination"] = selected_nav
        st.rerun()

    st.write("---")
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #687386; line-height: 1.5;">
            <b>Track S3:</b> Noise in Trotter Simulation<br>
            <b>Version:</b> <code>v1.2.0-submission</code><br>
            <b>Model:</b> 1D TFIM (N=4 Spins)<br>
            <b>Backend:</b> Qiskit Aer (Local CPU)
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; font-size: 0.75rem; color: #64748B; margin-top: 14px;">
            ⚠️ <b>Notice:</b> Simulations use verified demonstration topologies and synthetic noise models. Zero physical IBM hardware is connected.
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------------------------------------
# MAIN CONTENT ROUTER: Render Selected View Destination
# -------------------------------------------------------------
current_view = st.session_state["nav_destination"]

if current_view == "Home":
    render_home_view()
elif current_view == "Simulation Studio":
    render_studio_view()
elif current_view == "Interactive 3D Graph":
    render_graph_3d_view()
elif current_view == "Scientific Results":
    render_results_view()
elif current_view == "Processor Topology Explorer":
    render_topology_view()
elif current_view == "Experiment Comparison":
    render_comparison_view()
elif current_view == "Reports and About":
    render_reports_view()
else:
    render_home_view()
