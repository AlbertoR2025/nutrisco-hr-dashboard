import streamlit as st
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(
page_title="Chatbot Colaboradores – Nutrisco",
page_icon="💬",
layout="centered",
initial_sidebar_state="collapsed"
)

==================== CSS + JS ====================
st.markdown("""

<style> /* Ocultar header, footer, toolbar, deploy, github, etc. */ header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"], .stAppDeployButton, button[title*="Deploy"], button[title*="View"], [data-testid="baseButton-secondary"] { display: none !important; visibility: hidden !important; } /* Ocultar completamente el chat_input nativo y sus avatares */ [data-testid="stChatInput"], [data-testid="stChatInput"] [data-testid="stAvatar"], [data-testid="stChatInput"] img, [data-testid="stChatInput"] svg { display: none !important; visibility: hidden !important; height: 0 !important; width: 0 !important; overflow: hidden !important; } /* Ocultar avatares en mensajes */ [data-testid="stChatMessage"] [data-testid="stAvatar"], [data-testid="stChatMessage"] img, [data-testid="stChatMessage"] svg { display: none !important; visibility: hidden !important; } /* Layout principal */ .main .block-container { max-width: 800px !important; margin: 0 auto !important; padding: 1rem !important; padding-bottom: 120px !important; overflow: visible !important; } .stApp { background-color: #0e1117 !important; } /* Mensajes */ .user-msg { background: #262730; color: white; border-radius: 18px; padding: 14px 20px; margin: 12px 0 12px auto; max-width: 75%; box-shadow: 0 2px 10px rgba(0,0,0,0.4); } .assistant-msg { background: linear-gradient(135deg, #ea580c, #f97316); color: white; border-radius: 18px; padding: 14px 20px; margin: 12px auto 12px 0; max-width: 75%; box-shadow: 0 4px 15px rgba(249,115,22,0.5); } /* Header visual */ .header-box { background: linear-gradient(90deg, #ea580c, #c2410c); padding: 2rem; border-radius: 20px; text-align: center; color: white; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(234,88,12,0.4); } /* Input fijo personalizado */ .custom-input-container { position: fixed !important; bottom: 0 !important; left: 0 !important; right: 0 !important; background: #0e1117 !important; padding: 1rem !important; border-top: 1px solid #333 !important; z-index: 2147483647 !important; display: flex !important; justify-content: center !important; } .custom-input-wrapper { display: flex !important; gap: 10px !important; width: 90% !important; max-width: 800px !important; align-items: center !important; } .custom-text-input { flex: 1 !important; background: #1e1e1e !important; color: white !important; border: 1px solid #444 !important; border-radius: 25px !important; padding: 12px 20px !important; font-size: 16px !important; outline: none !important; } .custom-text-input:focus { border-color: #ea580c !important; box-shadow: 0 0 0 2px rgba(234, 88, 12, 0.2) !important; } .custom-send-button { background: #ea580c !important; color: white !important; border: none !important; border-radius: 50% !important; width: 50px !important; height: 50px !important; cursor: pointer !important; display: flex !important; align-items: center !important; justify-content: center !important; font-size: 18px !important; } .custom-send-button:hover { background: #c2410c !important; } /* Responsive */ @media (max-width: 768px) { .custom-input-wrapper { width: 95% !important; } .user-msg, .assistant-msg { max-width: 85% !important; } .header-box { padding: 1.5rem !important; } } </style>
""", unsafe_allow_html=True)

st.markdown("""

<script> function sendCustomMessage() { const input = document.getElementById('customChatInput'); const message = input.value.trim(); if (message) { const url = new URL(window.location); url.searchParams.set('user_message', message); window.history.pushState({}, '', url); window.location.reload(); } } document.addEventListener("DOMContentLoaded", function() { const input = document.getElementById('customChatInput'); if (input) { input.addEventListener('keypress', function(e) { if (e.key === 'Enter') sendCustomMessage(); }); setTimeout(() => input.focus(), 500); } }); </script>
""", unsafe_allow_html=True)

==================== UI ====================
st.markdown("""

<div class="header-box"> <h1 style="margin:0; font-size: 2.2rem;">Chatbot Colaboradores</h1> <h2 style="margin:8px 0 0 0; font-weight:300; font-size: 1.3rem;">Nutrisco – Atención Personas</h2> <p style="margin:15px 0 0 0; opacity: 0.9;">Escribe tu duda y te respondo al instante</p> </div> """, unsafe_allow_html=True)
st.markdown("""

<div class="assistant-msg"> <strong>¡Hola! 👋</strong> Soy parte del equipo de <strong>Atención a Personas</strong> de Nutrisco.<br><br> Puedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.<br><br> ¡Estoy aquí para ayudarte! </div> """, unsafe_allow_html=True)
if "messages" not in st.session_state:
st.session_state.messages = []

for m in st.session_state.messages:
if m["role"] == "user":
st.markdown(f'<div class="user-msg">{m["content"]}</div>', unsafe_allow_html=True)
else:
st.markdown(f'<div class="assistant-msg">{m["content"]}</div>', unsafe_allow_html=True)

Input personalizado fijo
st.markdown("""

<div class="custom-input-container"> <div class="custom-input-wrapper"> <input type="text" class="custom-text-input" id="customChatInput" placeholder="Escribe tu consulta aquí..." /> <button class="custom-send-button" onclick="sendCustomMessage()">➤</button> </div> </div> """, unsafe_allow_html=True)
==================== LÓGICA MENSAJES ====================
params = st.experimental_get_query_params()
user_message = params.get("user_message", [None])

if user_message and user_message != st.session_state.get("last_msg"):
st.session_state.last_msg = user_message
st.session_state.messages.append({"role": "user", "content": user_message})

text
with st.spinner("Pensando..."):
    time.sleep(1)
    try:
        if API_KEY:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Eres un asistente de RR.HH. de Nutrisco. Responde de manera profesional y cercana. Para temas delicados, deriva a Belén Bastías."
                        },
                        {"role": "user", "content": user_message}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=30
            )
            answer = resp.json()["choices"]["message"]["content"]
        else:
            answer = "Error: Falta configurar la API key."
    except Exception:
        answer = "Error de conexión. Contacta a Belén Bastías: belen.bastias@nutrisco.com"

st.session_state.messages.append({"role": "assistant", "content": answer})
st.experimental_set_query_params()
st.rerun()
