"""
Remedy Database Module
Now powered by SQLite (previously hardcoded)
"""

from typing import List, Dict, Optional
from database import get_remedies, get_seek_help

class Remedy:
    def __init__(self, data: Dict):
        self.name = data['name']
        self.rationale = data['rationale']
        self.steps = data['steps']
        self.precautions = data.get('precautions', [])
        self.avoid_if = data.get('avoid_if', [])
        self.safe_for_pregnancy = bool(data['safe_for_pregnancy'])
        self.safe_for_children = bool(data['safe_for_children'])
        self.min_age = int(data['min_age'])

    def to_dict(self):
        return {
            'name': self.name,
            'rationale': self.rationale,
            'steps': self.steps,
            'precautions': self.precautions,
            'safe_for_pregnancy': self.safe_for_pregnancy,
            'safe_for_children': self.safe_for_children,
            'min_age': self.min_age
        }


class RemedyDatabase:
    """Interface for fetching remedies from SQLite"""

    @staticmethod
    def get_remedies_for_symptom(symptom_type: str) -> List[Remedy]:
        """Get all remedies for a specific symptom type"""
        raw_remedies = get_remedies(symptom_type)
        return [Remedy(r) for r in raw_remedies]

    @staticmethod
    def filter_remedies_by_safety(
        remedies: List[Remedy], 
        age: Optional[int] = None,
        is_pregnant: bool = False,
        is_breastfeeding: bool = False,
        allergies: List[str] = None
    ) -> List[Remedy]:
        """
        Filter remedies based on user safety profile
        (Logic remains same, just applied to DB objects)
        """
        safe_remedies = []
        allergies = [a.lower().strip() for a in (allergies or [])]
        
        for remedy in remedies:
            # 1. Age Check
            if age is not None and age < remedy.min_age:
                continue
                
            # 2. Pregnancy/Breastfeeding Check
            if (is_pregnant or is_breastfeeding) and not remedy.safe_for_pregnancy:
                continue
                
            # 3. Allergy Check
            if allergies:
                is_allergic = False
                for avoid_item in remedy.avoid_if:
                    if avoid_item.lower() in allergies:
                        is_allergic = True
                        break
                if is_allergic:
                    continue
            
            safe_remedies.append(remedy)
            
        return safe_remedies

    @staticmethod
    def get_when_to_seek_help(symptom_type: str) -> List[str]:
        """Get criteria for seeking medical help"""
        return get_seek_help(symptom_type)
