# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN FINAL 100% LIMPIA (SIN NADA DE STREAMLIT) – FUNCIONA NOV 2025
import streamlit as st
import pandas as pd
import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Chatbot Colaboradores – Nutrisco", page_icon="💬", layout="centered")

# ==================== CSS + JS QUE SÍ FUNCIONA EN STREAMLIT CLOUD 2025 ====================
st.markdown("""
<style>
    /* OCULTAR TODO EL BRANDING DE STREAMLIT (corona, hosted, avatar, footer, toolbar) */
    header, footer, [data-testid="stToolbar"], [data-testid="stSidebar"], 
    [data-testid="stDeployButton"], button[kind="header"], .stDeployButton,
    [data-testid="stStatusWidget"], div[data-testid="collapsedControl"] {display: none !important;}
    
    /* OCULTAR AVATAR EN EL INPUT (EL CUADRADO CON CARA) */
    [data-testid="stChatInput"] img, [data-testid="stChatInput"] [kind="avatar"], 
    [data-testid="stChatInput"] svg {display: none !important; width:0 !important; height:0 !important;}
    
    /* OCULTAR AVATARES EN MENSAJES */
    [data-testid="stChatMessage"] img, [data-testid="stChatMessage"] svg {display: none !important;}
    
    /* FONDO Y CENTRADO PERFECTO */
    .main > div {padding-top: 0rem;}
    .block-container {max-width: 800px; padding: 1rem;}
    @media (max-width: 768px) {.block-container {padding: 0.5rem; width: 95% !important;}}
    .stApp {background: #0e1117;}
    
    /* ESTILOS NUTRISCO */
    .header-box {background: linear-gradient(90deg, #ea580c, #c2410c); padding: 2.5rem 2rem; border-radius: 20px; text-align: center; color: white; box-shadow: 0 10px 30px rgba(234,88,12,0.4);}
    .user {background: #262730; color: white; border-radius: 18px; padding: 14px 20px; margin: 16px 0 16px auto; max-width: 80%; box-shadow: 0 2px 10px rgba(0,0,0,0.4);}
    .assistant {background: linear-gradient(135deg, #ea580c, #f97316); color: white; border-radius: 18px; padding: 14px 20px; margin: 16px auto 16px 0; max-width: 80%; box-shadow: 0 4px 15px rgba(249,115,22,0.5);}
    .footer {text-align: center; margin-top: 4rem; color: #64748b; font-size: 0.95rem;}
</style>
""", unsafe_allow_html=True)

# ==================== CLAVE OPENAI ====================
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Falta OPENAI_API_KEY")
    st.stop()

# ==================== HEADER ====================
st.markdown('<div class="header-box"><h1 style="margin:0">Chatbot Colaboradores</h1><h2 style="margin:10px 0 0 0">Nutrisco – Atención Personas</h2><p>Escribe tu duda y te respondo al instante</p></div>', unsafe_allow_html=True)

# ==================== INICIALIZAR ====================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"}]

# ==================== MOSTRAR MENSAJES (SIN AVATARES) ====================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant">{msg["content"]}</div>', unsafe_allow_html=True)

# ==================== INPUT Y RESPUESTA ====================
if pregunta := st.chat_input("Escribe tu consulta aquí..."):
    # Usuario
    st.session_state.messages.append({"role": "user", "content": pregunta})
    st.markdown(f'<div class="user">{pregunta}</div>', unsafe_allow_html=True)
    
    # Typing
    typing = st.empty()
    typing.markdown('<div class="assistant">Escribiendo...</div>', unsafe_allow_html=True)
    time.sleep(1.5)
    typing.empty()
    
    # OpenAI
    try:
        resp = requests.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "gpt-4o-mini", "temperature": 0.7, "max_tokens": 600,
                  "messages": [{"role": "system", "content": "Eres del equipo de RR.HH. de Nutrisco Chile. Hablas español chileno cercano y profesional. Nunca digas que eres IA."},
                               {"role": "user", "content": pregunta}]}, timeout=30)
        respuesta = resp.json()["choices"][0]["message"]["content"]
    except:
        respuesta = "Uy, problema de conexión. Escribe a belen.bastias@nutrisco.com o llama al interno 7219."

    st.markdown(f'<div class="assistant">{respuesta}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

    # Temas sensibles
    if any(pal in pregunta.lower() for pal in ["acoso","denuncia","conflicto","maltrato"]):
        st.markdown('<div style="background:#dc2626;color:white;padding:1.3rem;border-radius:15px;text-align:center;font-weight:bold;margin:2rem 0;">Tema importante<br><strong>Belén Bastías</strong><br>belen.bastias@nutrisco.com | Interno 7219</div>', unsafe_allow_html=True)

    # Guardar historial
    try:
        df = pd.DataFrame([{"Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"), "Pregunta": pregunta, "Respuesta": respuesta}])
        file = "data/historial_chatbot.xlsx"
        os.makedirs("data", exist_ok=True)
        if os.path.exists(file):
            df.to_excel(file, mode="a", header=False, index=False)
        else:
            df.to_excel(file, index=False)
    except: pass

    st.rerun()

# ==================== FOOTER ====================
st.markdown('<div class="footer"><br>Inteligencia Artificial al servicio de las personas – Nutrisco © 2025</div>', unsafe_allow_html=True)
