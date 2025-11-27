# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN FINAL CON STREAMLIT-CHAT: SIN AVATARES NI CORONA, 100% CORPORATIVO (NOV 2025)
import streamlit as st
import pandas as pd
import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from streamlit_chat import message  # INSTALADO CON pip install streamlit-chat
load_dotenv()

# ==================== CONFIGURACIÓN GLOBAL ====================
st.set_page_config(
    page_title="Chatbot Colaboradores – Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CSS LIGERO: OCULTA RESIDUALES, LAYOUT RESPONSIVO ====================
st.markdown("""
<style>
    /* OCULTAR CORONA ROJA Y HOSTED FOOTER (FIX 2025) */
    .stDeployButton, button[data-testid="stDeployButton"], footer, [data-testid="stStatusWidget"], div[class*="hosted"] {display: none !important;}

    /* LAYOUT CENTRADO RESPONSIVO (SIN DESCUADRADO) */
    .main .block-container {max-width: 800px !important; margin: 0 auto !important; padding: 1rem !important;}
    @media (max-width: 768px) {.main .block-container {width: 95% !important; padding: 0.5rem !important;}}
    .stApp {background-color: #0e1117 !important;}

    /* ESTILOS HEADER Y FOOTER */
    .header-box {background: linear-gradient(90deg, #ea580c, #c2410c) !important; padding: 2rem !important; border-radius: 20px !important; text-align: center !important; color: white !important; box-shadow: 0 10px 30px rgba(234,88,12,0.4) !important;}
    @media (max-width: 768px) {.header-box {padding: 1.5rem !important;}}
    .belén-box {background: #dc2626 !important; color: white !important; padding: 1.3rem !important; border-radius: 15px !important; text-align: center !important; font-weight: bold !important; margin: 2rem auto !important;}
    .footer {text-align: center !important; margin-top: 4rem !important; color: #64748b !important; font-size: 0.95rem !important; padding: 2rem 0 !important;}
</style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("⚠️ Falta la clave OPENAI_API_KEY en Secrets o .env")
    st.stop()

# ==================== CABECERA CORPORATIVA ====================
st.markdown("""
<div class="header-box">
    <h1 style="margin:0; font-size: 2.4rem; font-weight: 800;">Chatbot Colaboradores</h1>
    <h2 style="margin:10px 0 0 0; font-weight: 400; font-size: 1.4rem;">Nutrisco – Atención Personas</h2>
    <p style="margin:15px 0 0 0; opacity: 0.9;">Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

# ==================== INICIALIZAR CHAT CON STREAMLIT-CHAT (SIN AVATARES) ====================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! 👋 Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"}]

# ==================== MOSTRAR HISTORIAL CON MESSAGE (SIN AVATARES) ====================
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=f"user_{i}")  # Usuario a la derecha, sin avatar
    else:
        message(msg["content"], key=f"assistant_{i}")  # Asistente a la izquierda, sin avatar

# ==================== INPUT PERSONALIZADO CON st.text_input (SIN AVATAR EN INPUT) ====================
pregunta = st.text_input("Escribe tu consulta aquí...", key="user_input", placeholder="Escribe tu consulta aquí...")
if pregunta:
    st.session_state.messages.append({"role": "user", "content": pregunta})
    message(pregunta, is_user=True)  # Muestra usuario sin avatar

    # Typing simulado
    with st.spinner("Escribiendo..."):
        time.sleep(1.3)

    # Llamada a OpenAI
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 600,
                "messages": [
                    {"role": "system", "content": "Eres una persona real del equipo de RR.HH. de Nutrisco en Chile. Hablas español chileno, cercano, profesional y amable. Nunca digas que eres IA. Si el tema es delicado (acoso, conflicto, denuncia), deriva con mucho tacto a Belén Bastías."},
                    {"role": "user", "content": pregunta}
                ]
            },
            timeout=30
        )
        respuesta = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        respuesta = "Uy, justo ahora tengo un problema de conexión. Mejor escribe a **belen.bastias@nutrisco.com** o llama al interno **7219**. ¡Perdona las molestias!"

    message(respuesta, key="assistant_response")  # Muestra respuesta sin avatar
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

    # Temas sensibles
    sensibles = ["agresi", "acoso", "denuncia", "conflicto", "pelea", "maltrato", "insulto", "abus", "discrimin"]
    if any(p in pregunta.lower() for p in sensibles):
        st.markdown("""
        <div class="belén-box">
            Este tema es muy importante<br>
            <strong>Belén Bastías Hurtado</strong> te puede ayudar personalmente<br>
            📧 belen.bastias@nutrisco.com | ☎ Interno: 7219
        </div>
        """, unsafe_allow_html=True)

    # Guardar historial
    try:
        nuevo = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Pregunta": pregunta,
            "Respuesta": respuesta
        }])
        archivo = "data/historial_chatbot.xlsx"
        os.makedirs("data", exist_ok=True)
        if os.path.exists(archivo):
            df_antiguo = pd.read_excel(archivo)
            df_final = pd.concat([df_antiguo, nuevo], ignore_index=True)
        else:
            df_final = nuevo
        df_final.to_excel(archivo, index=False)
    except:
        pass

    st.rerun()  # Refresca para limpiar input

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco © 2025
</div>
""", unsafe_allow_html=True)
