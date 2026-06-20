"""
Unit tests for TerraByte calculator and assistant engines.
Run using: pytest tests/test_assistant.py
"""

import pytest
from src.calculator import CarbonEngine
from src.assistant import EcoAssistant


def test_calculator_emissions():
    """Validates that CarbonEngine outputs correct mathematical calculations for basic profiles."""
    engine = CarbonEngine()

    # Case 1: Standard Balanced Commuter Profile
    inputs = {
        "commute_distance": 25.0,
        "transport_type": "driving",
        "diet_type": "balanced",
        "electricity_kwh": 10.0
    }
    
    breakdown = engine.calculate_total_daily_emissions(inputs)
    
    # Assert breakdown elements
    # 25 km driving * 0.20 = 5.0 kg CO2
    assert breakdown["commute"] == 5.0
    # Balanced diet = 2.5 kg CO2
    assert breakdown["diet"] == 2.5
    # 10 kWh energy * 0.40 = 4.0 kg CO2
    assert breakdown["energy"] == 4.0
    # Total = 5.0 + 2.5 + 4.0 = 11.5 kg CO2
    assert breakdown["total"] == 11.5


def test_calculator_edge_cases():
    """Validates boundary inputs, type mismatches, and negative checks in CarbonEngine."""
    engine = CarbonEngine()

    # Negative commute distance should raise ValueError
    with pytest.raises(ValueError, match="cannot be negative"):
        engine.calculate_commute_emissions(-10, "driving")

    # Invalid transport type should raise ValueError
    with pytest.raises(ValueError, match="Unknown transport type"):
        engine.calculate_commute_emissions(15, "rocketship")

    # Type mismatch for commute distance should raise TypeError
    with pytest.raises(TypeError, match="must be a numeric value"):
        engine.calculate_commute_emissions("fifteen", "driving")

    # Invalid diet type should raise ValueError
    with pytest.raises(ValueError, match="Unknown diet type"):
        engine.calculate_diet_emissions("junk_food")

    # Negative electricity should raise ValueError
    with pytest.raises(ValueError, match="cannot be negative"):
        engine.calculate_energy_emissions(-5.0)


def test_assistant_recommendations():
    """Validates that EcoAssistant returns appropriate context-aware advice based on user profiles."""
    engine = CarbonEngine()
    assistant = EcoAssistant()

    # Case 1: High Emission Driving Meat-Heavy Profile
    inputs = {
        "commute_distance": 40.0,
        "transport_type": "driving",
        "diet_type": "meat_heavy",
        "electricity_kwh": 20.0
    }
    breakdown = engine.calculate_total_daily_emissions(inputs)
    recs = assistant.generate_recommendations(inputs, breakdown)

    # Should return at least 2 recommendations
    assert len(recs) >= 2
    
    # Verify categories present in recommendations
    categories = [r["category"] for r in recs]
    assert "Commute" in categories
    assert "Diet" in categories
    assert "Energy" in categories

    # Verify that the recommendations are sorted by potential savings descending
    assert recs[0]["potential_savings"] >= recs[1]["potential_savings"]

    # Case 2: Already exceptionally green profile (active transport, vegan, no energy use)
    green_inputs = {
        "commute_distance": 5.0,
        "transport_type": "walking_cycling",
        "diet_type": "vegan",
        "electricity_kwh": 0.0
    }
    green_breakdown = engine.calculate_total_daily_emissions(green_inputs)
    green_recs = assistant.generate_recommendations(green_inputs, green_breakdown)

    assert len(green_recs) == 1
    assert green_recs[0]["category"] == "General"
    assert "Share Your Sustainable Habits" in green_recs[0]["title"]