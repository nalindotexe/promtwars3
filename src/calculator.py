"""
CarbonEngine module for calculating daily carbon footprint emissions.
"""

from typing import Union, Dict

# Constants for daily emission factors (kg CO2 per unit)
COMMUTE_FACTORS = {
    "driving": 0.20,         # kg CO2 per km
    "public_transit": 0.05,  # kg CO2 per km
    "walking_cycling": 0.00  # kg CO2 per km
}

DIET_FACTORS = {
    "vegan": 1.5,            # kg CO2 per day
    "vegetarian": 2.0,       # kg CO2 per day
    "balanced": 2.5,         # kg CO2 per day
    "meat_heavy": 3.3        # kg CO2 per day
}

# Grid average electricity factor (kg CO2 per kWh)
ELECTRICITY_FACTOR = 0.40


class CarbonEngine:
    """
    Engine to calculate carbon emissions for daily activities based on standard baseline factors.
    """

    def __init__(self) -> None:
        """Initializes the CarbonEngine with baseline configurations."""
        self.commute_factors = COMMUTE_FACTORS
        self.diet_factors = DIET_FACTORS
        self.electricity_factor = ELECTRICITY_FACTOR

    def calculate_commute_emissions(self, distance_km: Union[int, float], transport_type: str) -> float:
        """
        Calculate daily emissions from commuting.

        Args:
            distance_km: Daily distance in kilometers. Must be non-negative.
            transport_type: Mode of transport ('driving', 'public_transit', 'walking_cycling').

        Returns:
            Emissions in kg CO2.
        """
        if not isinstance(distance_km, (int, float)):
            raise TypeError("Commute distance must be a numeric value.")
        if distance_km < 0:
            raise ValueError("Commute distance cannot be negative.")
        
        normalized_transport = str(transport_type).strip().lower()
        if normalized_transport not in self.commute_factors:
            raise ValueError(
                f"Unknown transport type: '{transport_type}'. "
                f"Supported types: {list(self.commute_factors.keys())}"
            )
        
        factor = self.commute_factors[normalized_transport]
        return float(distance_km * factor)

    def calculate_diet_emissions(self, diet_type: str) -> float:
        """
        Calculate daily emissions from diet.

        Args:
            diet_type: Type of diet ('vegan', 'vegetarian', 'balanced', 'meat_heavy').

        Returns:
            Emissions in kg CO2.
        """
        if not isinstance(diet_type, str):
            raise TypeError("Diet type must be a string.")
            
        normalized_diet = diet_type.strip().lower()
        if normalized_diet not in self.diet_factors:
            raise ValueError(
                f"Unknown diet type: '{diet_type}'. "
                f"Supported types: {list(self.diet_factors.keys())}"
            )
            
        return float(self.diet_factors[normalized_diet])

    def calculate_energy_emissions(self, electricity_kwh: Union[int, float]) -> float:
        """
        Calculate daily emissions from electricity consumption.

        Args:
            electricity_kwh: Daily electricity consumption in kWh. Must be non-negative.

        Returns:
            Emissions in kg CO2.
        """
        if not isinstance(electricity_kwh, (int, float)):
            raise TypeError("Electricity usage must be a numeric value.")
        if electricity_kwh < 0:
            raise ValueError("Electricity usage cannot be negative.")
            
        return float(electricity_kwh * self.electricity_factor)

    def calculate_total_daily_emissions(self, inputs: Dict[str, Union[str, int, float]]) -> Dict[str, float]:
        """
        Calculate comprehensive daily emissions breakdown and total.

        Args:
            inputs: Dictionary containing:
                - 'commute_distance': float/int
                - 'transport_type': str
                - 'diet_type': str
                - 'electricity_kwh': float/int

        Returns:
            A dictionary with breakdown: commute, diet, energy, and total.
        """
        if not isinstance(inputs, dict):
            raise TypeError("Inputs must be a dictionary.")

        # Check for missing keys
        required_keys = ["commute_distance", "transport_type", "diet_type", "electricity_kwh"]
        for key in required_keys:
            if key not in inputs:
                raise ValueError(f"Missing required input key: '{key}'")

        commute = self.calculate_commute_emissions(inputs["commute_distance"], inputs["transport_type"])
        diet = self.calculate_diet_emissions(inputs["diet_type"])
        energy = self.calculate_energy_emissions(inputs["electricity_kwh"])
        total = commute + diet + energy

        return {
            "commute": round(commute, 2),
            "diet": round(diet, 2),
            "energy": round(energy, 2),
            "total": round(total, 2)
        }