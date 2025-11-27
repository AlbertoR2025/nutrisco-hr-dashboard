# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN FINAL 2025: SIN FOTO/CORONA, SIMÉTRICO DESKTOP/MÓVIL
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

# ==================== CSS DEFINITIVO 2025 (SIN ROMPER EL CHAT) ====================
css_code = '''
<style>
    /* OCULTAR CORONA ROJA (DEPLOY BUTTON / CROWN) */
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

    /* OCULTAR AVATAR EN INPUT DE CHAT (SOLO LA IMAGEN/SVG) */
    [data-testid="stChatInput"] > div > div > div > img,
    [data-testid="stChatInput"] > div > div > div > svg,
    [data-testid="stChatInput"] > div > div > div > [alt*="avatar"],
    [data-testid="stChatInput"] > div > div > div > [data-testid="stAvatar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
    }

    /* OCULTAR AVATARES EN MENSAJES DEL CHAT (SOLO LA IMAGEN/SVG) */
    [data-testid="stChatMessage"] > div > img,
    [data-testid="stChatMessage"] > div > svg,
    [data-testid="stChatMessage"] > div > [data-testid="stAvatar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* LAYOUT SIMÉTRICO RESPONSIVO */
    .main .block-container {
        max-width: 800px !important;
        margin: 0 auto !important;
        padding: 1rem !important;
        width: auto !important;
    }
    @media (max-width: 768px) {
        .main .block-container { width: 95% !important; padding: 0.5rem !important; }
        [data-testid="stChatInput"] { max-width: 100% !important; margin: 0 auto !important; padding-bottom: 2rem !important; }
    }
    .stApp { background-color: #0e1117 !important; }

    /* ESTILOS MENSAJES SIMÉTRICOS */
    [data-testid="stChatMessage"] { padding: 0 !important; gap: 0 !important; }
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
        margin: 0 auto !important;
    }
    @media (max-width: 768px) {
        .header-box { padding: 1.5rem !important; }
    }

    /* BELÉN BOX */
    .belén-box {
        background: #dc2626 !important;
        color: white !important;
        padding: 1.3rem !important;
        border-radius: 15px !important;
        text-align: center !important;
    }

    /* EXTRA: OCULTAR BOTÓN DE "FORK" O "GITHUB" SI APARECE */
    [data-testid="stGitHubButton"], button[aria-label="Fork this app"], [data-testid="stToolbar"] {
        display: none !important;
    }

    /* OCULTAR SOLO EL CONTENEDOR DEL AVATAR EN INPUT (SI ES NECESARIO) */
    [data-testid="stChatInput"] > div > div > div {
        display: none !important;
    }
</style>
'''

# Aplica el CSS
st.write(css_code, unsafe_allow_html=True)

# ==================== CONTENIDO DEL CHATBOT ====================
st.markdown('<div class="header-box"><h1>Chatbot Colaboradores</h1><p>Nutrisco – Atención Personas</p><p>Escribe tu duda y te respondo al instante</p></div>', unsafe_allow_html=True)

# Mensaje inicial (IMPORTANTE: NO usar st.chat_message con avatar=None si quieres mantenerlo)
# En lugar de eso, usamos st.markdown para evitar problemas con CSS
st.markdown("""
<div style="padding: 16px; background: linear-gradient(135deg, #ea580c, #f97316); color: white; border-radius: 18px; margin: 16px auto 16px 8%; max-width: 75%; box-shadow: 0 4px 15px rgba(249,115,22,0.5); text-align: left;">
    ¡Hola! 🤝 Soy parte del equipo de <strong>Atención a Personas</strong> de Nutrisco.<br><br>
    Puedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.<br><br>
    ¡Estoy aquí para ayudarte!
</div>
""", unsafe_allow_html=True)

# Input de chat
user_input = st.chat_input("Escribe tu consulta aquí...")

if user_input:
    # Mensaje del usuario
    st.markdown(f"""
<div style="padding: 14px 20px; background: #262730; color: white; border-radius: 18px; margin: 16px 8% 16px auto; max-width: 75%; box-shadow: 0 2px 10px rgba(0,0,0,0.4); text-align: left;">
    {user_input}
</div>
""", unsafe_allow_html=True)

    # Respuesta del asistente
    st.markdown("""
<div style="padding: 14px 20px; background: linear-gradient(135deg, #ea580c, #f97316); color: white; border-radius: 18px; margin: 16px auto 16px 8%; max-width: 75%; box-shadow: 0 4px 15px rgba(249,115,22,0.5); text-align: left;">
    Gracias por tu pregunta. Estoy procesando la respuesta...
</div>
""", unsafe_allow_html=True)
