"""
TerraByte Streamlit Frontend Application.
Context-Aware Daily Carbon Intelligence & Micro-Action System.
"""

import streamlit as st
import pandas as pd
import html
from src.calculator import CarbonEngine, TRANSPORT_MAPPING, DIET_MAPPING
from src.assistant import EcoAssistant

# ----------------- CONSTANTS -----------------
US_AVG_EMISSIONS = 16.0
GLOBAL_TARGET_EMISSIONS = 5.0

# ----------------- CONFIG & CACHING -----------------
st.set_page_config(
    page_title="TerraByte — Eco-Action Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def get_custom_css() -> str:
    """Caches CSS string to prevent memory reallocation on every UI rerun."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0b0c10;
        color: #e2e8f0;
        font-family: 'Outfit', sans-serif !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0f131a;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        padding-top: 2rem;
    }
    .sidebar-header {
        font-size: 1.4rem; font-weight: 700; color: #00b894; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;
    }
    .dashboard-card {
        background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 24px;
        box-shadow: 0 12px 32px 0 rgba(0, 0, 0, 0.25); margin-bottom: 24px;
    }
    .kpi-title { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; font-weight: 500; }
    .kpi-value {
        font-size: 2.8rem; font-weight: 700; line-height: 1.1; margin: 8px 0;
        background: linear-gradient(90deg, #05c46b, #00d2d3); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .kpi-subtitle { font-size: 0.85rem; color: #94a3b8; } 

    .rec-card {
        background: rgba(24, 32, 48, 0.6); border-left: 5px solid #05c46b;
        border: 1px solid rgba(255, 255, 255, 0.05); border-left-width: 5px; border-radius: 6px 16px 16px 6px;
        padding: 22px; margin-bottom: 18px; box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2);
    }
    .rec-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
    .rec-title { font-size: 1.1rem; font-weight: 600; color: #f8fafc; }
    .rec-desc { font-size: 0.95rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 14px; }
    .rec-savings { font-size: 0.9rem; font-weight: 600; color: #00d2d3; display: flex; align-items: center; gap: 6px; }

    .badge {
        display: inline-block; padding: 3px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.5px;
    }
    .badge-commute { background: rgba(54, 162, 235, 0.15); color: #36a2eb; border: 1px solid rgba(54, 162, 235, 0.3); }
    .badge-diet { background: rgba(255, 159, 64, 0.15); color: #ff9f40; border: 1px solid rgba(255, 159, 64, 0.3); }
    .badge-energy { background: rgba(255, 205, 86, 0.15); color: #ffcd56; border: 1px solid rgba(255, 205, 86, 0.3); }
    .badge-general { background: rgba(153, 102, 255, 0.15); color: #9966ff; border: 1px solid rgba(153, 102, 255, 0.3); }
    .badge-high { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-medium { background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-low { background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }

    .compare-container { margin-top: 15px; }
    .bar-label { font-size: 0.85rem; color: #94a3b8; display: flex; justify-content: space-between; margin-bottom: 4px; }
    .bar-bg { background: rgba(255, 255, 255, 0.05); border-radius: 9999px; height: 10px; overflow: hidden; margin-bottom: 12px; }
    .bar-fill { height: 100%; border-radius: 9999px; }

    .hero-banner { padding: 2.5rem 0 1.5rem 0; }
    .hero-title {
        font-size: 3rem; font-weight: 800; background: linear-gradient(135deg, #05c46b 0%, #00d2d3 50%, #9966ff 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; margin-bottom: 0px;
    }
    .hero-subtitle { font-size: 1.1rem; color: #94a3b8; margin-top: 0px; }
    </style>
    """

def inject_custom_css() -> None:
    """Injects cached custom styling for high accessibility and visual hierarchy."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

@st.cache_data
def get_dashboard_data(commute_dist: float, transport_type: str, diet_type: str, electricity_kwh: float) -> tuple:
    """Caches calculations using primitive types to prevent dictionary serialization overhead."""
    engine = CarbonEngine()
    assistant = EcoAssistant()
    
    inputs = {
        "commute_distance": commute_dist,
        "transport_type": transport_type,
        "diet_type": diet_type,
        "electricity_kwh": electricity_kwh
    }
    
    breakdown = engine.calculate_total_daily_emissions(inputs)
    recommendations = assistant.generate_recommendations(inputs, breakdown)
    
    breakdown_data = pd.DataFrame({
        "Category": ["Commute", "Diet", "Energy"],
        "Emissions (kg CO₂)": [breakdown["commute"], breakdown["diet"], breakdown["energy"]]
    })
    
    return breakdown, recommendations, breakdown_data


# ----------------- MAIN APPLICATION LOGIC -----------------
def main() -> None:
    """Main execution block for the Streamlit UI."""
    inject_custom_css()

    st.sidebar.markdown('<div class="sidebar-header">🌱 TerraByte</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 1rem;">Input your daily lifestyle metrics below.</div>', unsafe_allow_html=True)

    commute_dist = st.sidebar.slider("Daily Commute Distance (km)", 0.0, 150.0, 20.0, 0.5)
    transport_mode = st.sidebar.selectbox("Primary Transport Mode", ["Driving", "Public Transit", "Walking/Cycling"], 0)
    diet_type = st.sidebar.selectbox("Dietary Habit", ["Meat-Heavy", "Balanced", "Vegetarian", "Vegan"], 1)
    electricity_kwh = st.sidebar.slider("Daily Electricity Usage (kWh)", 0.0, 60.0, 12.0, 0.5)

    st.markdown(
        """
        <div class="hero-banner">
            <h1 class="hero-title">TerraByte</h1>
            <p class="hero-subtitle">Context-Aware Daily Carbon Intelligence & Micro-Action System</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        breakdown, recommendations, breakdown_data = get_dashboard_data(
            commute_dist, 
            TRANSPORT_MAPPING.get(transport_mode, "driving"), 
            DIET_MAPPING.get(diet_type, "balanced"), 
            electricity_kwh
        )
    except (ValueError, TypeError, KeyError) as e:
        st.error(f"Error executing logic: {str(e)}")
        return

    col_metrics, col_actions = st.columns([1, 1.1], gap="large")

    with col_metrics:
        st.markdown(
            f"""
            <div class="dashboard-card" role="region" aria-label="Carbon Footprint Summary">
                <div class="kpi-title">Total Daily Carbon Footprint</div>
                <div class="kpi-value" aria-live="polite" role="status">{breakdown['total']:.2f} kg CO₂</div>
                <div class="kpi-subtitle">Estimated carbon emissions from your current daily profile</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        user_pct = min(100.0, max(2.0, (breakdown['total'] / US_AVG_EMISSIONS) * 100.0))
        target_pct = min(100.0, max(2.0, (GLOBAL_TARGET_EMISSIONS / US_AVG_EMISSIONS) * 100.0))

        st.markdown("### Benchmarks & Comparison")
        
        # Implicit string concatenation makes this immune to IDE auto-indentation bugs!
        compare_html = (
            '<div class="compare-container">'
            f'<div class="bar-label"><span>Your Profile</span><strong>{breakdown["total"]:.2f} kg CO₂</strong></div>'
            f'<div class="bar-bg"><div class="bar-fill" role="progressbar" aria-valuenow="{user_pct}" aria-valuemin="0" aria-valuemax="100" style="width: {user_pct}%; background: linear-gradient(90deg, #05c46b, #00d2d3);"></div></div>'
            f'<div class="bar-label"><span>National Average</span><strong>{US_AVG_EMISSIONS:.2f} kg CO₂</strong></div>'
            '<div class="bar-bg"><div class="bar-fill" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%; background: rgba(255, 255, 255, 0.25);"></div></div>'
            f'<div class="bar-label"><span>Sustainable Target</span><strong>{GLOBAL_TARGET_EMISSIONS:.2f} kg CO₂</strong></div>'
            f'<div class="bar-bg"><div class="bar-fill" role="progressbar" aria-valuenow="{target_pct}" aria-valuemin="0" aria-valuemax="100" style="width: {target_pct}%; background: #9966ff;"></div></div>'
            '</div>'
        )
        st.markdown(compare_html, unsafe_allow_html=True)


        st.markdown("### Category Distribution")
        st.bar_chart(data=breakdown_data.set_index("Category"), color="#05c46b", height=250)

    with col_actions:
        st.markdown("### 🌱 Personalized Eco-Actions")
        st.caption("Recommended micro-actions tailored specifically to reduce your highest footprint categories.")

        for rec in recommendations:
            cat = rec["category"].lower()
            impact = rec["impact_level"].lower()
            
            safe_category = html.escape(str(rec['category']))
            safe_impact = html.escape(str(rec['impact_level']))
            safe_title = html.escape(str(rec['title']))
            safe_desc = html.escape(str(rec['description']))
            safe_savings = float(rec['potential_savings'])
            
            cat_badge_class = f"badge-{cat}" if cat in ["commute", "diet", "energy"] else "badge-general"
            impact_badge_class = f"badge-{impact}"

            st.markdown(
                f"""
                <div class="rec-card" role="region" aria-label="Recommendation: {safe_title}">
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

    st.markdown("---")
    st.caption("TerraByte runs complete computations locally with lightweight, pinned packages. Secure, private, and fully context-aware.")

if __name__ == "__main__":
    main()