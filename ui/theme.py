"""
FloquetSim Explorer - Frontend Design System & Styling Tokens
Specification: Frontend UI Blueprint v1.2 FINAL
Design System: Clean white canvas, soft blue/violet/cyan accents, subtle glass-like cards.
"""

# Palette Tokens
COLOR_MAIN_BG = "#FFFFFF"
COLOR_ALT_BG = "#F7F9FC"
COLOR_TEXT_PRIMARY = "#172033"
COLOR_TEXT_SECONDARY = "#687386"
COLOR_ACCENT_PRIMARY = "#5267F2"     # Indigo / Blue
COLOR_ACCENT_SECONDARY = "#8B5CF6"   # Violet
COLOR_SCIENTIFIC_CYAN = "#29B6D8"    # Cyan highlight
COLOR_BORDER = "#E7EAF1"
COLOR_SUCCESS = "#10B981"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER = "#EF4444"

CUSTOM_CSS = f"""
<style>
/* Main App Canvas */
.stApp {{
    background-color: {COLOR_MAIN_BG};
    color: {COLOR_TEXT_PRIMARY};
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}}

/* Clean Header & Navigation Bar */
header[data-testid="stHeader"] {{
    background-color: rgba(255, 255, 255, 0.95);
    border-bottom: 1px solid {COLOR_BORDER};
}}

/* Typography */
h1, h2, h3, h4, h5, h6 {{
    color: {COLOR_TEXT_PRIMARY};
    font-weight: 600;
    letter-spacing: -0.02em;
}}

p, span, label {{
    color: {COLOR_TEXT_PRIMARY};
}}

.caption-text {{
    color: {COLOR_TEXT_SECONDARY};
    font-size: 0.875rem;
}}

/* Clean Rounded Card Containers */
.scientific-card {{
    background-color: {COLOR_MAIN_BG};
    border: 1px solid {COLOR_BORDER};
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(23, 32, 51, 0.04);
    margin-bottom: 16px;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}

.scientific-card:hover {{
    box-shadow: 0 4px 14px rgba(82, 103, 242, 0.08);
}}

.scientific-card-alt {{
    background-color: {COLOR_ALT_BG};
    border: 1px solid {COLOR_BORDER};
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}}

/* Feature Highlight Cards */
.feature-card {{
    background: linear-gradient(180deg, #FFFFFF 0%, {COLOR_ALT_BG} 100%);
    border: 1px solid {COLOR_BORDER};
    border-radius: 12px;
    padding: 18px;
    height: 100%;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}}
.feature-card:hover {{
    border-color: {COLOR_ACCENT_PRIMARY};
    box-shadow: 0 6px 16px rgba(82, 103, 242, 0.1);
}}

.feature-icon {{
    font-size: 1.5rem;
    margin-bottom: 8px;
    display: inline-block;
}}

.feature-title {{
    font-size: 1.05rem;
    font-weight: 600;
    color: {COLOR_TEXT_PRIMARY};
    margin-bottom: 4px;
}}

.feature-desc {{
    font-size: 0.85rem;
    color: {COLOR_TEXT_SECONDARY};
    line-height: 1.4;
}}

/* Hardware Provenance Banners */
.banner-demo {{
    background-color: #FEF2F2;
    border: 1px solid #FECACA;
    border-left: 4px solid {COLOR_DANGER};
    border-radius: 8px;
    padding: 12px 16px;
    color: #991B1B;
    font-size: 0.875rem;
    line-height: 1.45;
    margin-bottom: 20px;
}}

.banner-official {{
    background-color: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-left: 4px solid {COLOR_SUCCESS};
    border-radius: 8px;
    padding: 12px 16px;
    color: #166534;
    font-size: 0.875rem;
    margin-bottom: 20px;
}}

/* Top Navigation Pills */
.nav-container {{
    display: flex;
    gap: 8px;
    background-color: {COLOR_ALT_BG};
    border: 1px solid {COLOR_BORDER};
    border-radius: 30px;
    padding: 4px;
    margin-bottom: 24px;
    overflow-x: auto;
}}

/* Custom Buttons */
.stButton > button {{
    border-radius: 8px;
    font-weight: 500;
    border: 1px solid {COLOR_BORDER};
    background-color: {COLOR_MAIN_BG};
    color: {COLOR_TEXT_PRIMARY};
    transition: all 0.15s ease-in-out;
}}

.stButton > button:hover {{
    border-color: {COLOR_ACCENT_PRIMARY};
    color: {COLOR_ACCENT_PRIMARY};
    box-shadow: 0 2px 6px rgba(82, 103, 242, 0.12);
}}

.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {COLOR_ACCENT_PRIMARY} 0%, {COLOR_ACCENT_SECONDARY} 100%);
    color: #FFFFFF;
    border: none;
}}

.stButton > button[kind="primary"]:hover {{
    box-shadow: 0 4px 12px rgba(82, 103, 242, 0.3);
    transform: translateY(-1px);
}}

/* Streamlit Metrics */
[data-testid="stMetricValue"] {{
    color: {COLOR_ACCENT_PRIMARY};
    font-weight: 700;
}}

[data-testid="stMetricLabel"] {{
    color: {COLOR_TEXT_SECONDARY};
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

/* Tab Styling */
.stTabs [data-baseweb="tab-list"] {{
    gap: 12px;
    border-bottom: 1px solid {COLOR_BORDER};
}}

.stTabs [data-baseweb="tab"] {{
    padding: 10px 16px;
    font-weight: 500;
    color: {COLOR_TEXT_SECONDARY};
    border-radius: 6px 6px 0 0;
}}

.stTabs [aria-selected="true"] {{
    color: {COLOR_ACCENT_PRIMARY} !important;
    border-bottom: 2px solid {COLOR_ACCENT_PRIMARY} !important;
    font-weight: 600;
}}
</style>
"""


def apply_theme():
    """Inject global design system CSS tokens."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
