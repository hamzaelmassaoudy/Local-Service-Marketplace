import random

class AIService:
    """
    Service to handle AI logic.
    Currently uses Mock Logic. 
    """

    @staticmethod
    def estimate_price(description):
        # Mock logic to simulate AI analysis
        base_price = 50.0
        if "leak" in description.lower() or "urgent" in description.lower():
            return {
                "estimated_min": 80, 
                "estimated_max": 120, 
                "reasoning": "Urgent repair detected based on keywords."
            }
        return {
            "estimated_min": 40, 
            "estimated_max": 60, 
            "reasoning": "Standard maintenance job."
        }