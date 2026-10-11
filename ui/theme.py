"""
FloquetSim Explorer - Frontend Design System & Styling Tokens
Specification: Nagrik Scientific Research Interface Design Reference
Palette:
  Canvas:           #07090E  (Deep navy-black)
  Card surface:     #0F131D  (Dark navy card surface)
  Raised surface:   #171E2E  (Elevated panel / control surface)
  Borders:          #2A354D  (Technical hairline border)
  Primary text:     #F4F7FB  (Crisp high-contrast off-white)
  Secondary text:   #9AA6B8  (Technical slate grey)
  Cyan accent:      #00D5E8  (Primary quantum telemetry & action)
  Amber accent:     #FFB300  (Warning / Highlight / Focus)
  Violet accent:    #7C4DFF  (Quantum phase / Experiment B)
  Success:          #10B981  (Verified / Validated status)
  Error:            #EF4444  (Failure / Non-Hermitian error)
Typography:
  UI Text: Inter, -apple-system, sans-serif
  Numbers/Data: JetBrains Mono, monospace (tabular numerals)
"""

# Nagrik Reference Color Tokens
COLOR_CANVAS = "#07090E"             # Deep navy-black canvas
COLOR_SURFACE = "#0F131D"            # Dark navy card surface
COLOR_RAISED = "#171E2E"             # Raised surface / input control
COLOR_SECONDARY_SURFACE = "#171E2E"  # Alias for raised surface
COLOR_DARK_SURFACE = "#0F131D"       # Dark surface
COLOR_BACKGROUND_DARK = "#07090E"    # Deep canvas
COLOR_GRAPH_WORKSPACE = "#07090E"    # 3D Graph workspace canvas

COLOR_BORDER = "#2A354D"             # Hairline border
COLOR_BORDER_DARK = "#2A354D"        # Consistent border
COLOR_BORDER_SUBTLE = "#1B2335"      # Subtle separator border

COLOR_TEXT_PRIMARY = "#F4F7FB"       # Crisp high-contrast off-white
COLOR_TEXT_SECONDARY = "#9AA6B8"     # Technical slate grey
COLOR_TEXT_DARK = "#F4F7FB"          # Same for dark surfaces

COLOR_CYAN = "#00D5E8"               # Cyan accent (Primary action & telemetry)
COLOR_PRIMARY_ACCENT = "#00D5E8"     # Cyan accent
COLOR_QUANTUM_CYAN = "#00D5E8"       # Cyan accent
COLOR_AMBER = "#FFB300"              # Amber accent (Caution & focus)
COLOR_GOLD = "#FFB300"               # Mapped to amber accent
COLOR_BRONZE = "#00D5E8"             # Mapped to cyan accent
COLOR_COPPER = "#FFB300"             # Mapped to amber accent
COLOR_VIOLET = "#7C4DFF"             # Violet accent (Experiment B & secondary metrics)
COLOR_SUCCESS = "#10B981"            # Emerald green success
COLOR_WARNING = "#FFB300"            # Amber warning
COLOR_ERROR = "#EF4444"              # Crimson error

# 3D Quantum Graph Tokens
COLOR_NODE_SELECTED = "#FFB300"      # Amber for selected node
COLOR_NODE_NEIGHBOR = "#00D5E8"      # Cyan for incident neighbors
COLOR_NODE_DEFAULT = "#7C4DFF"       # Violet for default nodes
COLOR_EDGE_DEFAULT = "#2A354D"       # Hairline border edge
COLOR_EDGE_ACTIVE = "#00D5E8"        # Luminous cyan active edge
COLOR_GRAPH_BLUE = "#00D5E8"         # Cyan
COLOR_GRAPH_VIOLET = "#7C4DFF"       # Violet

CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* Main App Canvas */
.stApp {{
    background-color: {COLOR_CANVAS};
    color: {COLOR_TEXT_PRIMARY};
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    background-image: radial-gradient({COLOR_BORDER} 0.65px, transparent 0.65px);
    background-size: 28px 28px;
}}

/* Typography Hierarchy */
h1 {{
    color: {COLOR_TEXT_PRIMARY};
    font-size: 2.25rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    line-height: 1.2;
}}

h2 {{
    color: {COLOR_TEXT_PRIMARY};
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.25;
}}

h3 {{
    color: {COLOR_TEXT_PRIMARY};
    font-size: 1.3rem;
    font-weight: 600;
    letter-spacing: -0.015em;
}}

h4 {{
    color: {COLOR_TEXT_PRIMARY};
    font-size: 1.1rem;
    font-weight: 600;
}}

p, span, label, div {{
    color: {COLOR_TEXT_PRIMARY};
    font-size: 0.94rem;
}}

.caption-text {{
    color: {COLOR_TEXT_SECONDARY};
    font-size: 0.84rem;
    line-height: 1.45;
}}

