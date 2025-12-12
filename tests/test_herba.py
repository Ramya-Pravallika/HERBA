"""
Unit tests for Herba Health Companion
"""

import pytest
from backend.herba_core import RedFlagDetector, RemedyTriggerDetector, HerbaCore, UserContext
from backend.remedy_database import RemedyDatabase


class TestRedFlagDetector:
    """Test red flag detection"""
    
    def test_chest_pain_detection(self):
        is_flag, symptom = RedFlagDetector.check("I have severe chest pain")
        assert is_flag == True
        assert "chest pain" in symptom.lower()
    
    def test_breathing_difficulty(self):
        is_flag, symptom = RedFlagDetector.check("I can't breathe properly")
        assert is_flag == True
        assert "breathing" in symptom.lower()
    
    def test_high_fever(self):
        is_flag, symptom = RedFlagDetector.check("I have fever of 40 degrees")
        assert is_flag == True
    
    def test_normal_symptoms(self):
        is_flag, symptom = RedFlagDetector.check("I have a mild headache")
        assert is_flag == False
        assert symptom is None


class TestRemedyTriggerDetector:
    """Test remedy request detection"""
    
    def test_explicit_request(self):
        assert RemedyTriggerDetector.is_remedy_request("Can you suggest remedies?") == True
        assert RemedyTriggerDetector.is_remedy_request("Can you suggest me the remedies?") == True
        assert RemedyTriggerDetector.is_remedy_request("Please give home remedies") == True
    
    def test_implicit_mention(self):
        assert RemedyTriggerDetector.is_remedy_request("What home remedies can help?") == True
    
    def test_no_request(self):
        assert RemedyTriggerDetector.is_remedy_request("I have a headache") == False
        assert RemedyTriggerDetector.is_remedy_request("When did this start?") == False


class TestRemedyDatabase:
    """Test remedy database functionality"""
    
    def test_get_cold_remedies(self):
        remedies = RemedyDatabase.get_remedies_for_symptom('cold')
        assert len(remedies) > 0
        assert any('salt water' in r.name.lower() for r in remedies)
    
    def test_get_headache_remedies(self):
        remedies = RemedyDatabase.get_remedies_for_symptom('headache')
        assert len(remedies) > 0
    
    def test_filter_by_age(self):
        remedies = RemedyDatabase.get_remedies_for_symptom('cold')
        safe_remedies = RemedyDatabase.filter_remedies_by_safety(remedies, age=5)
        
        # Should exclude remedies with min_age > 5
        for remedy in safe_remedies:
            assert remedy.min_age <= 5
    
    def test_filter_by_pregnancy(self):
        remedies = RemedyDatabase.get_remedies_for_symptom('headache')
        safe_remedies = RemedyDatabase.filter_remedies_by_safety(
            remedies,
            is_pregnant=True
        )
        
        # All returned remedies should be safe for pregnancy
        for remedy in safe_remedies:
            assert remedy.safe_for_pregnancy == True
    
    def test_filter_by_allergies(self):
        remedies = RemedyDatabase.get_remedies_for_symptom('cold')
        safe_remedies = RemedyDatabase.filter_remedies_by_safety(
            remedies,
            allergies=['honey']
        )
        
        # Should exclude honey remedies
        for remedy in safe_remedies:
            assert 'honey' not in [a.lower() for a in remedy.avoid_if]


class TestHerbaCore:
    """Test core chatbot logic"""
    
    def test_session_creation(self):
        core = HerbaCore()
        session_id = "test-session"
        context = core.get_or_create_session(session_id)
        
        assert isinstance(context, UserContext)
        assert context.age is None
        assert context.symptoms_described == False
    
    def test_red_flag_handling(self):
        core = HerbaCore()
        result = core.process_message("test", "I can't breathe and have chest pain")
        
        assert result['red_flag'] == True
        assert result['response_type'] == 'red_flag_emergency'
        assert 'emergency' in result['response'].lower()
    
    def test_age_extraction(self):
        core = HerbaCore()
        session_id = "test"
        core.process_message(session_id, "I'm 25 years old")
        context = core.get_or_create_session(session_id)
        
        assert context.age == 25
    
    def test_pregnancy_detection(self):
        core = HerbaCore()
        session_id = "test"
        core.process_message(session_id, "I'm pregnant")
        context = core.get_or_create_session(session_id)
        
        assert context.is_pregnant == True
    
    def test_pregnancy_negative(self):
        core = HerbaCore()
        session_id = "test"
        core.process_message(session_id, "I'm not pregnant")
        context = core.get_or_create_session(session_id)
        
        assert context.is_pregnant == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
