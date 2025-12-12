"""
FastAPI Backend for Herba Health Companion
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import uuid
import logging
from datetime import datetime

from herba_core import HerbaCore
from remedy_database import RemedyDatabase
from llm_service import LLMService
from disclaimer import DisclaimerGenerator

# Configure logging (privacy-safe)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Herba Health Companion API",
    description="Conversational health companion chatbot",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
herba_core = HerbaCore()
try:
    llm_service = LLMService()
    logger.info("LLM service initialized successfully")
except Exception as e:
    logger.warning(f"LLM service failed to initialize: {e}. Using fallback responses.")
    llm_service = None


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    conversation_history: Optional[List[Dict]] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    response_type: str
    needs_confirmation: bool = False
    red_flag: bool = False
    remedies_json: Optional[List[Dict]] = None
    when_to_seek_help: Optional[List[str]] = None
    context: Optional[Dict] = None


class ResetRequest(BaseModel):
    session_id: str


# Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Herba Health Companion",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "ok",
        "llm_available": llm_service is not None,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    Processes user messages and returns appropriate responses
    """
    # Generate or use existing session ID
    session_id = request.session_id or str(uuid.uuid4())
    
    # Privacy-safe logging (no personal health info)
    logger.info(f"Chat request - Session: {session_id[:8]}..., Message length: {len(request.message)}")
    
    try:
        # Process message through core logic
        result = herba_core.process_message(session_id, request.message)
        
        # Handle different response types
        if result.get('red_flag'):
            # Emergency response - return immediately
            return ChatResponse(
                response=result['response'],
                session_id=session_id,
                response_type='red_flag_emergency',
                red_flag=True
            )
        
        if result['response_type'] == 'provide_remedies':
            # Generate remedy response using LLM
            context = result.get('context', {})
            remedy_response = await generate_remedy_response(
                session_id, 
                request.message, 
                context
            )
            
            return ChatResponse(
                response=remedy_response['response'],
                session_id=session_id,
                response_type='provide_remedies',
                remedies_json=remedy_response.get('remedies_json'),
                when_to_seek_help=remedy_response.get('when_to_seek_help'),
                context=context
            )
        
        # For all other responses, use LLM if available
        if llm_service and not result.get('response'):
            try:
                llm_response = llm_service.generate_conversational_response(
                    request.message,
                    request.conversation_history
                )
                result['response'] = llm_response
            except Exception as e:
                logger.error(f"LLM generation failed: {e}")
                # Keep the default response from herba_core
        
        return ChatResponse(
            response=result['response'],
            session_id=session_id,
            response_type=result['response_type'],
            needs_confirmation=result.get('needs_confirmation', False)
        )
        
    except Exception as e:
        logger.error(f"Chat processing error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/reset")
async def reset_session(request: ResetRequest):
    """Clear conversation history for a session"""
    herba_core.clear_session(request.session_id)
    logger.info(f"Session reset: {request.session_id[:8]}...")
    
    return {
        "status": "success",
        "message": "Session cleared",
        "session_id": request.session_id
    }


async def generate_remedy_response(
    session_id: str,
    user_message: str,
    context: Dict
) -> Dict:
    """
    Generate remedy response by:
    1. Identifying symptom type
    2. Fetching relevant remedies
    3. Filtering for safety
    4. Formatting with LLM
    """
    
    # Identify symptom type from message
    symptom_type = identify_symptom_type(user_message)
    
    # Get base remedies for symptom
    remedies = RemedyDatabase.get_remedies_for_symptom(symptom_type)
    
    # Filter by user safety profile
    safe_remedies = RemedyDatabase.filter_remedies_by_safety(
        remedies,
        age=context.get('age'),
        is_pregnant=context.get('is_pregnant', False),
        is_breastfeeding=context.get('is_breastfeeding', False),
        allergies=context.get('allergies', [])
    )
    
    if not safe_remedies:
        # No safe remedies available
        return {
            'response': (
                "Based on your profile, I don't have specific home remedies I can safely recommend. "
                "I'd suggest consulting with a healthcare professional who can provide personalized advice. "
                "\n\n" + DisclaimerGenerator.get_disclaimer('general')
            ),
            'remedies_json': [],
            'when_to_seek_help': []
        }
    
    # Limit to top 4-6 remedies
    safe_remedies = safe_remedies[:6]
    
    # Get "when to seek help" criteria
    when_to_seek_help = RemedyDatabase.get_when_to_seek_help(symptom_type)
    
    # Convert remedies to dict format
    remedies_json = [r.to_dict() for r in safe_remedies]
    
    # Generate formatted response with LLM
    if llm_service:
        try:
            return llm_service.generate_remedy_response(
                context,
                remedies_json,
                when_to_seek_help
            )
        except Exception as e:
            logger.error(f"LLM remedy generation failed: {e}")
            # Fall through to fallback
    
    # Fallback: simple formatted response
    return generate_simple_remedy_response(remedies_json, when_to_seek_help)


def identify_symptom_type(message: str) -> str:
    """Simple symptom type identification from message"""
    message_lower = message.lower()
    
    symptom_keywords = {
        'cold': ['cold', 'congestion', 'runny nose', 'stuffy', 'sore throat', 'cough'],
        'headache': ['headache', 'head pain', 'migraine'],
        'stomach': ['stomach', 'nausea', 'upset stomach', 'indigestion', 'stomach ache'],
        'muscle_pain': ['muscle pain', 'sore muscle', 'muscle ache', 'body ache'],
        'cut': ['cut', 'scrape', 'wound', 'scratch']
    }
    
    for symptom_type, keywords in symptom_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            return symptom_type
    
    # Default to cold if uncertain
    return 'cold'


def generate_simple_remedy_response(
    remedies: List[Dict],
    when_to_seek_help: List[str]
) -> Dict:
    """Generate simple text response without LLM"""
    
    response_parts = [
        "Here are some safe home remedies that might help:\n"
    ]
    
    for i, remedy in enumerate(remedies, 1):
        response_parts.append(f"\n**{i}. {remedy['name']}**")
        response_parts.append(f"*{remedy['rationale']}*")
        response_parts.append("\nSteps:")
        for step in remedy['steps']:
            response_parts.append(f"  • {step}")
        
        if remedy['precautions']:
            response_parts.append(f"\n⚠️ Precautions: {', '.join(remedy['precautions'])}")
        response_parts.append("")
    
    response_parts.append("\n**⚕️ When to Seek Medical Help:**")
    for item in when_to_seek_help:
        response_parts.append(f"  • {item}")
    
    response_parts.append("\n" + DisclaimerGenerator.get_disclaimer('remedy'))
    
    response_parts.append("\n\nWould you like more details about any of these remedies? 💚")
    
    return {
        'response': '\n'.join(response_parts),
        'remedies_json': remedies,
        'when_to_seek_help': when_to_seek_help
    }


if __name__ == "__main__":
    import uvicorn
    
    print("Starting Herba Health Companion API...")
    print("Remember to set GEMINI_API_KEY environment variable")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
