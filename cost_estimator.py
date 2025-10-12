"""
Cost Estimator Module - For Car Damage Repair Cost Estimation
This file is for your friend who is doing the cost estimation
"""

import random
from typing import Dict, List

class CarRepairCostEstimator:
    """Car repair cost estimation system."""
    
    def __init__(self):
        self.damage_type_costs = {
            'low': {
                'Scratch': (150, 400),
                'Paint Damage': (200, 500),
                'Minor Dent': (300, 600),
                'Bumper Scrape': (250, 450)
            },
            'moderate': {
                'Dent': (500, 1200),
                'Bumper Damage': (400, 1000),
                'Headlight Damage': (300, 800),
                'Door Damage': (600, 1500)
            },
            'heavy': {
                'Major Dent': (1500, 4000),
                'Broken Glass': (800, 2000),
                'Structural Damage': (2000, 8000),
                'Engine Damage': (3000, 10000)
            }
        }
        
        self.labor_rates = {
            'low': 50,      # $50/hour
            'moderate': 75, # $75/hour
            'heavy': 100    # $100/hour
        }
        
        self.parts_markup = 1.3  # 30% markup on parts
    
    def estimate_repair_cost(self, damage_severity: str, damage_type: str, confidence: float) -> Dict:
        """Estimate repair cost based on damage assessment."""
        
        # Get base cost range
        if damage_severity in self.damage_type_costs:
            if damage_type in self.damage_type_costs[damage_severity]:
                min_cost, max_cost = self.damage_type_costs[damage_severity][damage_type]
            else:
                # Use average for severity if specific type not found
                all_costs = list(self.damage_type_costs[damage_severity].values())
                min_cost = sum(cost[0] for cost in all_costs) // len(all_costs)
                max_cost = sum(cost[1] for cost in all_costs) // len(all_costs)
        else:
            # Default costs
            min_cost, max_cost = 500, 2000
        
        # Adjust based on confidence
        confidence_factor = 0.8 + (confidence * 0.4)  # 0.8 to 1.2
        adjusted_min = int(min_cost * confidence_factor)
        adjusted_max = int(max_cost * confidence_factor)
        
        # Add labor costs
        labor_hours = self.get_labor_hours(damage_severity, damage_type)
        labor_rate = self.labor_rates.get(damage_severity, 75)
        labor_cost = labor_hours * labor_rate
        
        # Calculate parts cost
        parts_cost = random.randint(adjusted_min, adjusted_max)
        total_parts_cost = int(parts_cost * self.parts_markup)
        
        # Total cost
        total_cost = total_parts_cost + labor_cost
        
        # Add taxes and fees (8-12%)
        tax_rate = random.uniform(0.08, 0.12)
        final_cost = int(total_cost * (1 + tax_rate))
        
        return {
            "estimated_cost": final_cost,
            "parts_cost": total_parts_cost,
            "labor_cost": labor_cost,
            "labor_hours": labor_hours,
            "tax_rate": round(tax_rate * 100, 1),
            "confidence_adjustment": round(confidence_factor, 2),
            "cost_breakdown": {
                "parts": total_parts_cost,
                "labor": labor_cost,
                "taxes": int(total_cost * tax_rate),
                "total": final_cost
            }
        }
    
    def get_labor_hours(self, severity: str, damage_type: str) -> int:
        """Estimate labor hours based on damage."""
        base_hours = {
            'low': (1, 3),
            'moderate': (3, 8),
            'heavy': (8, 20)
        }
        
        min_hours, max_hours = base_hours.get(severity, (2, 6))
        
        # Adjust based on damage type
        if 'glass' in damage_type.lower():
            min_hours += 1
            max_hours += 2
        elif 'structural' in damage_type.lower():
            min_hours += 5
            max_hours += 10
        
        return random.randint(min_hours, max_hours)
    
    def get_cost_estimate_details(self, damage_severity: str, damage_type: str, confidence: float) -> Dict:
        """Get detailed cost estimate with breakdown."""
        cost_estimate = self.estimate_repair_cost(damage_severity, damage_type, confidence)
        
        # Add market comparison
        market_comparison = self.get_market_comparison(cost_estimate["estimated_cost"], damage_severity)
        
        # Add time estimate
        time_estimate = self.get_repair_time_estimate(damage_severity, damage_type)
        
        return {
            **cost_estimate,
            "market_comparison": market_comparison,
            "repair_time_estimate": time_estimate,
            "recommendations": self.get_repair_recommendations(damage_severity, cost_estimate["estimated_cost"])
        }
    
    def get_market_comparison(self, estimated_cost: int, severity: str) -> Dict:
        """Compare estimated cost with market averages."""
        market_averages = {
            'low': (200, 800),
            'moderate': (800, 2500),
            'heavy': (2500, 8000)
        }
        
        min_market, max_market = market_averages.get(severity, (500, 2000))
        market_avg = (min_market + max_market) / 2
        
        if estimated_cost < min_market:
            comparison = "Below market average"
            percentage = round(((min_market - estimated_cost) / min_market) * 100, 1)
        elif estimated_cost > max_market:
            comparison = "Above market average"
            percentage = round(((estimated_cost - max_market) / max_market) * 100, 1)
        else:
            comparison = "Within market range"
            percentage = 0
        
        return {
            "market_average": int(market_avg),
            "market_range": f"${min_market:,} - ${max_market:,}",
            "comparison": comparison,
            "percentage_difference": percentage
        }
    
    def get_repair_time_estimate(self, severity: str, damage_type: str) -> Dict:
        """Estimate repair time."""
        base_days = {
            'low': (1, 3),
            'moderate': (3, 7),
            'heavy': (7, 21)
        }
        
        min_days, max_days = base_days.get(severity, (2, 5))
        
        # Adjust for specific damage types
        if 'glass' in damage_type.lower():
            min_days += 1
        elif 'structural' in damage_type.lower():
            min_days += 3
            max_days += 7
        
        return {
            "estimated_days": f"{min_days}-{max_days}",
            "min_days": min_days,
            "max_days": max_days,
            "urgency": "High" if severity == 'heavy' else "Medium" if severity == 'moderate' else "Low"
        }
    
    def get_repair_recommendations(self, severity: str, cost: int) -> List[str]:
        """Get repair recommendations based on damage and cost."""
        recommendations = []
        
        if severity == 'low' and cost < 500:
            recommendations.append("Consider DIY repair for minor damage")
            recommendations.append("Get multiple quotes for comparison")
        elif severity == 'moderate':
            recommendations.append("Professional repair recommended")
            recommendations.append("Check insurance coverage")
        elif severity == 'heavy':
            recommendations.append("Immediate professional assessment required")
            recommendations.append("Consider insurance claim")
            recommendations.append("Get detailed inspection report")
        
        if cost > 5000:
            recommendations.append("Consider total loss evaluation")
            recommendations.append("Document all damage thoroughly")
        
        return recommendations

# Global cost estimator instance
cost_estimator = CarRepairCostEstimator()

def estimate_repair_cost(damage_severity: str, damage_type: str, confidence: float) -> Dict:
    """Main function to estimate repair cost - call this from app.py"""
    return cost_estimator.get_cost_estimate_details(damage_severity, damage_type, confidence)
