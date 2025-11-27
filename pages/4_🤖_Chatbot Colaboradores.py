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

# ==================== INYECTAR HTML EXTERNO ====================
# Lee el archivo HTML
try:
    with open("static/chatbot.html", "r", encoding="utf-8") as f:
        html_content = f.read()
except FileNotFoundError:
    html_content = ""

# Aplica el HTML
st.markdown(html_content, unsafe_allow_html=True)

# ==================== CONTENIDO DEL CHATBOT ====================
st.markdown('<div class="header-box"><h1>Chatbot Colaboradores</h1><p>Nutrisco – Atención Personas</p><p>Escribe tu duda y te respondo al instante</p></div>', unsafe_allow_html=True)

# Mensaje inicial
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
    st.markdown(f"""
<div style="padding: 14px 20px; background: #262730; color: white; border-radius: 18px; margin: 16px 8% 16px auto; max-width: 75%; box-shadow: 0 2px 10px rgba(0,0,0,0.4); text-align: left;">
    {user_input}
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="padding: 14px 20px; background: linear-gradient(135deg, #ea580c, #f97316); color: white; border-radius: 18px; margin: 16px auto 16px 8%; max-width: 75%; box-shadow: 0 4px 15px rgba(249,115,22,0.5); text-align: left;">
    Gracias por tu pregunta. Estoy procesando la respuesta...
</div>
""", unsafe_allow_html=True)
