"""
Medical Disclaimer Generator
"""


class DisclaimerGenerator:
    """Generates appropriate medical disclaimers"""
    
    GENERAL_DISCLAIMER = (
        "💚 **Medical Disclaimer**: I'm not a doctor. This is general information "
        "and not a substitute for professional medical advice. If you're concerned, "
        "please contact a healthcare professional."
    )
    
    REMEDY_DISCLAIMER = (
        "⚠️ **Important**: These are home remedies for minor conditions only. "
        "This is not medical advice. If symptoms are severe, worsening, or persistent, "
        "please consult a healthcare professional."
    )
    
    EMERGENCY_DISCLAIMER = (
        "🚨 **Emergency**: Based on your symptoms, you should seek immediate medical attention. "
        "Call emergency services or go to the nearest emergency room. Do not rely on home remedies."
    )
    
    @classmethod
    def get_disclaimer(cls, context: str = 'general') -> str:
        """Get appropriate disclaimer based on context"""
        disclaimers = {
            'general': cls.GENERAL_DISCLAIMER,
            'remedy': cls.REMEDY_DISCLAIMER,
            'emergency': cls.EMERGENCY_DISCLAIMER,
        }
        
        return disclaimers.get(context, cls.GENERAL_DISCLAIMER)
