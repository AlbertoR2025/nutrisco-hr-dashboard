# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN FUNCIONAL
import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Chatbot Nutrisco", page_icon="💬", layout="centered")

# ELIMINA TODO LO DE STREAMLIT
st.markdown("""
<style>
    header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"], 
    .stDeployButton, [data-testid="stStatusWidget"], a[href*="github"], 
    a[href*="streamlit"] {display:none!important;}
    .stApp {background:#0e1117;}
    .block-container {max-width:900px;padding:1rem;padding-bottom:100px;}
    .header{background:linear-gradient(90deg,#ea580c,#c2410c);padding:2.5rem;border-radius:20px;text-align:center;color:white;margin-bottom:2rem;}
    .user{background:#262730;color:white;border-radius:18px;padding:14px 20px;margin:12px 8% 12px auto;max-width:75%;box-shadow:0 2px 10px rgba(0,0,0,0.4);}
    .bot{background:linear-gradient(135deg,#ea580c,#f97316);color:white;border-radius:18px;padding:14px 20px;margin:12px auto 12px 8%;max-width:75%;box-shadow:0 4px 15px rgba(249,115,22,0.5);}
    .footer{text-align:center;margin-top:4rem;color:#64748b;font-size:0.95rem;}
    
    /* INPUT FIJADO EN LA PARTE INFERIOR */
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #0e1117;
        padding: 15px;
        box-sizing: border-box;
        z-index: 1000;
        border-top: 1px solid #333;
    }
    .input-container {
        max-width: 900px;
        margin: 0 auto;
        display: flex;
        gap: 10px;
        align-items: center;
    }
    .text-input {
        flex: 1;
        padding: 16px 20px;
        border-radius: 30px;
        border: 1px solid #444;
        background: #1f2937;
        color: white;
        font-size: 1.1rem;
    }
    .send-button {
        background: #ea580c;
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        cursor: pointer;
        font-size: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Falta OPENAI_API_KEY")
    st.stop()

st.markdown('<div class="header"><h1>Chatbot Colaboradores</h1><h2>Nutrisco – Atención Personas</h2><p>Escribe tu duda y te respondo al instante</p></div>', unsafe_allow_html=True)

# Inicializar mensajes
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"bot","content":"¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"}]

# Mostrar historial
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot">{msg["content"]}</div>', unsafe_allow_html=True)

# INPUT FUNCIONAL CON st.text_input Y BOTÓN
st.markdown('<div class="fixed-input">', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "Escribe tu consulta aquí...", 
        placeholder="Escribe tu consulta aquí...", 
        key="chat_input",
        label_visibility="collapsed"
    )
with col2:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)  # Espacio para alinear
    send_button = st.button("➤", key="send_button", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# PROCESAR MENSAJE CUANDO SE PRESIONA EL BOTÓN
if send_button and user_input:
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role":"user","content":user_input})
    st.markdown(f'<div class="user">{user_input}</div>', unsafe_allow_html=True)
    
    # Obtener respuesta
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 600,
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres del equipo RRHH Nutrisco Chile. Hablas español chileno cercano y profesional. Para temas delicados, deriva a Belén Bastías."
                    },
                    {"role": "user", "content": user_input}
                ]
            },
            timeout=30
        )
        respuesta = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        respuesta = "⚠️ Problema de conexión. Contacta a Belén Bastías: belen.bastias@nutrisco.com"

    # Agregar y mostrar respuesta
    st.session_state.messages.append({"role":"bot","content":respuesta})
    st.markdown(f'<div class="bot">{respuesta}</div>', unsafe_allow_html=True)
    
    # Detectar temas sensibles
    temas_sensibles = ["agresi", "acoso", "denuncia", "conflicto", "pelea", "maltrato", "insulto"]
    if any(p in user_input.lower() for p in temas_sensibles):
        st.markdown("""
        <div style="background:#dc2626;color:white;padding:1.3rem;border-radius:15px;text-align:center;font-weight:bold;margin:2rem auto;max-width:75%;">
            💡 <strong>Para este tema específico</strong><br>
            Contacta directamente a <strong>Belén Bastías Hurtado</strong><br>
            📧 belen.bastias@nutrisco.com | ☎ Interno: 7219
        </div>
        """, unsafe_allow_html=True)
    
    # Recargar para limpiar input
    st.rerun()

# Footer
st.markdown('<div class="footer"><br>Inteligencia Artificial al servicio de las personas – Nutrisco © 2025</div>', unsafe_allow_html=True)