.code-font {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.86rem;
    font-feature-settings: 'tnum';
}}

/* Clean Header & Navigation Bar */
header[data-testid="stHeader"] {{
    background-color: rgba(7, 9, 14, 0.95);
    border-bottom: 1px solid {COLOR_BORDER};
    backdrop-filter: blur(10px);
}}

/* Sidebar Re-open / Collapsed Control Button */
[data-testid="collapsedControl"] {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background-color: {COLOR_SURFACE} !important;
    color: {COLOR_CYAN} !important;
    border-radius: 6px !important;
    padding: 6px 12px !important;
    box-shadow: 0 0 12px rgba(0, 213, 232, 0.2) !important;
    border: 1px solid {COLOR_BORDER} !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}}

[data-testid="collapsedControl"]:hover {{
    border-color: {COLOR_CYAN} !important;
    color: #FFFFFF !important;
}}

[data-testid="collapsedControl"] svg {{
    fill: {COLOR_CYAN} !important;
    stroke: {COLOR_CYAN} !important;
    width: 18px !important;
    height: 18px !important;
}}

/* Sidebar Styling */
section[data-testid="stSidebar"] {{
    background-color: {COLOR_SURFACE};
    border-right: 1px solid {COLOR_BORDER};
}}

section[data-testid="stSidebar"] hr {{
    border-color: {COLOR_BORDER} !important;
}}

section[data-testid="stSidebar"] .stRadio > div {{
    gap: 4px;
}}

section[data-testid="stSidebar"] .stRadio label {{
    padding: 7px 12px;
    border-radius: 6px;
    font-weight: 500;
    font-size: 0.9rem;
    color: {COLOR_TEXT_SECONDARY};
    transition: all 0.15s ease;
}}

section[data-testid="stSidebar"] .stRadio label:hover {{
    color: {COLOR_TEXT_PRIMARY};
    background-color: {COLOR_RAISED};
}}

/* Compact Scientific Cards */
.scientific-card {{
    background-color: {COLOR_SURFACE};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    padding: 18px;
    margin-bottom: 14px;
    transition: border-color 0.15s ease;
}}

.scientific-card:hover {{
    border-color: {COLOR_CYAN};
}}

.scientific-card-alt {{
    background-color: {COLOR_RAISED};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 14px;
}}

/* 3D Graph Workspace Panel */
.graph-workspace-panel {{
    background-color: {COLOR_SURFACE};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    padding: 6px;
    position: relative;
    overflow: hidden;
}}

/* Status & Parameter Pill */
.param-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background-color: {COLOR_RAISED};
    color: {COLOR_CYAN};
    border: 1px solid {COLOR_BORDER};
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 0.78rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    font-feature-settings: 'tnum';
}}

.status-pill-idle {{
    background-color: rgba(154, 166, 184, 0.12);
    color: {COLOR_TEXT_SECONDARY};
    border: 1px solid {COLOR_BORDER};
}}

.status-pill-running {{
    background-color: rgba(255, 179, 0, 0.15);
    color: {COLOR_AMBER};
    border: 1px solid {COLOR_AMBER};
}}

.status-pill-completed {{
    background-color: rgba(16, 185, 129, 0.15);
    color: {COLOR_SUCCESS};
    border: 1px solid {COLOR_SUCCESS};
}}

.status-pill-failed {{
    background-color: rgba(239, 68, 68, 0.15);
    color: {COLOR_ERROR};
    border: 1px solid {COLOR_ERROR};
}}

/* Scientific Notice Banners */
.banner-demo {{
    background-color: rgba(255, 179, 0, 0.06);
    border: 1px solid {COLOR_BORDER};
    border-left: 3px solid {COLOR_AMBER};
    border-radius: 6px;
    padding: 10px 14px;
    color: {COLOR_TEXT_PRIMARY};
    font-size: 0.84rem;
    line-height: 1.45;
    margin-bottom: 14px;
}}

.banner-official {{
    background-color: rgba(16, 185, 129, 0.06);
    border: 1px solid {COLOR_BORDER};
    border-left: 3px solid {COLOR_SUCCESS};
    border-radius: 6px;
    padding: 10px 14px;
    color: {COLOR_TEXT_PRIMARY};
    font-size: 0.84rem;
    margin-bottom: 14px;
}}

/* Buttons */
.stButton > button {{
    border-radius: 6px;
    font-weight: 500;
    font-size: 0.88rem;
    padding: 6px 16px;
    border: 1px solid {COLOR_BORDER};
    background-color: {COLOR_RAISED};
    color: {COLOR_TEXT_PRIMARY};
    transition: all 0.15s ease-in-out;
}}

.stButton > button:hover {{
    border-color: {COLOR_CYAN};
    color: {COLOR_CYAN};
}}

.stButton > button[kind="primary"] {{
    background: {COLOR_CYAN};
    color: #07090E;
    font-weight: 600;
    border: 1px solid {COLOR_CYAN};
    box-shadow: 0 0 14px rgba(0, 213, 232, 0.3);
}}

