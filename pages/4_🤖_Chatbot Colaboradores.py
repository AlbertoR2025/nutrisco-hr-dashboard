# pages/4_🤖_Chatbot Colaboradores.py → 100% LIMPIO Y SIMÉTRICO – FUNCIONA 27 NOV 2025
import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Chatbot Nutrisco", page_icon="💬", layout="centered")

# CSS QUE SÍ ELIMINA FOTO Y CORONA EN 2025
st.markdown("""
<style>
    /* OCULTA TODO LO DE STREAMLIT */
    header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"], 
    .stDeployButton, [data-testid="stStatusWidget"], .stAppDeployButton {display: none !important;}
    
    /* OCULTA FOTO Y CORONA EN EL INPUT */
    [data-testid="stChatInput"] > div > div > div:first-child {display: none !important;}
    [data-testid="stChatInput"] img, [data-testid="stChatInput"] svg {display: none !important;}
    
    /* SIMETRÍA PERFECTA */
    .block-container {max-width: 800px; padding: 1rem;}
    @media (max-width: 768px) {.block-container {padding: 0.5rem; width: 95% !important;}}
    .stApp {background: #0e1117;}
    
    .header {background: linear-gradient(90deg, #ea580c, #c2410c); padding: 2.5rem; border-radius: 20px; text-align: center; color: white;}
    .user {background: #262730; color: white; border-radius: 18px; padding: 14px 20px; margin: 12px 8% 12px auto; max-width: 75%;}
    .assistant {background: linear-gradient(135deg, #ea580c, #f97316); color: white; border-radius: 18px; padding: 14px 20px; margin: 12px auto 12px 8%; max-width: 75%;}
    .footer {text-align: center; margin-top: 3rem; color: #64748b; font-size: 0.95rem; padding-bottom: 80px;}
</style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Falta OPENAI_API_KEY")
    st.stop()

st.markdown('<div class="header"><h1>Chatbot Colaboradores</h1><h2>Nutrisco – Atención Personas</h2><p>Escribe tu duda y te respondo al instante</p></div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"}]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant">{msg["content"]}</div>', unsafe_allow_html=True)

if pregunta := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": pregunta})
    st.markdown(f'<div class="user">{pregunta}</div>', unsafe_allow_html=True)
    
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "gpt-4o-mini", "temperature": 0.7, "max_tokens": 600,
                  "messages": [{"role": "system", "content": "Eres del equipo RRHH Nutrisco Chile. Hablas español chileno cercano y profesional."},
                               {"role": "user", "content": pregunta}]})
        respuesta = r.json()["choices"][0]["message"]["content"]
    except:
        respuesta = "Problema de conexión."

    st.markdown(f'<div class="assistant">{respuesta}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})
    st.rerun()

st.markdown('<div class="footer"><br>Inteligencia Artificial al servicio de las personas – Nutrisco © 2025</div>', unsafe_allow_html=True)
