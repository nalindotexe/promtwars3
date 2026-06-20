"""
EcoAssistant module for generating context-aware ecological suggestions.
"""

from typing import Dict, List, Any

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
                raise ValueError(f"Missing input key: {key}")

        required_breakdown = ["commute", "diet", "energy", "total"]
        for key in required_breakdown:
            if key not in emissions_breakdown:
                raise ValueError(f"Missing breakdown key: {key}")

        recommendations = []

        # 1. Commute Recommendations
        commute_dist = user_inputs["commute_distance"]
        transport = str(user_inputs["transport_type"]).strip().lower()
        if transport == "driving" and commute_dist > 0:
            transit_savings = round(commute_dist * (0.20 - 0.05), 2)
            active_savings = round(commute_dist * 0.20, 2)
            
            if commute_dist <= 5:
                recommendations.append({
                    "category": "Commute",
                    "title": "Switch to Active Commuting (Walking/Cycling)",
                    "description": (
                        f"Since your daily commute is relatively short ({commute_dist} km), "
                        "walking or cycling would eliminate driving emissions and improve your health."
                    ),
                    "potential_savings": active_savings,
                    "impact_level": self._get_impact_level(active_savings)
                })
            else:
                recommendations.append({
                    "category": "Commute",
                    "title": "Opt for Public Transit or Carpooling",
                    "description": (
                        f"Your daily drive of {commute_dist} km produces a significant footprint. "
                        "Switching to public transit would reduce this category's emissions by 75%."
                    ),
                    "potential_savings": transit_savings,
                    "impact_level": self._get_impact_level(transit_savings)
                })
        elif transport == "public_transit" and commute_dist > 5:
            active_savings = round(commute_dist * 0.05, 2)
            recommendations.append({
                "category": "Commute",
                "title": "Incorporate Walk/Cycle for Part of Your Commute",
                "description": (
                    f"You already use public transit for {commute_dist} km daily. Walking or cycling the first/last "
                    "mile can trim your footprint to zero while getting some exercise."
                ),
                "potential_savings": active_savings,
                "impact_level": self._get_impact_level(active_savings)
            })

        # 2. Diet Recommendations
        diet = str(user_inputs["diet_type"]).strip().lower()
        if diet == "meat_heavy":
            savings = 1.3  # Meat-heavy (3.3) to Vegetarian (2.0)
            recommendations.append({
                "category": "Diet",
                "title": "Introduce Meatless Days",
                "description": (
                    "A meat-heavy diet has a high carbon footprint. Transitioning to vegetarian options "
                    "just a few days a week can dramatically lower your annual dietary emissions."
                ),
                "potential_savings": savings,
                "impact_level": self._get_impact_level(savings)
            })
        elif diet == "balanced":
            savings = 0.5  # Balanced (2.5) to Vegetarian (2.0)
            recommendations.append({
                "category": "Diet",
                "title": "Try Vegetarian Substitutions",
                "description": (
                    "Transitioning from a balanced diet to vegetarian meals (e.g., substituting plant proteins "
                    "for poultry/pork) helps lower greenhouse gas intensity."
                ),
                "potential_savings": savings,
                "impact_level": self._get_impact_level(savings)
            })
        elif diet == "vegetarian":
            savings = 0.5  # Vegetarian (2.0) to Vegan (1.5)
            recommendations.append({
                "category": "Diet",
                "title": "Explore Vegan / Plant-Based Alternatives",
                "description": (
                    "You're already doing great as a vegetarian! Reducing dairy and eggs by swapping them "
                    "for plant-based milks and cheeses further lowers your daily impact."
                ),
                "potential_savings": savings,
                "impact_level": self._get_impact_level(savings)
            })

        # 3. Energy Recommendations
        electricity = user_inputs["electricity_kwh"]
        if electricity > 0:
            # Estimate 15% daily savings from smart habits
            savings = round(electricity * 0.15 * 0.40, 2)
            if savings > 0.05:
                recommendations.append({
                    "category": "Energy",
                    "title": "Optimize Daily Electricity Consumption",
                    "description": (
                        f"Based on your daily electricity usage of {electricity} kWh, adopting energy-efficient "
                        "habits (LED lighting, turning off standby devices, eco-mode on appliances) can cut "
                        "your energy footprint by 15%."
                    ),
                    "potential_savings": savings,
                    "impact_level": self._get_impact_level(savings)
                })

        # Fallback if no recommendation generated
        if not recommendations:
            recommendations.append({
                "category": "General",
                "title": "Share Your Sustainable Habits",
                "description": (
                    "Incredible! Your lifestyle emissions are extremely low. Spread the word and inspire "
                    "others to adopt a carbon-conscious lifestyle."
                ),
                "potential_savings": 0.0,
                "impact_level": "Low"
            })

        # Sort recommendations by potential savings in descending order and limit to top 3
        recommendations.sort(key=lambda x: x["potential_savings"], reverse=True)
        return recommendations[:3]

    def _get_impact_level(self, savings: float) -> str:
        """Determines the visual impact level of carbon savings."""
        if savings <= 0.5:
            return "Low"
        elif savings <= 2.0:
            return "Medium"
        else:
            return "High"