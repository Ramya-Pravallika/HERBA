# Herba - Health Companion Chatbot

🌿 **Herba** is a warm, conversational health companion chatbot that helps users explore their symptoms through clarifying questions and provides safe, evidence-based home remedies.

## Features

✨ **Conversational & Empathetic**: Warm, friendly tone that makes users feel heard
🔍 **Intelligent Symptom Triage**: Asks clarifying questions about onset, severity, allergies, and more
🚨 **Red Flag Detection**: Immediately escalates severe symptoms to emergency care
💊 **Evidence-Based Remedies**: Provides safe home remedies only when explicitly requested
✅ **Safety-First Approach**: Filters remedies by age, pregnancy, and allergies
🤖 **LLM-Powered**: Uses Gemini API for natural, conversational responses
🎨 **Beautiful UI**: Calming green palette with modern, healthcare-appropriate design

## Architecture

- **Backend**: FastAPI with async support
- **Frontend**: Streamlit with custom CSS
- **LLM**: Google Gemini 2.0 Flash
- **Session Management**: In-memory (extensible to Redis)

## Installation

1. **Clone the repository**:
```bash
cd HERBA
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set API Key**:
Create a `.env` file or set environment variable:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Windows CMD
set GEMINI_API_KEY=your-api-key-here
```

## Usage

### Running the Backend

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### Running the Frontend

In a separate terminal:
```bash
streamlit run app.py
```

The UI will open automatically in your browser at `http://localhost:8501`

## API Endpoints

- `GET /`: Health check
- `GET /health`: Detailed health status
- `POST /chat`: Main conversation endpoint
- `POST /reset`: Clear conversation history

### Example Chat Request

```json
{
  "message": "I have a sore throat and mild fever",
  "session_id": "optional-session-id",
  "conversation_history": []
}
```

## Safety Features

1. **Never Diagnoses**: Only provides supportive information
2. **Red Flag System**: Detects severe symptoms and redirects to emergency care
3. **Explicit Remedy Requests**: Only shows remedies when user asks
4. **Safety Checks**: Confirms allergies, pregnancy, and age before suggesting remedies
5. **Medical Disclaimers**: Included in every interaction
6. **Evidence-Based Content**: Only safe, low-risk remedies
7. **Privacy-Safe Logging**: No personal health information logged

## Remedy Categories

- Cold & Congestion
- Headaches
- Upset Stomach
- Minor Cuts & Scrapes
- Muscle Pain

Each remedy includes:
- Step-by-step instructions
- Rationale
- Precautions
- When to seek medical help

## Testing

```bash
pytest tests/
```

## Project Structure

```
HERBA/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── herba_core.py        # Core chatbot logic
│   ├── remedy_database.py   # Home remedy data
│   ├── llm_service.py       # Gemini API integration
│   └── disclaimer.py        # Medical disclaimers
├── app.py                   # Streamlit frontend
├── requirements.txt          # Dependencies
└── README.md                # This file
```

## Important Disclaimers

⚠️ **Medical Disclaimer**: Herba is not a medical professional and does not provide medical diagnoses. This is general health information and not a substitute for professional medical advice. If you have health concerns, please consult a qualified healthcare provider.

🔒 **Privacy**: Conversations are session-based and not stored permanently. No personal health information is logged in plain text.


## Support

For issues or questions, please open an issue on the repository.

---

Made with 💚 for better health conversations
