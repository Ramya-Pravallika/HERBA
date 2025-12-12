# Quick Start Guide for Herba

## 🚀 Running Herba Locally

### Prerequisites
- Python 3.11+
- Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

### Quick Setup

1. **Set API Key** (PowerShell):
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

2. **Start Backend** (Terminal 1):
```powershell
cd c:\Users\nikhi\OneDrive\Desktop\HERBA\backend
python main.py
```

3. **Start Frontend** (Terminal 2):
```powershell
cd c:\Users\nikhi\OneDrive\Desktop\HERBA
streamlit run app.py
```

4. **Open Browser**:
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

### Try These Examples

**Test Conversation Flow**:
1. Type: "I have a sore throat"
2. Answer clarifying questions
3. Type: "Can you suggest me the remedies?"
4. See filtered, safe remedies

**Test Red Flag Detection**:
- Type: "I have severe chest pain"
- Herba immediately redirects to emergency care

**Test Safety Filtering**:
1. Type: "I have a headache"
2. Say: "I'm pregnant"
3. Request remedies
4. Only pregnancy-safe remedies shown

### Common Issues

**LLM Not Working?**
- Check `GEMINI_API_KEY` is set
- Fallback responses still work!

**Connection Error?**
- Ensure backend is running on port 8000
- Check firewall settings

**Import Errors?**
- Run: `pip install -r requirements.txt`

---

Made with 💚 by Herba
