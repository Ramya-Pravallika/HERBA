"""
LLM Service - Integration with Gemini API for conversational responses
"""

import os
import json
from typing import Dict, List, Optional
import google.generativeai as genai


class LLMService:
    """Handles LLM API calls for conversational responses and remedy formatting"""
    
    SYSTEM_PROMPT = """You are Herba, a warm, empathetic health companion chatbot. Your personality:
- Warm, conversational, friendly (not clinical or cold)
- Use plain language, avoid medical jargon
- Be concise and clear
- Show empathy and understanding

CRITICAL RULES:
1. NEVER diagnose medical conditions
2. NEVER recommend prescription medications
3. NEVER advise stopping prescribed medications
4. Always maintain safe, supportive guidance

Your role is to:
- Ask clarifying questions about symptoms naturally
- Provide emotional support
- Present home remedies in a friendly, accessible way
- Always include safety disclaimers"""

    REMEDY_PROMPT_TEMPLATE = """The user has requested home remedies for their symptoms. Generate a warm, helpful response.

User Context:
{context}

Approved Safe Remedies:
{remedies}

When to Seek Help:
{seek_help}

Generate a response that:
1. Starts with empathy and brief non-diagnostic summary
2. Presents each remedy conversationally with steps and precautions
3. Includes "When to Seek Medical Help" section
4. Ends with supportive follow-up question
5. Includes medical disclaimer

Use a warm, conversational tone. Format with clear sections and bullet points for readability."""

    CONVERSATION_PROMPT_TEMPLATE = """Continue the conversation with the user about their health concerns.

Conversation so far:
{history}

User's latest message: {message}

Respond with:
- Natural, empathetic acknowledgment
- One or two relevant clarifying questions
- Warm, supportive tone

Keep it concise (2-3 sentences)."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize LLM service with API key"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it as environment variable.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_remedy_response(
        self,
        context: Dict,
        remedies: List[Dict],
        when_to_seek_help: List[str]
    ) -> Dict:
        """Generate formatted remedy response with LLM"""
        
        # Format context
        context_str = f"""
Age: {context.get('age', 'Not specified')}
Pregnant: {context.get('is_pregnant', 'Not specified')}
Breastfeeding: {context.get('is_breastfeeding', 'Not specified')}
Allergies: {', '.join(context.get('allergies', [])) or 'None mentioned'}
Symptoms: {context.get('symptoms', {})}
"""
        
        # Format remedies
        remedies_str = "\n\n".join([
            f"**{r['name']}**\n"
            f"Rationale: {r['rationale']}\n"
            f"Steps:\n" + "\n".join(f"  - {step}" for step in r['steps']) + "\n"
            f"Precautions: {', '.join(r['precautions'])}"
            for r in remedies
        ])
        
        # Format seek help criteria
        seek_help_str = "\n".join(f"- {item}" for item in when_to_seek_help)
        
        prompt = self.REMEDY_PROMPT_TEMPLATE.format(
            context=context_str,
            remedies=remedies_str,
            seek_help=seek_help_str
        )
        
        try:
            response = self.model.generate_content(
                f"{self.SYSTEM_PROMPT}\n\n{prompt}",
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'max_output_tokens': 2048,
                }
            )
            
            response_text = response.text
            
            # Add disclaimer if not already present
            if 'not medical advice' not in response_text.lower():
                response_text += "\n\n💚 **Medical Disclaimer**: I'm not a doctor. This is general information and not a substitute for professional medical advice. If you're concerned, please contact a healthcare professional."
            
            return {
                'response': response_text,
                'remedies_json': remedies,
                'when_to_seek_help': when_to_seek_help
            }
            
        except Exception as e:
            # Fallback response if LLM fails
            return self._generate_fallback_remedy_response(remedies, when_to_seek_help)
    
    def generate_conversational_response(
        self,
        message: str,
        conversation_history: List[Dict] = None
    ) -> str:
        """Generate natural conversational response"""
        
        history_str = ""
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages
                role = msg.get('role', 'user')
                text = msg.get('content', '')
                history_str += f"{role.capitalize()}: {text}\n"
        
        prompt = self.CONVERSATION_PROMPT_TEMPLATE.format(
            history=history_str or "First message",
            message=message
        )
        
        try:
            response = self.model.generate_content(
                f"{self.SYSTEM_PROMPT}\n\n{prompt}",
                generation_config={
                    'temperature': 0.8,
                    'top_p': 0.9,
                    'max_output_tokens': 512,
                }
            )
            
            return response.text
            
        except Exception as e:
            # Fallback
            return "I'm having a bit of trouble right now. Could you tell me more about what you're experiencing?"
    
    def _generate_fallback_remedy_response(
        self,
        remedies: List[Dict],
        when_to_seek_help: List[str]
    ) -> Dict:
        """Generate structured response without LLM (fallback)"""
        
        response_parts = [
            "Here are some safe home remedies that might help:\n"
        ]
        
        for i, remedy in enumerate(remedies, 1):
            response_parts.append(f"\n**{i}. {remedy['name']}**")
            response_parts.append(f"*{remedy['rationale']}*\n")
            response_parts.append("Steps:")
            for step in remedy['steps']:
                response_parts.append(f"  • {step}")
            response_parts.append(f"\n⚠️ Precautions: {', '.join(remedy['precautions'])}\n")
        
        response_parts.append("\n**When to Seek Medical Help:**")
        for item in when_to_seek_help:
            response_parts.append(f"  • {item}")
        
        response_parts.append("\n\n💚 **Medical Disclaimer**: I'm not a doctor. This is general information and not a substitute for professional medical advice. If you're concerned, please contact a healthcare professional.")
        
        response_parts.append("\n\nWould you like more details about any of these remedies?")
        
        return {
            'response': '\n'.join(response_parts),
            'remedies_json': remedies,
            'when_to_seek_help': when_to_seek_help
        }
