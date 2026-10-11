"""
FloquetSim Explorer - Interactive Scientific Web Application
Specification: Nagrik Scientific Research Interface Design Reference
A precision quantum simulation platform featuring deep navy-black canvas (#07090E),
dark card surfaces (#0F131D), technical hairline borders (#2A354D), and holographic
cyan (#00D5E8) & amber (#FFB300) telemetry.
"""

import streamlit as st
from ui.theme import (
    apply_theme,
    COLOR_CANVAS,
    COLOR_SURFACE,
    COLOR_BORDER,
    COLOR_CYAN,
    COLOR_AMBER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
)
from ui.views.dashboard import render_dashboard_view
from ui.views.studio import render_studio_view
from ui.views.graph_3d_view import render_graph_3d_view
from ui.views.results_view import render_results_view
from ui.views.topology_view import render_topology_view
from ui.views.comparison_view import render_comparison_view
from ui.views.reports_view import render_reports_view

# Page Configuration - Deep dark research environment
st.set_page_config(
    page_title="FloquetSim Explorer | Quantum Spin Dynamics Lab",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply Global Nagrik Design System
apply_theme()

# The 7 Official Navigation Destinations
NAV_DESTINATIONS = [
    "Landing Page",
    "Simulation Studio",
    "Interactive Quantum Graph",
    "Scientific Results",
    "Processor Topology Explorer",
    "Experiment Comparison",
    "Reports & About",
]

NAV_ALIASES = {
    "Dashboard": "Landing Page",
    "Home": "Landing Page",
    "Interactive 3D Quantum Graph": "Interactive Quantum Graph",
    "Reports and About": "Reports & About",
}

# Initialize session state navigation & simulation telemetry
if "nav_destination" not in st.session_state:
    st.session_state["nav_destination"] = "Landing Page"
elif st.session_state["nav_destination"] in NAV_ALIASES:
    st.session_state["nav_destination"] = NAV_ALIASES[st.session_state["nav_destination"]]
elif st.session_state["nav_destination"] not in NAV_DESTINATIONS:
    st.session_state["nav_destination"] = "Landing Page"

if "sim_status" not in st.session_state:
    st.session_state["sim_status"] = "idle"  # idle, running, completed, failed

if "selected_processor_id" not in st.session_state:
    st.session_state["selected_processor_id"] = "demo_processor_A"

# -------------------------------------------------------------
# SIDEBAR: Persistent Identity & Primary Navigation
# -------------------------------------------------------------
with st.sidebar:
    st.markdown(
        f"""
        <div style="padding: 6px 0 14px 0;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 36px; height: 36px; border-radius: 6px; background-color: {COLOR_SURFACE}; border: 1px solid {COLOR_BORDER}; display: flex; align-items: center; justify-content: center; color: {COLOR_CYAN}; font-size: 1.25rem; box-shadow: 0 0 10px rgba(0, 213, 232, 0.25);">
                    ⚛
                </div>
                <div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: {COLOR_TEXT_PRIMARY}; letter-spacing: -0.02em; line-height: 1.2;">
                        FloquetSim Explorer
                    </div>
                    <div style="font-size: 0.72rem; color: {COLOR_TEXT_SECONDARY}; font-family: 'JetBrains Mono', monospace;">
                        Quantum Dynamics • Track S3
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<p style='font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: {COLOR_TEXT_SECONDARY}; margin-bottom: 6px;'>Navigation</p>",
        unsafe_allow_html=True,
    )

    nav_labels = {
        "Landing Page": "⌂  Landing Page",
        "Simulation Studio": "⚛  Simulation Studio",
        "Interactive Quantum Graph": "🌐  Interactive Quantum Graph",
        "Scientific Results": "📊  Scientific Results",
        "Processor Topology Explorer": "⎇  Processor Topology",
        "Experiment Comparison": "⚖  Experiment Comparison",
        "Reports & About": "▤  Reports & About",
    }

    current_idx = NAV_DESTINATIONS.index(st.session_state["nav_destination"])

    selected_nav = st.radio(
        "Navigation",
        options=NAV_DESTINATIONS,
        format_func=lambda x: nav_labels.get(x, x),
        index=current_idx,
        label_visibility="collapsed",
        key="main_nav_radio",
    )

    if selected_nav != st.session_state["nav_destination"]:
        st.session_state["nav_destination"] = selected_nav
        st.rerun()

    st.write("---")

    # Status & Telemetry Summary
    status_label = st.session_state.get("sim_status", "idle").upper()
    status_class = f"status-pill-{st.session_state.get('sim_status', 'idle')}"
    active_proc_name = "Processor A (5Q Line)" if "A" in st.session_state.get("selected_processor_id", "A") else "Processor B (7Q Hex-Ring)"

    st.markdown(
        f"""
        <div style="font-size: 0.76rem; color: {COLOR_TEXT_SECONDARY}; line-height: 1.7; background-color: {COLOR_SURFACE}; border: 1px solid {COLOR_BORDER}; border-radius: 6px; padding: 10px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <span style="font-weight:600; color:{COLOR_TEXT_PRIMARY};">Status:</span>
                <span class="param-pill {status_class}">{status_label}</span>
            </div>
            • <b>Active Architecture:</b> <span style="color:{COLOR_CYAN}; font-family:'JetBrains Mono', monospace;">{active_proc_name}</span><br>
            • <b>Hamiltonian Model:</b> 1D TFIM (N=4)<br>
            • <b>Simulation Backend:</b> Qiskit Aer CPU<br>
            • <b>Host Institution:</b> SRM University-AP
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="background-color: rgba(255, 179, 0, 0.05); border: 1px solid {COLOR_BORDER}; border-left: 3px solid {COLOR_AMBER}; border-radius: 6px; padding: 8px 10px; font-size: 0.72rem; color: {COLOR_TEXT_SECONDARY}; margin-top: 10px; line-height: 1.45;">
            ⚠️ <b>Demonstration Notice:</b> Zero real IBM hardware is connected. All runs execute on local CPU Aer with demonstration topologies.
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------------------------------------
# TOP COMPACT QUICK NAVIGATION & TELEMETRY HEADER
# -------------------------------------------------------------
top_bar_cols = st.columns([2.0, 8.0])
with top_bar_cols[0]:
    st.markdown(
        f"""
        <div style="padding: 4px 0; font-size: 0.84rem; font-weight: 600; color: {COLOR_CYAN}; display: flex; align-items: center; gap: 8px; font-family:'JetBrains Mono', monospace;">
            <span style="color:{COLOR_AMBER};">●</span> <span>{st.session_state['nav_destination']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_bar_cols[1]:
    q_cols = st.columns(len(NAV_DESTINATIONS))
    short_names = {
        "Landing Page": "Landing",
        "Simulation Studio": "Studio",
        "Interactive Quantum Graph": "Graph",
        "Scientific Results": "Results",
        "Processor Topology Explorer": "Topology",
        "Experiment Comparison": "Compare",
        "Reports & About": "Reports",
    }
    for idx, dest in enumerate(NAV_DESTINATIONS):
        with q_cols[idx]:
            is_active = (dest == st.session_state["nav_destination"])
            btn_label = f"▸ {short_names[dest]}" if is_active else short_names[dest]
            if st.button(
                btn_label, 
                key=f"top_nav_{dest}", 
                type="primary" if is_active else "secondary", 
                use_container_width=True
            ):
                if not is_active:
                    st.session_state["nav_destination"] = dest
                    st.rerun()

st.markdown(f"<div style='margin-bottom: 12px; border-bottom: 1px solid {COLOR_BORDER};'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# MAIN CONTENT ROUTER: Render Selected View Destination
# -------------------------------------------------------------
current_view = st.session_state["nav_destination"]

if current_view in ["Landing Page", "Dashboard", "Home"]:
    render_dashboard_view()
elif current_view == "Simulation Studio":
    render_studio_view()
elif current_view in ["Interactive Quantum Graph", "Interactive 3D Quantum Graph"]:
    render_graph_3d_view()
elif current_view == "Scientific Results":
    render_results_view()
elif current_view == "Processor Topology Explorer":
    render_topology_view()
elif current_view == "Experiment Comparison":
    render_comparison_view()
elif current_view in ["Reports & About", "Reports and About"]:
    render_reports_view()
else:
    render_dashboard_view()
