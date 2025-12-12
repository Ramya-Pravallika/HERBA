"""
Herba Health Companion - Streamlit Frontend
A warm, conversational health companion chatbot
"""

import streamlit as st
import requests
import json
from typing import Dict, List
import uuid

# Configuration
API_URL = "http://localhost:8001"

# Page configuration - Using CENTERED layout for the 3D card look
st.set_page_config(
    page_title="Herba | Health Companion",
    page_icon="🌿",
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- THEME & CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Force variables to ensure consistency across Light/Dark modes */
    :root {
        --primary-teal: #2A9D8F;
        --deep-blue: #264653;
        --soft-bg: #F0F2F0;
        --card-bg: #FFFFFF;
        --text-main: #264653;
        --text-secondary: #5F6368;
        --accent-orange: #E76F51;
        --shadow-color: rgba(38, 70, 83, 0.15);
    }

    /* Global Overrides */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* App Background */
    .stApp {
        background: linear-gradient(135deg, #E0F2F1 0%, #B2DFDB 100%);
        background-attachment: fixed;
    }

    /* The "3D Card" Effect for Main Container */
    .block-container {
        background-color: var(--card-bg);
        border-radius: 24px;
        box-shadow: 
            0 20px 40px var(--shadow-color),
            0 0 0 1px rgba(255,255,255,0.5) inset;
        margin-top: 2rem;
        padding: 2rem !important;
        border: 1px solid rgba(255,255,255,0.6);
        max-width: 800px;
        width: 95%; /* Responsive width */
    }
    
    /* Mobile Optimization */
    @media (max-width: 600px) {
        .block-container {
            padding: 1rem !important;
            margin-top: 1rem;
            border-radius: 16px;
        }
        
        .herba-logo { font-size: 3rem; }
        .header-title { font-size: 2rem; }
        
        .stTextInput input {
            padding: 12px 15px !important;
        }
    }

    /* Force input area background to ensure visibility */
    .stChatInputContainer {
        padding-bottom: 2rem;
    }
    
    [data-testid="stChatInput"] {
        background-color: transparent !important;
    }
    
    /* Force Input text color */
    textarea[data-testid="stChatInputTextArea"] {
        background-color: white !important;
        color: var(--text-main) !important;
        border-radius: 24px !important;
        border: 2px solid #E0E0E0 !important;
    }

    /* Ensure text visibility in Dark Mode by forcing colors inside the card */
    .stMarkdown, .stText, h1, h2, h3, p, label, .stChatMessage {
        color: var(--text-main) !important;
    }

    /* Custom Header inside Card */
    .herba-header {
        text-align: center;
        margin-bottom: 2rem;
        padding-bottom: 2rem;
        border-bottom: 2px dashed #E0E0E0;
    }
    
    .herba-logo {
        font-size: 4rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 10px rgba(0,0,0,0.1);
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .header-title {
        font-size: 2.5rem;
        color: var(--deep-blue);
        font-weight: 700;
        margin: 0;
    }
    
    .header-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 0.5rem;
    }

    /* Chat Styling */
    .stChatMessage {
        background-color: transparent !important;
    }

    /* User Message */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        flex-direction: row-reverse;
        text-align: right;
    }
    
    div[data-testid="stChatMessage"]:nth-child(odd) .stMarkdown {
        background: linear-gradient(135deg, var(--deep-blue) 0%, var(--primary-teal) 100%);
        color: white !important;
        border-radius: 18px 18px 4px 18px;
        box-shadow: 0 4px 15px rgba(42, 157, 143, 0.2);
        padding: 1rem 1.5rem;
    }
    
    div[data-testid="stChatMessage"]:nth-child(odd) p {
        color: white !important;
    }

    /* Bot Message */
    div[data-testid="stChatMessage"]:nth-child(even) .stMarkdown {
        background-color: #F8F9FA;
        border: 1px solid #E0E0E0;
        color: var(--text-main) !important;
        border-radius: 18px 18px 18px 4px;
        padding: 1rem 1.5rem;
    }

    /* Input Field */
    .stTextInput input {
        border-radius: 30px !important;
        border: 2px solid #E0E0E0 !important;
        padding: 15px 25px !important;
        background-color: white !important;
        color: var(--text-main) !important;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary-teal) !important;
        box-shadow: 0 0 0 4px rgba(42, 157, 143, 0.1) !important;
    }

    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] { display: none; } /* Strictly hide sidebar */

    /* Remedy Card Styling */
    .remedy-box {
        background: white;
        border: 1px solid #E0E0E0;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        transition: all 0.2s;
        border-left: 4px solid var(--primary-teal);
    }
    
    .remedy-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    }

</style>
""", unsafe_allow_html=True)

# Initialize State
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Logic
def send_message(message: str) -> Dict:
    try:
        payload = {
            "message": message,
            "session_id": st.session_state.session_id,
            "conversation_history": st.session_state.conversation_history
        }
        response = requests.post(f"{API_URL}/chat", json=payload, timeout=30)
        return response.json() if response.status_code == 200 else None
    except:
        return None

# --- MAIN CONTENT ---

# 3D Card Header
st.markdown("""
<div class="herba-header">
    <div class="herba-logo">🌿</div>
    <div class="header-title">Herba</div>
    <div class="header-subtitle">Your AI Health Companion</div>
</div>
""", unsafe_allow_html=True)

# Conversation Display
chat_placeholder = st.container()

with chat_placeholder:
    if not st.session_state.messages:
        st.markdown("<div style='text-align: center; color: #888; margin: 2rem 0;'>Start chatting below to check symptoms or get home remedies.</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        if col1.button("🤕 Headache Remedial", use_container_width=True):
             st.session_state.messages.append({"role": "user", "content": "I have a headache"})
             st.rerun()
        if col2.button("🤧 Cold & Flu", use_container_width=True):
             st.session_state.messages.append({"role": "user", "content": "I have a cold"})
             st.rerun()

    for msg in st.session_state.messages:
        role = msg['role']
        is_user = role == "user"
        
        with st.chat_message(role, avatar="👤" if is_user else "🌿"):
            if msg.get('is_emergency'):
                st.markdown(f"🚨 **EMERGENCY RESPONSE**\n\n{msg['content']}")
            else:
                st.markdown(msg['content'])

            # Render Remedies
            if msg.get('remedies'):
                for remedy in msg['remedies']:
                    with st.expander(f"✨ {remedy['name']}"):
                        st.markdown(f"""
                        <div class="remedy-box">
                            <b>Why?</b> {remedy['rationale']}<br><br>
                            <b>Steps:</b><br>
                            {'<br>'.join([f'- {s}' for s in remedy['steps']])}
                            <br><br>
                            <span style="color:#E76F51; font-size:0.9em;">⚠️ {', '.join(remedy.get('precautions',[]))}</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            if msg.get('when_to_seek_help'):
                 with st.expander("⚕️ When to see a doctor"):
                     for item in msg['when_to_seek_help']:
                         st.markdown(f"- {item}")

# Footer Input
st.markdown("<br>", unsafe_allow_html=True)
if prompt := st.chat_input("How are you feeling properly?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation_history.append({"role": "user", "content": prompt})
    
    with st.spinner("Analyzing..."):
        response = send_message(prompt)
    
    if response:
        bot_msg = {
            "role": "assistant",
            "content": response['response'],
            "is_emergency": response.get('red_flag'),
            "remedies": response.get('remedies_json'),
            "when_to_seek_help": response.get('when_to_seek_help')
        }
        st.session_state.messages.append(bot_msg)
        st.session_state.conversation_history.append({"role": "assistant", "content": response['response']})
        st.rerun()
