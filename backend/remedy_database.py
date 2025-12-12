"""
Remedy Database - Evidence-based home remedies with safety information
"""

from typing import List, Dict, Optional


class Remedy:
    """Single home remedy with all safety information"""
    
    def __init__(
        self,
        name: str,
        steps: List[str],
        rationale: str,
        precautions: List[str],
        avoid_if: List[str] = None,
        safe_for_pregnancy: bool = True,
        safe_for_children: bool = True,
        min_age: int = 0
    ):
        self.name = name
        self.steps = steps
        self.rationale = rationale
        self.precautions = precautions
        self.avoid_if = avoid_if or []
        self.safe_for_pregnancy = safe_for_pregnancy
        self.safe_for_children = safe_for_children
        self.min_age = min_age
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'steps': self.steps,
            'rationale': self.rationale,
            'precautions': self.precautions,
            'avoid_if': self.avoid_if,
            'safe_for_pregnancy': self.safe_for_pregnancy,
            'safe_for_children': self.safe_for_children,
            'min_age': self.min_age
        }


class RemedyDatabase:
    """Database of evidence-based home remedies categorized by symptom"""
    
    # Common cold and congestion remedies
    COLD_REMEDIES = [
        Remedy(
            name="Warm Salt Water Gargle",
            steps=[
                "Mix 1/4 to 1/2 teaspoon of salt in a glass of warm water",
                "Gargle for 30 seconds, then spit out",
                "Repeat 2-3 times daily"
            ],
            rationale="Helps reduce throat inflammation and clear mucus",
            precautions=["Don't swallow the salt water", "Use warm (not hot) water"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=6
        ),
        Remedy(
            name="Steam Inhalation",
            steps=[
                "Boil water and pour into a large bowl",
                "Lean over the bowl with a towel over your head",
                "Breathe in the steam for 5-10 minutes"
            ],
            rationale="Helps loosen congestion and soothe airways",
            precautions=["Keep face at safe distance to avoid burns", "Adult supervision required for children"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=12
        ),
        Remedy(
            name="Honey and Warm Water",
            steps=[
                "Mix 1-2 teaspoons of honey in a cup of warm water or tea",
                "Drink slowly",
                "Can be taken 2-3 times daily"
            ],
            rationale="Honey has natural antibacterial properties and can soothe throat irritation",
            precautions=["Not for children under 1 year", "Check for honey allergies"],
            avoid_if=["honey allergy"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=1
        ),
        Remedy(
            name="Stay Hydrated",
            steps=[
                "Drink 8-10 glasses of water throughout the day",
                "Include warm liquids like herbal tea or broth",
                "Avoid caffeinated or alcoholic beverages"
            ],
            rationale="Fluids help thin mucus and prevent dehydration",
            precautions=["Sip slowly if nauseous"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=0
        )
    ]
    
    # Headache remedies
    HEADACHE_REMEDIES = [
        Remedy(
            name="Cold Compress",
            steps=[
                "Wrap ice pack or cold cloth in a towel",
                "Apply to forehead or back of neck",
                "Keep on for 15-20 minutes"
            ],
            rationale="Helps reduce inflammation and numb pain",
            precautions=["Don't apply ice directly to skin"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=0
        ),
        Remedy(
            name="Rest in Dark, Quiet Room",
            steps=[
                "Find a quiet, dark space",
                "Lie down and close your eyes",
                "Rest for 20-30 minutes"
            ],
            rationale="Reduces sensory stimulation that can worsen headaches",
            precautions=["If headache is severe or sudden, seek medical care"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=0
        ),
        Remedy(
            name="Gentle Neck Stretches",
            steps=[
                "Slowly tilt head toward each shoulder",
                "Gently rotate head in circles",
                "Hold each stretch for 10 seconds"
            ],
            rationale="Relieves tension that may be causing headache",
            precautions=["Move slowly and gently", "Stop if pain increases"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=10
        ),
        Remedy(
            name="Peppermint or Lavender Oil",
            steps=[
                "Apply a small amount of diluted oil to temples",
                "Gently massage in circular motions",
                "Breathe deeply"
            ],
            rationale="Essential oils may have calming and pain-relieving properties",
            precautions=["Dilute essential oils before skin contact", "Avoid if allergic"],
            avoid_if=["essential oil allergy", "sensitive skin"],
            safe_for_pregnancy=False,
            safe_for_children=True,
            min_age=12
        )
    ]
    
    # Upset stomach remedies
    STOMACH_REMEDIES = [
        Remedy(
            name="Ginger Tea",
            steps=[
                "Slice fresh ginger root (about 1 inch)",
                "Steep in hot water for 5-10 minutes",
                "Sip slowly"
            ],
            rationale="Ginger has anti-nausea properties and aids digestion",
            precautions=["Start with small amounts", "Avoid if you have GERD"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=2
        ),
        Remedy(
            name="BRAT Diet",
            steps=[
                "Eat bland foods: Bananas, Rice, Applesauce, Toast",
                "Start with small portions",
                "Gradually return to normal diet as you feel better"
            ],
            rationale="Easy-to-digest foods that are gentle on the stomach",
            precautions=["Only temporary - not nutritionally complete", "Stay hydrated"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=1
        ),
        Remedy(
            name="Chamomile Tea",
            steps=[
                "Steep chamomile tea bag in hot water for 5 minutes",
                "Let cool slightly",
                "Drink 2-3 times daily"
            ],
            rationale="Chamomile has anti-inflammatory and calming properties",
            precautions=["Check for chamomile/ragweed allergies"],
            avoid_if=["chamomile allergy", "ragweed allergy"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=6
        )
    ]
    
    # Minor cuts and scrapes
    WOUND_REMEDIES = [
        Remedy(
            name="Clean and Dress Wound",
            steps=[
                "Wash hands thoroughly",
                "Rinse wound with clean water for 5 minutes",
                "Apply antibiotic ointment if available",
                "Cover with clean bandage"
            ],
            rationale="Prevents infection and promotes healing",
            precautions=["Change bandage daily", "Watch for signs of infection (redness, swelling, pus)"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=0
        ),
        Remedy(
            name="Honey Dressing (for minor wounds)",
            steps=[
                "Clean wound thoroughly",
                "Apply thin layer of medical-grade honey",
                "Cover with clean bandage"
            ],
            rationale="Honey has natural antibacterial properties",
            precautions=["Only for minor wounds", "Watch for signs of infection"],
            avoid_if=["honey allergy"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=1
        )
    ]
    
    # Muscle pain
    MUSCLE_PAIN_REMEDIES = [
        Remedy(
            name="Warm Compress",
            steps=[
                "Soak cloth in warm water or use heating pad",
                "Apply to sore muscle for 15-20 minutes",
                "Repeat 3-4 times daily"
            ],
            rationale="Heat increases blood flow and relaxes tight muscles",
            precautions=["Use warm, not hot", "Don't fall asleep with heating pad"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=0
        ),
        Remedy(
            name="Gentle Stretching",
            steps=[
                "Slowly stretch the affected muscle",
                "Hold stretch for 15-30 seconds",
                "Repeat 2-3 times"
            ],
            rationale="Stretching helps relieve muscle tension",
            precautions=["Move slowly", "Stop if pain increases"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=5
        ),
        Remedy(
            name="Rest and Elevation",
            steps=[
                "Rest the affected area",
                "Elevate if possible",
                "Avoid strenuous activity for 24-48 hours"
            ],
            rationale="Allows muscles to heal and reduces inflammation",
            precautions=["Resume activity gradually"],
            safe_for_pregnancy=True,
            safe_for_children=True,
            min_age=0
        )
    ]
    
    @classmethod
    def get_remedies_for_symptom(cls, symptom_type: str) -> List[Remedy]:
        """Get remedies for a specific symptom type"""
        symptom_map = {
            'cold': cls.COLD_REMEDIES,
            'congestion': cls.COLD_REMEDIES,
            'sore_throat': cls.COLD_REMEDIES,
            'cough': cls.COLD_REMEDIES,
            'headache': cls.HEADACHE_REMEDIES,
            'stomach': cls.STOMACH_REMEDIES,
            'nausea': cls.STOMACH_REMEDIES,
            'upset_stomach': cls.STOMACH_REMEDIES,
            'cut': cls.WOUND_REMEDIES,
            'scrape': cls.WOUND_REMEDIES,
            'wound': cls.WOUND_REMEDIES,
            'muscle_pain': cls.MUSCLE_PAIN_REMEDIES,
            'sore_muscle': cls.MUSCLE_PAIN_REMEDIES,
        }
        
        return symptom_map.get(symptom_type.lower(), [])
    
    @classmethod
    def filter_remedies_by_safety(
        cls,
        remedies: List[Remedy],
        age: Optional[int] = None,
        is_pregnant: bool = False,
        is_breastfeeding: bool = False,
        allergies: List[str] = None
    ) -> List[Remedy]:
        """Filter remedies based on user safety profile"""
        allergies = [a.lower() for a in (allergies or [])]
        safe_remedies = []
        
        for remedy in remedies:
            # Check age
            if age is not None and age < remedy.min_age:
                continue
            
            # Check pregnancy
            if is_pregnant and not remedy.safe_for_pregnancy:
                continue
            
            # Check allergies
            if allergies:
                has_allergen = any(
                    allergen in allergies 
                    for allergen in [a.lower() for a in remedy.avoid_if]
                )
                if has_allergen:
                    continue
            
            safe_remedies.append(remedy)
        
        return safe_remedies
    
    @classmethod
    def get_when_to_seek_help(cls, symptom_type: str) -> List[str]:
        """Get 'when to see a doctor' criteria for symptom type"""
        general_criteria = [
            "Symptoms persist for more than 7-10 days",
            "Symptoms worsen significantly",
            "You develop a high fever (>39°C/102°F)",
            "You experience severe pain",
            "You have difficulty breathing"
        ]
        
        specific_criteria = {
            'cold': [
                "Fever lasts more than 3 days",
                "Symptoms last more than 10 days",
                "Difficulty breathing or chest pain",
                "Severe sore throat or trouble swallowing"
            ],
            'headache': [
                "Worst headache of your life",
                "Headache with fever, stiff neck, confusion, or vision changes",
                "Headache after head injury",
                "Frequent or worsening headaches"
            ],
            'stomach': [
                "Severe abdominal pain",
                "Vomiting blood or blood in stool",
                "Signs of dehydration (dark urine, dizziness)",
                "Symptoms last more than 2 days"
            ],
        }
        
        return specific_criteria.get(symptom_type.lower(), general_criteria)
