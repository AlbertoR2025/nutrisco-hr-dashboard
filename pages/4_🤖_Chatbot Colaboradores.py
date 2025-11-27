# pages/4_🤖_Chatbot Colaboradores.py → 100% LIMPIO 2025 (SIN AVATAR, SIN CORONA, SIN NADA)
import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Chatbot Nutrisco", page_icon="💬", layout="centered")

# OCULTAR TODO LO DE STREAMLIT
st.markdown("""
<style>
    header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"], 
    .stDeployButton, [data-testid="stStatusWidget"], div[class*="hosted"] {display: none !important;}
    .stApp {background: #0e1117;}
    .block-container {max-width: 800px; padding: 1rem;}
    .header {background: linear-gradient(90deg, #ea580c, #c2410c); padding: 2.5rem; border-radius: 20px; text-align: center; color: white; box-shadow: 0 10px 30px rgba(234,88,12,0.4);}
    .user {background: #262730; color: white; border-radius: 18px; padding: 14px 20px; margin: 16px 5% 16px auto; max-width: 80%; box-shadow: 0 2px 10px rgba(0,0,0,0.4);}
    .assistant {background: linear-gradient(135deg, #ea580c, #f97316); color: white; border-radius: 18px; padding: 14px 20px; margin: 16px auto 16px 5%; max-width: 80%; box-shadow: 0 4px 15px rgba(249,115,22,0.5);}
    .footer {text-align: center; margin-top: 4rem; color: #64748b; font-size: 0.95rem;}
    .chat-input {position: fixed; bottom: 0; left: 0; width: 100%; background: #0e1117; padding: 1rem; box-sizing: border-box; z-index: 999;}
    .chat-input input {width: 100%; padding: 16px 20px; border-radius: 30px; border: none; background: #1f2937; color: white; font-size: 1.1rem;}
    .chat-input input:focus {outline: none; background: #374151;}
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

# INPUT HTML PERSONALIZADO (SIN AVATAR NI CORONA)
st.markdown("""
<div class="chat-input">
    <input type="text" id="pregunta" placeholder="Escribe tu consulta aquí..." autofocus>
</div>
<script>
    const input = document.getElementById('pregunta');
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && input.value.trim()) {
            Streamlit.setComponentValue(input.value.trim());
            input.value = '';
        }
    });
</script>
""", unsafe_allow_html=True)

pregunta = st.experimental_get_query_params().get("pregunta", [None])[0]
if pregunta:
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
        respuesta = "Problema de conexión. Escribe a belen.bastias@nutrisco.com"

    st.markdown(f'<div class="assistant">{respuesta}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})
    st.experimental_set_query_params()
    st.rerun()

st.markdown('<div class="footer"><br>Inteligencia Artificial al servicio de las personas – Nutrisco © 2025</div>', unsafe_allow_html=True)
