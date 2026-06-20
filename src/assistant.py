"""
EcoAssistant module for generating context-aware ecological suggestions.
"""

from typing import Dict, List, Any
from src.calculator import COMMUTE_FACTORS, DIET_FACTORS, ELECTRICITY_FACTOR

# Configuration constants to prevent magic numbers
ENERGY_SAVINGS_RATIO = 0.15


class EcoAssistant:
    """
    EcoAssistant analyzes user carbon footprint data and generates personalized micro-actions.
    """

    def generate_recommendations(
        self, user_inputs: Dict[str, Any], emissions_breakdown: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """
        Generates up to 3 tailored recommendations based on user activities and emissions.

        Args:
            user_inputs: Dict containing 'commute_distance', 'transport_type', 'diet_type', 'electricity_kwh'.
            emissions_breakdown: Dict containing calculated category emissions.

        Returns:
            A list of dictionary recommendations containing title, description, potential savings, and impact.
        """
        if not isinstance(user_inputs, dict) or not isinstance(emissions_breakdown, dict):
            raise TypeError("Arguments must be dictionaries.")

        required_inputs = ["commute_distance", "transport_type", "diet_type", "electricity_kwh"]
        for key in required_inputs:
            if key not in user_inputs:
                raise KeyError(f"Missing input key: {key}")

        required_breakdown = ["commute", "diet", "energy", "total"]
        for key in required_breakdown:
            if key not in emissions_breakdown:
                raise KeyError(f"Missing breakdown key: {key}")

        recommendations = []

        # 1. Commute Recommendations
        commute_dist = float(user_inputs.get("commute_distance", 0.0))
        transport = str(user_inputs.get("transport_type", "driving")).strip().lower()
        
        if transport == "driving" and commute_dist > 0:
            transit_savings = max(0.0, round(commute_dist * (COMMUTE_FACTORS.get("driving", 0.20) - COMMUTE_FACTORS.get("public_transit", 0.05)), 2))
            active_savings = max(0.0, round(commute_dist * COMMUTE_FACTORS.get("driving", 0.20), 2))
            
            if commute_dist <= 5:
                recommendations.append({
                    "category": "Commute",
                    "title": "Switch to Active Commuting (Walking/Cycling)",
                    "description": (f"Since your daily commute is relatively short ({commute_dist} km), "
                                    "walking or cycling would eliminate driving emissions and improve your health."),
                    "potential_savings": active_savings,
                    "impact_level": self._get_impact_level(active_savings)
                })
            else:
                recommendations.append({
                    "category": "Commute",
                    "title": "Opt for Public Transit or Carpooling",
                    "description": (f"Your daily drive of {commute_dist} km produces a significant footprint. "
                                    "Switching to public transit would drastically reduce this category's emissions."),
                    "potential_savings": transit_savings,
                    "impact_level": self._get_impact_level(transit_savings)
                })
        elif transport == "public_transit" and commute_dist > 5:
            active_savings = max(0.0, round(commute_dist * COMMUTE_FACTORS.get("public_transit", 0.05), 2))
            recommendations.append({
                "category": "Commute",
                "title": "Incorporate Walk/Cycle for Part of Your Commute",
                "description": (f"You already use public transit for {commute_dist} km daily. Walking or cycling the first/last "
                                "mile can trim your footprint to zero while getting some exercise."),
                "potential_savings": active_savings,
                "impact_level": self._get_impact_level(active_savings)
            })

        # 2. Diet Recommendations
        diet = str(user_inputs.get("diet_type", "balanced")).strip().lower()
        if diet == "meat_heavy":
            savings = max(0.0, round(DIET_FACTORS.get("meat_heavy", 3.3) - DIET_FACTORS.get("vegetarian", 2.0), 2))
            recommendations.append({
                "category": "Diet",
                "title": "Introduce Meatless Days",
                "description": "Transitioning to vegetarian options just a few days a week can dramatically lower dietary emissions.",
                "potential_savings": savings,
                "impact_level": self._get_impact_level(savings)
            })
        elif diet == "balanced":
            savings = max(0.0, round(DIET_FACTORS.get("balanced", 2.5) - DIET_FACTORS.get("vegetarian", 2.0), 2))
            recommendations.append({
                "category": "Diet",
                "title": "Try Vegetarian Substitutions",
                "description": "Substituting plant proteins for poultry/pork helps lower greenhouse gas intensity.",
                "potential_savings": savings,
                "impact_level": self._get_impact_level(savings)
            })
        elif diet == "vegetarian":
            savings = max(0.0, round(DIET_FACTORS.get("vegetarian", 2.0) - DIET_FACTORS.get("vegan", 1.5), 2))
            recommendations.append({
                "category": "Diet",
                "title": "Explore Vegan / Plant-Based Alternatives",
                "description": "Reducing dairy and eggs by swapping them for plant-based milks further lowers your impact.",
                "potential_savings": savings,
                "impact_level": self._get_impact_level(savings)
            })

        # 3. Energy Recommendations
        electricity = float(user_inputs.get("electricity_kwh", 0.0))
        if electricity > 0:
            savings = max(0.0, round(electricity * ENERGY_SAVINGS_RATIO * ELECTRICITY_FACTOR, 2))
            if savings > 0.05:
                recommendations.append({
                    "category": "Energy",
                    "title": "Optimize Daily Electricity Consumption",
                    "description": (f"Adopting energy-efficient habits can cut your {electricity} kWh energy footprint by {int(ENERGY_SAVINGS_RATIO * 100)}%."),
                    "potential_savings": savings,
                    "impact_level": self._get_impact_level(savings)
                })

        if not recommendations:
            recommendations.append({
                "category": "General",
                "title": "Share Your Sustainable Habits",
                "description": "Your lifestyle emissions are extremely low. Inspire others to adopt a carbon-conscious lifestyle.",
                "potential_savings": 0.0,
                "impact_level": "Low"
            })

        recommendations.sort(key=lambda x: x["potential_savings"], reverse=True)
        return recommendations[:3]

    def _get_impact_level(self, savings: float) -> str:
        """
        Determines the visual impact level of carbon savings.
        
        Args:
            savings: The calculated potential savings in kg CO2.
            
        Returns:
            A string representing the impact level ('Low', 'Medium', 'High').
        """
        if savings <= 0.5:
            return "Low"
        elif savings <= 2.0:
            return "Medium"
        else:
            return "High"