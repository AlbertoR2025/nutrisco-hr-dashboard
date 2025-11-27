# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN CORREGIDA
import streamlit as st
import pandas as pd
import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIGURACIÓN GLOBAL ====================
st.set_page_config(
    page_title="Chatbot Colaboradores – Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CSS CORREGIDO - INPUT FUNCIONAL ====================
css_code = '''
<style>
    /* OCULTAR CORONA ROJA */
    .stAppDeployButton, button[data-testid="stDeployButton"], .stDeployButton {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        z-index: -9999 !important;
    }

    /* OCULTAR LOGO GITHUB Y FOOTER */
    footer, [data-testid="stStatusWidget"], div[class*="hosted"], 
    a[href*="github.com"], span:contains("Streamlit") {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }

    /* OCULTAR MENÚ SUPERIOR */
    .stToolbar { display: none !important; }
    .stHeader { display: none !important; }
    .stDeployButtonContainer { display: none !important; }

    /* LAYOUT SIMÉTRICO RESPONSIVO */
    .main .block-container {
        max-width: 800px !important;
        margin: 0 auto !important;
        padding: 1rem !important;
        width: auto !important;
    }
    @media (max-width: 768px) {
        .main .block-container { 
            width: 95% !important; 
            padding: 0.5rem !important; 
        }
    }
    .stApp { 
        background-color: #0e1117 !important; 
    }

    /* ESTILOS MENSAJES SIMÉTRICOS */
    [data-testid="stChatMessage"] { 
        padding: 0 !important; 
        gap: 0 !important; 
    }
    .user-message {
        background: #262730 !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 14px 20px !important;
        margin: 16px 8% 16px auto !important;
        max-width: 75% !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.4) !important;
    }
    .assistant-message {
        background: linear-gradient(135deg, #ea580c, #f97316) !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 14px 20px !important;
        margin: 16px auto 16px 8% !important;
        max-width: 75% !important;
        box-shadow: 0 4px 15px rgba(249,115,22,0.5) !important;
    }
    @media (max-width: 768px) {
        .user-message, .assistant-message {
            max-width: 90% !important;
            padding: 12px 16px !important;
            margin: 12px 4% 12px auto !important;
        }
    }

    /* HEADER BOX */
    .header-box {
        background: linear-gradient(90deg, #ea580c, #c2410c) !important;
        padding: 2rem !important;
        border-radius: 20px !important;
        text-align: center !important;
        color: white !important;
        box-shadow: 0 10px 30px rgba(234,88,12,0.4) !important;
        margin: 0 auto 2rem auto !important;
    }
    @media (max-width: 768px) {
        .header-box { 
            padding: 1.5rem !important; 
        }
    }

    /* BELÉN BOX */
    .belén-box {
        background: #dc2626 !important;
        color: white !important;
        padding: 1.3rem !important;
        border-radius: 15px !important;
        text-align: center !important;
        font-weight: bold !important;
        margin: 2rem auto !important;
    }

    /* === CORRECCIÓN CRÍTICA: HACER EL INPUT DE CHAT VISIBLE === */
    [data-testid="stChatInput"] {
        display: block !important;
        visibility: visible !important;
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: #0e1117 !important;
        padding: 1rem !important;
        border-top: 1px solid #333 !important;
        z-index: 1000 !important;
    }

    /* MOSTRAR EL TEXTAREA DEL INPUT */
    [data-testid="stChatInput"] textarea {
        display: block !important;
        visibility: visible !important;
        width: 100% !important;
        background: #1e1e1e !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        outline: none !important;
        border-color: #ea580c !important;
    }

    /* OCULTAR SOLO EL AVATAR DEL INPUT, NO TODO EL CONTENEDOR */
    [data-testid="stChatInput"] [data-testid="stAvatar"],
    [data-testid="stChatInput"] img,
    [data-testid="stChatInput"] svg {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* MOSTRAR EL BOTÓN DE ENVÍO */
    [data-testid="stChatInput"] button {
        display: block !important;
        visibility: visible !important;
        background: #ea580c !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
    }

    /* OCULTAR AVATARES EN MENSAJES DE CHAT */
    [data-testid="stChatMessage"] img,
    [data-testid="stChatMessage"] svg,
    [data-testid="stChatMessage"] [data-testid="stAvatar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }
</style>
'''

# Aplica el CSS
st.markdown(css_code, unsafe_allow_html=True)

# ==================== INICIALIZACIÓN ====================
API_KEY = os.getenv("OPENAI_API_KEY")

# ==================== CONTENIDO DEL CHATBOT ====================
# Header
st.markdown(
    '''
    <div class="header-box">
        <h1 style="margin:0; font-size: 2.2rem;">Chatbot Colaboradores</h1>
        <h2 style="margin:8px 0 0 0; font-weight:300; font-size: 1.3rem;">Nutrisco – Atención Personas</h2>
        <p style="margin:15px 0 0 0; opacity: 0.9;">Escribe tu duda y te respondo al instante</p>
    </div>
    ''', 
    unsafe_allow_html=True
)

# Mensaje de bienvenida
st.markdown(
    '''
    <div class="assistant-message">
        ¡Hola! 👋 Soy parte del equipo de <strong>Atención a Personas</strong> de Nutrisco.<br><br>
        Puedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.<br><br>
        ¡Estoy aquí para ayudarte!
    </div>
    ''', 
    unsafe_allow_html=True
)

# ==================== LÓGICA DEL CHAT ====================
# Inicializar mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de mensajes
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

# Input de chat - ESTA ES LA PARTE CRÍTICA QUE DEBE FUNCIONAR
user_input = st.chat_input("Escribe tu consulta aquí...")

if user_input:
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Mostrar mensaje del usuario
    st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)
    
    # Mostrar indicador de escritura
    with st.spinner("Escribiendo respuesta..."):
        time.sleep(1)
        
        # Obtener respuesta
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
                respuesta = response.json()["choices"][0]["message"]["content"]
            else:
                respuesta = "⚠️ Error: No se configuró OPENAI_API_KEY"
        except Exception as e:
            respuesta = f"⚠️ Error de conexión. Contacta a Belén Bastías: belen.bastias@nutrisco.com"
        
        # Agregar y mostrar respuesta
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        st.markdown(f'<div class="assistant-message">{respuesta}</div>', unsafe_allow_html=True)
    
    # Recargar para limpiar input
    st.rerun()

# Footer
st.markdown(
    '''
    <div style="text-align:center; margin-top: 4rem; color: #64748b; padding: 2rem;">
        <br>
        Inteligencia Artificial al servicio de las personas – Nutrisco © 2025
    </div>
    ''', 
    unsafe_allow_html=True
)
