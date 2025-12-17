"""
Herba Core - Main chatbot logic engine
Handles conversation flow, symptom triage, red flag detection, and remedy triggers
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UserContext:
    """Stores user information for a conversation session"""
    age: Optional[int] = None
    is_pregnant: Optional[bool] = None
    is_breastfeeding: Optional[bool] = None
    allergies: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)
    chronic_conditions: List[str] = field(default_factory=list)
    symptoms: Dict[str, any] = field(default_factory=dict)
    symptoms_described: bool = False
    safety_confirmed: bool = False
    last_bot_question: Optional[str] = None


class RedFlagDetector:
    """Detects severe symptoms that require emergency care"""
    
    RED_FLAG_PATTERNS = [
        # Breathing issues
        (r'\b(can\'?t breathe|difficulty breathing|gasping|suffocating|choking)\b', 'severe breathing difficulty'),
        (r'\b(shortness of breath|breathing hard|can\'?t catch.*breath)\b', 'breathing problems'),
        
        # Chest pain
        (r'\b(chest pain|crushing.*chest|pressure.*chest|tight.*chest)\b', 'chest pain'),
        (r'\b(heart.*pain|cardiac|angina)\b', 'cardiac symptoms'),
        
        # Neurological
        (r'\b(stroke|face.*droop|arm.*weak|slurred speech|sudden.*confusion)\b', 'stroke symptoms'),
        (r'\b(fainting|fainted|passed out|lost consciousness|unconscious)\b', 'loss of consciousness'),
        (r'\b(severe.*headache|worst headache|sudden.*headache.*severe)\b', 'severe headache'),
        (r'\b(seizure|convulsion|fitting)\b', 'seizure activity'),
        
        # Bleeding
        (r'\b(severe bleeding|heavy bleeding|bleeding.*won\'?t stop|hemorrhag)\b', 'severe bleeding'),
        (r'\b(vomit.*blood|cough.*blood|blood.*stool|blood.*urine)\b', 'bleeding symptoms'),
        
        # High fever
        (r'\b(fever.*40|fever.*104|fever.*41|fever.*105|very high fever)\b', 'dangerously high fever'),
        (r'\b(fever.*39\.5|fever.*103)\b', 'very high fever'),
        
        # Other emergencies
        (r'\b(anaphyla|severe.*allergic|throat.*closing|swelling.*throat)\b', 'severe allergic reaction'),
        (r'\b(suicide|kill myself|harm myself)\b', 'mental health crisis'),
        (r'\b(severe.*abdominal.*pain|appendicitis)\b', 'severe abdominal pain'),
    ]
    
    @classmethod
    def check(cls, text: str) -> Tuple[bool, Optional[str]]:
        """
        Check if text contains red flag symptoms
        Returns: (is_red_flag, detected_symptom)
        """
        text_lower = text.lower()
        
        for pattern, symptom_type in cls.RED_FLAG_PATTERNS:
            if re.search(pattern, text_lower):
                return True, symptom_type
        
        return False, None


class RemedyTriggerDetector:
    """Detects explicit requests for home remedies"""
    
    REMEDY_REQUEST_PATTERNS = [
        r'\b(can you|could you|please)\s+(suggest|give|provide|recommend|tell me).*remedies?\b',
        r'\bsuggest\s+me\s+(the\s+)?remedies?\b',
        r'\bhome\s+remedies?\b',
        r'\bwhat\s+(can|should)\s+I\s+(try|do|take)\b',
        r'\bany\s+remedies?\b',
        r'\bremedies?\s+(for|to|that)\b',
        r'\bhelp\s+me\s+with.*remedies?\b',
        r'\bnatural\s+(cure|treatment|remedy)\b',
        r'\b(how|what).*cure\b',
    ]
    
    @classmethod
    def is_remedy_request(cls, text: str) -> bool:
        """Check if user is explicitly requesting home remedies"""
        text_lower = text.lower()
        
        for pattern in cls.REMEDY_REQUEST_PATTERNS:
            if re.search(pattern, text_lower):
                return True
        
        return False


class HerbaCore:
    """Core chatbot logic and conversation management"""
    
    def __init__(self):
        self.sessions: Dict[str, UserContext] = {}
    
    def get_or_create_session(self, session_id: str) -> UserContext:
        """Get existing session or create new one"""
        if session_id not in self.sessions:
            self.sessions[session_id] = UserContext()
        return self.sessions[session_id]
    
    def clear_session(self, session_id: str):
        """Clear conversation history for a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def process_message(self, session_id: str, user_message: str) -> Dict:
        """
        Main message processing logic
        Returns structured response with text and metadata
        """
        context = self.get_or_create_session(session_id)
        
        # Check for red flags first
        is_red_flag, red_flag_type = RedFlagDetector.check(user_message)
        if is_red_flag:
            return self._handle_red_flag(red_flag_type)
        
        # Update context based on message (age, pregnancy, etc.)
        context = self._update_context(context, user_message)
        
        # Check if user is explicit requesting remedies
        is_explicit_remedy_request = RemedyTriggerDetector.is_remedy_request(user_message)
        
        # 1. Logic Flow: Answer to "When did start?" -> Trigger
        if context.last_bot_question == "When did these symptoms start?":
             # We assume this is the answer
             return self._trigger_remedy_flow(context)
        
        # 2. Logic Flow: Explicit Request
        if is_explicit_remedy_request:
            if not context.symptoms_described:
                 # If user says "give me remedies" but hasn't said "I have a cold"
                return {
                    'response': "I'd be happy to help! But first, could you tell me a bit more about what symptoms you're experiencing?",
                    'response_type': 'need_more_info',
                    'needs_confirmation': False
                }
            return self._trigger_remedy_flow(context)

        # 3. Logic Flow: New Symptoms -> Ask "When started?"
        has_new_symptoms = self._has_symptoms_in_message(user_message)
        if has_new_symptoms:
            context.symptoms_described = True
            question = "When did these symptoms start?"
            context.last_bot_question = question
            return {
                'response': question,
                'response_type': 'clarifying_question',
                'needs_confirmation': False
            }

        # 4. Logic Flow: Greetings
        if not context.symptoms_described:
            greetings = ['hi', 'hello', 'hey', 'greetings', 'morning', 'afternoon', 'evening']
            # If greeting OR very short message likely just saying hi
            if any(g in user_message.lower() for g in greetings) or len(user_message.split()) < 3:
                return {
                     'response': "Hi! I'm Herba, your health companion. 💚 I'm here to help you with natural home remedies. How are you feeling today?",
                     'response_type': 'greeting',
                     'needs_confirmation': False
                }

        # 5. Fallback
        # If we have symptoms but stuck in loop, just give remedies
        if context.symptoms_described:
              return self._trigger_remedy_flow(context)

        return {
            'response': '',
            'response_type': 'conversation',
            'needs_confirmation': False
        }

    def _trigger_remedy_flow(self, context: UserContext) -> Dict:
        """Helper to manage the flow to remedies with safety checks"""
        
        # Check if we need safety confirmation
        if not context.safety_confirmed:
            return self._request_safety_confirmation(context)
        
        # Ready to provide remedies
        context.last_bot_question = None # Reset
        return {
            'response': '',  # Will be filled by LLM
            'response_type': 'provide_remedies',
            'needs_confirmation': False,
            'context': self._serialize_context(context)
        }
    
    def _handle_red_flag(self, red_flag_type: str) -> Dict:
        """Generate emergency response for red flag symptoms"""
        response = f"""⚠️ **This sounds serious.**

Based on what you've described ({red_flag_type}), I strongly recommend you seek immediate medical attention:

• **Call emergency services (911/112)** or go to the nearest emergency room
• If symptoms are life-threatening, don't delay
• Don't drive yourself if symptoms are severe

I cannot provide home remedies for potentially serious conditions. Please get professional medical help right away.

Stay safe, and I hope you get the care you need quickly. 💚"""
        
        return {
            'response': response,
            'response_type': 'red_flag_emergency',
            'needs_confirmation': False,
            'red_flag': True
        }
    
    def _request_safety_confirmation(self, context: UserContext) -> Dict:
        """Ask for safety information before providing remedies"""
        questions = []
        
        if context.age is None:
            questions.append("What's your age?")
        
        if context.is_pregnant is None:
            questions.append("Are you currently pregnant or breastfeeding?")
        
        if not context.allergies:
            questions.append("Do you have any allergies I should know about? (food, medications, plants, etc.)")
        
        if questions:
            response = "Before I suggest remedies, I need to know a few things to ensure they're safe for you:\n\n"
            response += "\n".join(f"• {q}" for q in questions)
            
            context.last_bot_question = "safety_check"
            return {
                'response': response,
                'response_type': 'safety_check',
                'needs_confirmation': True
            }
        
        context.safety_confirmed = True
        return self._trigger_remedy_flow(context)
    
    def _update_context(self, context: UserContext, message: str) -> UserContext:
        """Extract information from user message and update context"""
        message_lower = message.lower()
        
        # Extract age
        age_match = re.search(r'\b(\d{1,3})\s*(years?|yrs?|y\.?o\.?)?\s*(old)?\b', message_lower)
        if age_match:
            try:
                age = int(age_match.group(1))
                if 0 < age < 120:
                    context.age = age
            except ValueError:
                pass
        
        # Check pregnancy/breastfeeding
        if re.search(r'\b(not pregnant|no.*pregnant|not.*expecting)\b', message_lower):
            context.is_pregnant = False
        elif re.search(r'\b(pregnant|expecting|pregnancy)\b', message_lower):
            context.is_pregnant = True
        
        if re.search(r'\b(not breastfeeding|no.*breastfeeding|not.*nursing)\b', message_lower):
            context.is_breastfeeding = False
        elif re.search(r'\b(breastfeeding|nursing)\b', message_lower):
            context.is_breastfeeding = True
        
        # Check allergies
        if re.search(r'\b(no allergies|no allergy|not allergic)\b', message_lower):
            context.allergies = []
        elif 'allerg' in message_lower:
            common_allergens = ['peanut', 'nut', 'dairy', 'lactose', 'gluten', 'honey', 
                              'pollen', 'dust', 'penicillin', 'aspirin', 'sulfa', 'latex']
            for allergen in common_allergens:
                if allergen in message_lower:
                    if allergen not in context.allergies:
                        context.allergies.append(allergen)
        
        return context
    
    def _has_symptoms_in_message(self, message: str) -> bool:
        """Check if message describes symptoms"""
        symptom_keywords = [
            'pain', 'ache', 'hurt', 'sore', 'fever', 'cold', 'cough', 'headache',
            'nausea', 'dizzy', 'tired', 'fatigue', 'congestion', 'runny nose',
            'stomach', 'throat', 'sick', 'ill', 'unwell', 'symptom', 'vomit',
            'burn', 'cut', 'bleed', 'rash', 'itch', 'swoll'
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in symptom_keywords)
    
    def _serialize_context(self, context: UserContext) -> Dict:
        """Convert context to dictionary for API response"""
        return {
            'age': context.age,
            'is_pregnant': context.is_pregnant,
            'is_breastfeeding': context.is_breastfeeding,
            'allergies': context.allergies,
            'medications': context.medications,
            'chronic_conditions': context.chronic_conditions,
            'symptoms': context.symptoms
        }
