"""
TerraByte Streamlit Frontend Application.
Author: Expert Streamlit Developer
"""

import streamlit as st
import pandas as pd
import textwrap
from src.calculator import CarbonEngine
from src.assistant import EcoAssistant

# Set page configuration for a premium look
st.set_page_config(
    page_title="TerraByte — Eco-Action Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling & Typography
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Global Typography */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0b0c10;
        color: #e2e8f0;
        font-family: 'Outfit', sans-serif !important;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #0f131a;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        padding-top: 2rem;
    }
    .sidebar-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #00b894;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Glassmorphic Container/Card */
    .dashboard-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 12px 32px 0 rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(12px);
        margin-bottom: 24px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .dashboard-card:hover {
        transform: translateY(-2px);
        border-color: rgba(5, 196, 107, 0.3);
    }

    /* KPI Metrics Styling */
    .kpi-title {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94a3b8;
        font-weight: 500;
    }
    .kpi-value {
        font-size: 2.8rem;
        font-weight: 700;
        line-height: 1.1;
        margin: 8px 0;
        background: linear-gradient(90deg, #05c46b, #00d2d3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .kpi-subtitle {
        font-size: 0.85rem;
        color: #64748b;
    }

    /* Recommendation Card Styling */
    .rec-card {
        background: rgba(24, 32, 48, 0.6);
        border-left: 5px solid #05c46b;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 6px 16px 16px 6px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .rec-card:hover {
        border-left-width: 8px;
        background: rgba(30, 41, 59, 0.7);
        transform: translateX(4px);
    }
    .rec-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .rec-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f8fafc;
    }
    .rec-desc {
        font-size: 0.95rem;
        color: #cbd5e1;
        line-height: 1.5;
        margin-bottom: 14px;
    }
    .rec-savings {
        font-size: 0.9rem;
        font-weight: 600;
        color: #00d2d3;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Custom Badges */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-commute {
        background: rgba(54, 162, 235, 0.15);
        color: #36a2eb;
        border: 1px solid rgba(54, 162, 235, 0.3);
    }
    .badge-diet {
        background: rgba(255, 159, 64, 0.15);
        color: #ff9f40;
        border: 1px solid rgba(255, 159, 64, 0.3);
    }
    .badge-energy {
        background: rgba(255, 205, 86, 0.15);
        color: #ffcd56;
        border: 1px solid rgba(255, 205, 86, 0.3);
    }
    .badge-general {
        background: rgba(153, 102, 255, 0.15);
        color: #9966ff;
        border: 1px solid rgba(153, 102, 255, 0.3);
    }

    .badge-high {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .badge-medium {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-low {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    /* Comparison Bar Chart */
    .compare-container {
        margin-top: 15px;
    }
    .bar-label {
        font-size: 0.85rem;
        color: #94a3b8;
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
    }
    .bar-bg {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 9999px;
        height: 10px;
        overflow: hidden;
        margin-bottom: 12px;
    }
    .bar-fill {
        height: 100%;
        border-radius: 9999px;
    }

    /* Decorative header gradient */
    .hero-banner {
        padding: 2.5rem 0 1.5rem 0;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #05c46b 0%, #00d2d3 50%, #9966ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-top: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Backend Engines safely
try:
    engine = CarbonEngine()
    assistant = EcoAssistant()
except Exception as e:
    st.error(f"Failed to initialize calculation engines: {str(e)}")
    st.stop()

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

# Process Calculations
try:
    breakdown = engine.calculate_total_daily_emissions(user_inputs)
    recommendations = assistant.generate_recommendations(user_inputs, breakdown)
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
    # Baseline benchmark: US average = 16.0 kg/day, Global average target = 5.0 kg/day.
    us_avg = 16.0
    global_target = 5.0
    
    # Calculate percentages for comparison bars (clamp between 2% and 100% for aesthetic render)
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

    # 3. Emissions Breakdown Breakdown
    st.markdown("### Category Distribution")
    breakdown_data = pd.DataFrame({
        "Category": ["Commute", "Diet", "Energy"],
        "Emissions (kg CO₂)": [breakdown["commute"], breakdown["diet"], breakdown["energy"]]
    })
    
    # Simple table display using clean Streamlit layout
    st.table(breakdown_data)


with col_actions:
    st.markdown("### 🌱 Personalized Eco-Actions")
    st.caption("Recommended micro-actions tailored specifically to reduce your highest footprint categories.")

    for rec in recommendations:
        cat = rec["category"].lower()
        impact = rec["impact_level"].lower()
        
        # Select appropriate badge classes
        cat_badge_class = f"badge-{cat}" if cat in ["commute", "diet", "energy"] else "badge-general"
        impact_badge_class = f"badge-{impact}"

        st.markdown(
            f"""
            <div class="rec-card">
                <div class="rec-header">
                    <div>
                        <span class="badge {cat_badge_class}">{rec['category']}</span>
                        <span class="badge {impact_badge_class}">{rec['impact_level']} Impact</span>
                    </div>
                </div>
                <div class="rec-title">{rec['title']}</div>
                <div class="rec-desc">{rec['description']}</div>
                <div class="rec-savings">
                    🌍 Estimated Savings: <strong>{rec['potential_savings']:.2f} kg CO₂/day</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Footer info
st.markdown("---")
st.caption("TerraByte runs complete computations locally with lightweight, pinned packages. Secure, private, and fully context-aware.")