.stButton > button[kind="primary"]:hover {{
    background: #20E0F0;
    color: #07090E;
    box-shadow: 0 0 20px rgba(0, 213, 232, 0.5);
}}

/* Metrics Display */
[data-testid="stMetric"] {{
    background-color: {COLOR_SURFACE};
    border: 1px solid {COLOR_BORDER};
    border-radius: 8px;
    padding: 10px 14px;
}}

[data-testid="stMetricValue"] {{
    color: {COLOR_CYAN};
    font-family: 'JetBrains Mono', monospace;
    font-feature-settings: 'tnum';
    font-weight: 700;
    font-size: 1.6rem !important;
}}

[data-testid="stMetricLabel"] {{
    color: {COLOR_TEXT_SECONDARY};
    font-size: 0.78rem !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {{
    gap: 6px;
    border-bottom: 1px solid {COLOR_BORDER};
    background-color: transparent;
}}

.stTabs [data-baseweb="tab"] {{
    padding: 8px 16px;
    font-weight: 500;
    font-size: 0.88rem;
    color: {COLOR_TEXT_SECONDARY};
    border-radius: 4px 4px 0 0;
    background-color: transparent;
    transition: color 0.15s ease;
}}

.stTabs [aria-selected="true"] {{
    color: {COLOR_CYAN} !important;
    border-bottom: 2px solid {COLOR_CYAN} !important;
    font-weight: 600;
}}

/* Form Controls & Inputs */
.stSelectbox label, .stSlider label, .stNumberInput label {{
    font-weight: 500;
    font-size: 0.84rem;
    color: {COLOR_TEXT_SECONDARY};
}}

div[data-baseweb="select"] > div {{
    background-color: {COLOR_RAISED} !important;
    border-color: {COLOR_BORDER} !important;
    color: {COLOR_TEXT_PRIMARY} !important;
    border-radius: 6px !important;
}}

div[data-baseweb="input"] {{
    background-color: {COLOR_RAISED} !important;
    border-color: {COLOR_BORDER} !important;
    color: {COLOR_TEXT_PRIMARY} !important;
    border-radius: 6px !important;
}}

/* Streamlit Expander */
div[data-testid="stExpander"] {{
    background-color: {COLOR_SURFACE} !important;
    border: 1px solid {COLOR_BORDER} !important;
    border-radius: 8px !important;
}}

/* Dataframe & Tables */
div[data-testid="stDataFrame"] {{
    border: 1px solid {COLOR_BORDER};
    border-radius: 6px;
}}
</style>
"""


def apply_theme():
    """Inject global Nagrik research design system CSS tokens."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def apply_plotly_theme(fig, height: int = None, title: str = None):
    """
    Apply unified Nagrik research dark theme to any Plotly Figure.
    Sets canvas, axes, fonts, hairline borders, and hoverlabel styles.
    """
    layout_update = dict(
        paper_bgcolor=COLOR_CANVAS,
        plot_bgcolor=COLOR_SURFACE,
        font=dict(
            family="Inter, -apple-system, sans-serif",
            color=COLOR_TEXT_PRIMARY,
            size=12,
        ),
        xaxis=dict(
            gridcolor=COLOR_BORDER,
            zerolinecolor=COLOR_BORDER,
            tickfont=dict(family="JetBrains Mono, monospace", size=10, color=COLOR_TEXT_SECONDARY),
            titlefont=dict(size=12, color=COLOR_TEXT_PRIMARY),
            linecolor=COLOR_BORDER,
        ),
        yaxis=dict(
            gridcolor=COLOR_BORDER,
            zerolinecolor=COLOR_BORDER,
            tickfont=dict(family="JetBrains Mono, monospace", size=10, color=COLOR_TEXT_SECONDARY),
            titlefont=dict(size=12, color=COLOR_TEXT_PRIMARY),
            linecolor=COLOR_BORDER,
        ),
        legend=dict(
            bgcolor="rgba(15, 19, 29, 0.85)",
            bordercolor=COLOR_BORDER,
            borderwidth=1,
            font=dict(size=11, color=COLOR_TEXT_PRIMARY),
        ),
        hoverlabel=dict(
            bgcolor=COLOR_RAISED,
            bordercolor=COLOR_BORDER,
            font=dict(family="JetBrains Mono, monospace", size=11, color=COLOR_TEXT_PRIMARY),
        ),
        margin=dict(l=45, r=25, t=35 if title else 20, b=35),
    )
    if height:
        layout_update["height"] = height
    if title:
        layout_update["title"] = dict(
            text=f"<b>{title}</b>",
            font=dict(size=13, color=COLOR_TEXT_PRIMARY),
            x=0.01,
            xanchor="left",
        )
    fig.update_layout(**layout_update)
    return fig
