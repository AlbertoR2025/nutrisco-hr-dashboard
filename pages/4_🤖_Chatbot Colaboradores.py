# pages/4_Chatbot Colaboradores.py → VERSIÓN FINAL DEFINITIVA 100% LIMPIA Y CORPORATIVA
import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ==================== ELIMINAR TODO EL BRANDING DE STREAMLIT (avatar, corona, deploy, toolbar) ====================
st.markdown("""
<style>
    /* OCULTAR COMPLETAMENTE TODO LO DE STREAMLIT */
    div[data-testid="stToolbar"] {display: none !important;}
    div[data-testid="collapsedControl"] {display: none !important;}
    button[title="Deploy"] {display: none !important;}
    button[title="View source code"] {display: none !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    section[data-testid="stSidebar"] + div {padding-top: 0 !important;}
    .stChatFloatingInputContainer {padding-bottom: 0px !important;}
    .main > div {padding-top: 0rem !important;}
</style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Falta OPENAI_API_KEY en .env o en Streamlit Secrets")
    st.stop()

# ==================== ESTILO VISUAL NUTRISCO ====================
st.set_page_config(page_title="Chatbot RR.HH. Nutrisco", page_icon="speech_balloon", layout="centered")

st.markdown("""
<style>
    .main {background-color: #0e1117; padding: 2rem;}
    .user-message {
        background: #262730; color: white; border-radius: 18px;
        padding: 14px 18px; margin: 12px 0; max-width: 80%; margin-left: auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .assistant-message {
        background: linear-gradient(135deg, #ea580c, #f97316); color: white;
        border-radius: 18px; padding: 14px 18px; margin: 12px 0; max-width: 80%;
        margin-right: auto; box-shadow: 0 4px 12px rgba(249,115,22,0.4);
    }
    .header-box {
        background: linear-gradient(90deg, #ea580c, #c2410c);
        padding: 2rem; border-radius: 20px; text-align: center; color: white;
        margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(234,88,12,0.4);
    }
    .belén-box {
        background: #dc2626; color: white; padding: 1.2rem; border-radius: 15px;
        text-align: center; font-weight: bold; margin: 1.5rem 0; font-size: 1.1rem;
    }
    .typing {font-style: italic; color: #94a3b8; text-align: left; margin: 15px 0;}
    .footer {text-align: center; margin-top: 4rem; color: #94a3b8; font-size: 0.95rem;}
</style>
""", unsafe_allow_html=True)

# ==================== CABECERA ====================
st.markdown("""
<div class="header-box">
    <h1 style="margin:0;">Chatbot Colaboradores</h1>
    <h2 style="margin:8px 0 0 0; font-weight:300;">Nutrisco – Atención Personas</h2>
    <p style="margin:15px 0 0 0;">Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

# ==================== INICIALIZAR CHAT ====================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"
    }]

# ==================== MOSTRAR HISTORIAL ====================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

# ==================== INPUT DEL USUARIO ====================
if pregunta := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": pregunta})
    st.markdown(f'<div class="user-message">{pregunta}</div>', unsafe_allow_html=True)

    placeholder = st.empty()
    placeholder.markdown('<div class="typing">Escribiendo<span style="animation: blink 1s infinite;">...</span></div>', unsafe_allow_html=True)
    import time; time.sleep(1.3)
    placeholder.empty()

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Eres una persona real del equipo de RR.HH. de Nutrisco. Hablas en español, súper cercano y profesional. Nunca digas que eres IA. Si es tema delicado, deriva con tacto a Belén Bastías (interno 7219)."},
                    {"role": "user", "content": pregunta}
                ],
                "temperature": 0.7,
                "max_tokens": 600
            },
            timeout=30
        )
        respuesta = response.json()["choices"][0]["message"]["content"]
    except:
        respuesta = "Uy, justo ahora tengo un pequeño problema de conexión. Mejor llámame al interno 7219 o escribe a belen.bastias@nutrisco.com. ¡Perdona las molestias!"

    st.markdown(f'<div class="assistant-message">{respuesta}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

    # Tema sensible
    if any(p in pregunta.lower() for p in ["agresi", "acoso", "conflicto", "denuncia", "pelea", "maltrato", "insulto"]):
        st.markdown("""
        <div class="belén-box">
            Este tema es muy importante<br>
            <strong>Belén Bastías Hurtado</strong> te puede ayudar personalmente<br>
            Correo: belen.bastias@nutrisco.com | Interno: 7219
        </div>
        """, unsafe_allow_html=True)

    # Guardar historial
    nuevo = pd.DataFrame([{"Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"), "Pregunta": pregunta, "Respuesta": respuesta}])
    archivo = "data/historial_chatbot.xlsx"
    if os.path.exists(archivo):
        historial = pd.read_excel(archivo)
        historial = pd.concat([historial, nuevo], ignore_index=True)
    else:
        historial = nuevo
    historial.to_excel(archivo, index=False)

    st.rerun()

# ==================== FOOTER CORPORATIVO LIMPIO ====================
st.markdown("""
<div style="text-align:center; padding:2rem 0 1rem 0; color:#94a3b8; font-size:0.95rem;">
    Inteligencia Artificial al servicio de las personas – Nutrisco
</div>
""", unsafe_allow_html=True)

# Animación puntitos
st.markdown("""
<style>
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}
</style>
""", unsafe_allow_html=True)
