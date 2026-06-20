"""
TerraByte Streamlit Frontend Application.
Author: Expert Streamlit Developer
"""

import streamlit as st
import pandas as pd
import textwrap
import html
import os
from src.calculator import CarbonEngine
from src.assistant import EcoAssistant

# Set page configuration for a premium look
st.set_page_config(
    page_title="TerraByte — Eco-Action Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load External CSS for Clean Architecture
def load_css(file_name: str):
    """Loads external CSS to maintain clean Python architecture."""
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"Styling file {file_name} not found.")

load_css("style.css")

# Initialize Backend Engines securely and efficiently
@st.cache_resource
def load_engines():
    return CarbonEngine(), EcoAssistant()

try:
    engine, assistant = load_engines()
except Exception as e:
    st.error(f"Failed to initialize calculation engines: {str(e)}")
    st.stop()

# ----------------- CACHED LOGIC ENGINE -----------------
@st.cache_data
def get_dashboard_data(_engine, _assistant, inputs: dict):
    """Caches calculations to prevent redundant processing on UI re-renders."""
    breakdown = _engine.calculate_total_daily_emissions(inputs)
    recommendations = _assistant.generate_recommendations(inputs, breakdown)
    
    breakdown_data = pd.DataFrame({
        "Category": ["Commute", "Diet", "Energy"],
        "Emissions (kg CO₂)": [breakdown["commute"], breakdown["diet"], breakdown["energy"]]
    })
    
    return breakdown, recommendations, breakdown_data

# ----------------- SIDEBAR: ONBOARDING QUIZ -----------------
st.sidebar.markdown(
    '<div class="sidebar-header">🌱 TerraByte</div>',
    unsafe_allow_html=True
)
st.sidebar.markdown("### Onboarding Questionnaire")
st.sidebar.caption("Input your daily lifestyle metrics below to analyze your carbon footprint.")

# Form-like inputs with clear validation bounds
commute_dist = st.sidebar.slider(
    "Daily Commute Distance (km)",
    min_value=0.0,
    max_value=150.0,
    value=20.0,
    step=0.5,
    help="Total distance traveled round-trip per day."
)

transport_mode = st.sidebar.selectbox(
    "Primary Transport Mode",
    options=["Driving", "Public Transit", "Walking/Cycling"],
    index=0,
    help="Select the vehicle used for most of your commute."
)

diet_type = st.sidebar.selectbox(
    "Dietary Habit",
    options=["Meat-Heavy", "Balanced", "Vegetarian", "Vegan"],
    index=1,
    help="Select the pattern that best matches your daily food intake."
)

electricity_kwh = st.sidebar.slider(
    "Daily Electricity Usage (kWh)",
    min_value=0.0,
    max_value=60.0,
    value=12.0,
    step=0.5,
    help="Your share of daily electricity consumption. Average home uses ~10-20 kWh/day."
)

# Standardized baseline conversion dictionary for backend engine
transport_mapping = {
    "Driving": "driving",
    "Public Transit": "public_transit",
    "Walking/Cycling": "walking_cycling"
}

diet_mapping = {
    "Meat-Heavy": "meat_heavy",
    "Balanced": "balanced",
    "Vegetarian": "vegetarian",
    "Vegan": "vegan"
}

# Pack inputs for calculation
user_inputs = {
    "commute_distance": commute_dist,
    "transport_type": transport_mapping[transport_mode],
    "diet_type": diet_mapping[diet_type],
    "electricity_kwh": electricity_kwh
}

# ----------------- MAIN DASHBOARD -----------------
# Hero Banner Section
st.markdown(
    """
    <div class="hero-banner">
        <h1 class="hero-title">TerraByte</h1>
        <p class="hero-subtitle">Context-Aware Daily Carbon Intelligence & Micro-Action System</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Process Calculations via the cached engine
try:
    breakdown, recommendations, breakdown_data = get_dashboard_data(engine, assistant, user_inputs)
except Exception as e:
    st.error(f"Error executing emissions engine logic: {str(e)}")
    st.stop()

# Layout Configuration
col_metrics, col_actions = st.columns([1, 1.1], gap="large")

with col_metrics:
    # 1. Total Daily Footprint KPI Card
    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="kpi-title">Total Daily Carbon Footprint</div>
            <div class="kpi-value">{breakdown['total']:.2f} kg CO₂</div>
            <div class="kpi-subtitle">Estimated carbon emissions from your current daily lifestyle profile</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. National & Target Comparisons
    us_avg = 16.0
    global_target = 5.0
    
    # Calculate percentages for comparison bars
    user_pct = min(100.0, max(2.0, (breakdown['total'] / us_avg) * 100.0))
    us_pct = 100.0
    target_pct = min(100.0, max(2.0, (global_target / us_avg) * 100.0))

    st.markdown("### Benchmarks & Comparison")
    st.caption("How your daily footprint compares against standard benchmarks (kg CO₂ / day).")

    st.markdown(
        textwrap.dedent(
            f"""
            <div class="compare-container">
                <div class="bar-label">
                    <span>Your Profile</span>
                    <strong>{breakdown['total']:.2f} kg CO₂</strong>
                </div>
                <div class="bar-bg">
                    <div class="bar-fill" style="width: {user_pct}%; background: linear-gradient(90deg, #05c46b, #00d2d3);"></div>
                </div>
                <div class="bar-label">
                    <span>National Average (US Standard Benchmark)</span>
                    <strong>{us_avg:.2f} kg CO₂</strong>
                </div>
                <div class="bar-bg">
                    <div class="bar-fill" style="width: {us_pct}%; background: rgba(255, 255, 255, 0.25);"></div>
                </div>
                <div class="bar-label">
                    <span>Sustainable Global Target</span>
                    <strong>{global_target:.2f} kg CO₂</strong>
                </div>
                <div class="bar-bg">
                    <div class="bar-fill" style="width: {target_pct}%; background: #9966ff;"></div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True
    )

    # 3. Emissions Breakdown Chart
    st.markdown("### Category Distribution")
    st.bar_chart(
        data=breakdown_data.set_index("Category"), 
        color="#05c46b",
        height=250
    )


with col_actions:
    st.markdown("### 🌱 Personalized Eco-Actions")
    st.caption("Recommended micro-actions tailored specifically to reduce your highest footprint categories.")

    for rec in recommendations:
        cat = rec["category"].lower()
        impact = rec["impact_level"].lower()
        
        # Security: Escape HTML strings to prevent XSS vulnerabilities
        safe_category = html.escape(str(rec['category']))
        safe_impact = html.escape(str(rec['impact_level']))
        safe_title = html.escape(str(rec['title']))
        safe_desc = html.escape(str(rec['description']))
        safe_savings = float(rec['potential_savings'])
        
        # Select appropriate badge classes
        cat_badge_class = f"badge-{cat}" if cat in ["commute", "diet", "energy"] else "badge-general"
        impact_badge_class = f"badge-{impact}"

        st.markdown(
            f"""
            <div class="rec-card">
                <div class="rec-header">
                    <div>
                        <span class="badge {cat_badge_class}">{safe_category}</span>
                        <span class="badge {impact_badge_class}">{safe_impact} Impact</span>
                    </div>
                </div>
                <div class="rec-title">{safe_title}</div>
                <div class="rec-desc">{safe_desc}</div>
                <div class="rec-savings">
                    🌍 Estimated Savings: <strong>{safe_savings:.2f} kg CO₂/day</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Footer info
st.markdown("---")
st.caption("TerraByte runs complete computations locally with lightweight, pinned packages. Secure, private, and fully context-aware.")