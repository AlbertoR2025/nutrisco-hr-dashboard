# pages/4_🤖_Chatbot Colaboradores.py
import streamlit as st
import pandas as pd
import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="Chatbot Colaboradores – Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CSS MEJORADO - ELIMINAR TODO + INPUT FUNCIONAL ====================
st.markdown("""
<style>
    /* === ELIMINAR ELEMENTOS STREAMLIT === */
    header, [data-testid="stHeader"] {display: none !important;}
    footer, [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDeployButton"] {display: none !important;}
    
    /* === ELIMINAR AVATARES COMPLETAMENTE === */
    [data-testid="stChatMessage"] [data-testid="stAvatar"],
    [data-testid="stChatMessage"] img,
    [data-testid="stChatMessage"] svg,
    [data-testid="stChatInput"] [data-testid="stAvatar"],
    [data-testid="stChatInput"] img,
    [data-testid="stChatInput"] svg {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        visibility: hidden !important;
    }
    
    /* === CORREGIR INPUT DE CHAT - VERSIÓN SIMPLIFICADA === */
    [data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 90% !important;
        max-width: 800px !important;
        background: #0e1117 !important;
        padding: 1rem !important;
        border-top: 1px solid #333 !important;
        z-index: 9999 !important;
    }
    
    [data-testid="stChatInput"] > div {
        background: #1e1e1e !important;
        border: 1px solid #444 !important;
        border-radius: 25px !important;
        padding: 8px !important;
    }
    
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: white !important;
        border: none !important;
        padding: 8px 12px !important;
    }
    
    [data-testid="stChatInput"] textarea:focus {
        outline: none !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    [data-testid="stChatInput"] button {
        background: #ea580c !important;
        border: none !important;
        border-radius: 50% !important;
    }
    
    /* === ESTILOS DE LA APLICACIÓN === */
    .main .block-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
        padding-bottom: 100px !important;
    }
    
    .stApp {
        background-color: #0e1117 !important;
    }
    
    .header-box {
        background: linear-gradient(90deg, #ea580c, #c2410c);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .user-msg {
        background: #262730;
        color: white;
        border-radius: 18px;
        padding: 14px 20px;
        margin: 12px 0 12px auto;
        max-width: 75%;
    }
    
    .assistant-msg {
        background: linear-gradient(135deg, #ea580c, #f97316);
        color: white;
        border-radius: 18px;
        padding: 14px 20px;
        margin: 12px auto 12px 0;
        max-width: 75%;
    }
    
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #64748b;
        padding: 2rem 0;
    }
    
    @media (max-width: 768px) {
        [data-testid="stChatInput"] {
            width: 95% !important;
        }
        .user-msg, .assistant-msg {
            max-width: 85%;
        }
    }
</style>

<script>
// JavaScript para eliminar elementos persistentes
setTimeout(() => {
    // Eliminar avatares
    document.querySelectorAll('[data-testid="stAvatar"]').forEach(el => el.remove());
    // Eliminar elementos del header
    document.querySelectorAll('header').forEach(el => el.remove());
}, 100);
</script>
""", unsafe_allow_html=True)

# ==================== LÓGICA DE LA APLICACIÓN ====================
API_KEY = os.getenv("OPENAI_API_KEY")

# Header
st.markdown("""
<div class="header-box">
    <h1 style="margin:0; font-size: 2.2rem;">Chatbot Colaboradores</h1>
    <h2 style="margin:8px 0 0 0; font-weight:300; font-size: 1.3rem;">Nutrisco – Atención Personas</h2>
    <p style="margin:15px 0 0 0; opacity: 0.9;">Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

# Mensaje de bienvenida
st.markdown("""
<div class="assistant-msg">
    <strong>¡Hola! 👋</strong> Soy parte del equipo de <strong>Atención a Personas</strong> de Nutrisco.<br><br>
    Puedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.<br><br>
    ¡Estoy aquí para ayudarte!
</div>
""", unsafe_allow_html=True)

# ==================== CHAT FUNCTIONALITY ====================
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-msg">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-msg">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input - ESTA ES LA PARTE CRÍTICA
user_input = st.chat_input("Escribe tu consulta aquí...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    st.markdown(f'<div class="user-msg">{user_input}</div>', unsafe_allow_html=True)
    
    # Display assistant response
    with st.spinner("Pensando..."):
        # Simulate processing time
        time.sleep(1)
        
        # Get AI response
        try:
            if API_KEY:
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {
                                "role": "system", 
                                "content": "Eres un asistente de RR.HH. de Nutrisco. Responde de manera profesional y cercana."
                            },
                            {"role": "user", "content": user_input}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500
                    },
                    timeout=30
                )
                assistant_response = response.json()["choices"][0]["message"]["content"]
            else:
                assistant_response = "Error: No se configuró la API key"
        except Exception as e:
            assistant_response = "Error de conexión. Contacta a Belén Bastías: belen.bastias@nutrisco.com"
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # Display assistant response
    st.markdown(f'<div class="assistant-msg">{assistant_response}</div>', unsafe_allow_html=True)
    
    # Rerun to clear input and show new messages
    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco © 2025
</div>
""", unsafe_allow_html=True)
