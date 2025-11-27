# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN DEFINITIVA 100% SIN AVATARES NI CORONA – CENTRADO PERFECTO (NOV 2025)
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
    layout="wide",  # Cambiado a 'wide' para mejor centrado
    initial_sidebar_state="collapsed"
)

# ==================== CSS ULTRA-AGRESIVO: ELIMINAR AVATARES, CORONA, HOSTED BY, TODO (NOV 2025) ====================
st.markdown("""
<style>
    /* ELIMINAR HEADER COMPLETO, TOOLBAR, DEPLOY, FOOTER */
    header, footer, [data-testid="stHeader"], [data-testid="stToolbar"], 
    [data-testid="collapsedControl"], [data-testid="stDecoration"], 
    [data-testid="stStatusWidget"], #MainMenu, .stDeployButton, 
    button[title*="Deploy"], button[title*="View source"] { 
        display: none !important; visibility: hidden !important; height: 0px !important; 
    }

    /* ELIMINAR AVATARES Y CORONA EN CHAT_MESSAGE (selectores 2025) */
    [data-testid="stChatMessage"] img, [data-testid="stChatMessage"] svg,
    [data-testid="stAvatar"], [data-testid="stChatMessageAvatar"],
    div[class*="css-"][alt*="avatar"], div[class*="e"][alt*="avatar"],
    .css-1d391kg img, .e1d0834u0, .css-h1sjnp { 
        display: none !important; visibility: hidden !important; 
        width: 0px !important; height: 0px !important; opacity: 0 !important; 
    }

    /* ELIMINAR 'HOSTED WITH STREAMLIT' Y CUALQUIER PIE */
    div[class*="hosted"], div:contains("Streamlit"), footer > div { display: none !important; }

    /* AJUSTAR LAYOUT DEL CHAT SIN AVATARES (gap=0, padding=0) */
    [data-testid="stChatMessage"] > div > div:first-child { 
        display: none !important; width: 0px !important; min-width: 0px !important; 
    }
    [data-testid="stChatMessage"] > div { 
        gap: 0px !important; padding-left: 0px !important; padding-right: 0px !important; 
        justify-content: flex-start !important; 
    }

    /* CENTRADO PERFECTO: Contenedor principal centrado al 90% */
    .main .block-container { 
        max-width: 90% !important; margin: 0 auto !important; padding: 1rem !important; 
    }
    .stApp { background-color: #0e1117; }

    /* ESTILOS PERSONALIZADOS (mantener tu diseño naranja) */
    .user-message {
        background: #262730; color: white; border-radius: 18px; padding: 14px 20px;
        margin: 16px 0; max-width: 80%; margin-left: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.4);
    }
    .assistant-message {
        background: linear-gradient(135deg, #ea580c, #f97316); color: white; border-radius: 18px; 
        padding: 14px 20px; margin: 16px 0; max-width: 80%; margin-right: auto; 
        box-shadow: 0 4px 15px rgba(249,115,22,0.5);
    }
    .header-box {
        background: linear-gradient(90deg, #ea580c, #c2410c); padding: 2.5rem 2rem; border-radius: 20px; 
        text-align: center; color: white; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(234,88,12,0.4);
    }
    .belén-box {
        background: #dc2626; color: white; padding: 1.3rem; border-radius: 15px; text-align: center; 
        font-weight: bold; margin: 2rem 0; font-size: 1.15rem; box-shadow: 0 4px 15px rgba(220,38,38,0.4);
    }
    .typing {
        font-style: italic; color: #94a3b8; margin: 15px 0;
    }
    .footer {
        text-align: center; margin-top: 4rem; color: #64748b; font-size: 0.95rem; padding: 2rem 0;
    }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# ==================== CLAVE OPENAI ====================
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("⚠️ Falta la clave OPENAI_API_KEY en Secrets o .env")
    st.stop()

# ==================== CONTENEDOR CENTRADO ====================
container = st.container()
with container:
    # ==================== CABECERA CORPORATIVA ====================
    st.markdown("""
    <div class="header-box">
        <h1 style="margin:0; font-size: 2.4rem; font-weight: 800;">Chatbot Colaboradores</h1>
        <h2 style="margin:10px 0 0 0; font-weight: 400; font-size: 1.4rem;">Nutrisco – Atención Personas</h2>
        <p style="margin:15px 0 0 0; opacity: 0.9;">Escribe tu duda y te respondo al instante</p>
    </div>
    """, unsafe_allow_html=True)

    # ==================== INICIALIZAR CHAT ====================
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "¡Hola! 👋 Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"
        }]

    # ==================== MOSTRAR HISTORIAL CON AVATAR=NONE ====================
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=None):  # ¡CLAVE: avatar=None elimina avatares!
            st.markdown(f'<div class="{ "user-message" if msg["role"] == "user" else "assistant-message" }">{msg["content"]}</div>', unsafe_allow_html=True)

    # ==================== INPUT Y PROCESAMIENTO ====================
    if pregunta := st.chat_input("Escribe tu consulta aquí..."):
        # Agregar mensaje del usuario con avatar=None
        st.session_state.messages.append({"role": "user", "content": pregunta})
        with st.chat_message("user", avatar=None):
            st.markdown(f'<div class="user-message">{pregunta}</div>', unsafe_allow_html=True)

        # Typing indicator
        with st.chat_message("assistant", avatar=None):
            placeholder = st.empty()
            placeholder.markdown('<div class="typing">Escribiendo<span style="animation: blink 1s infinite;">...</span></div>', unsafe_allow_html=True)
            time.sleep(1.3)  # Simular delay

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

        placeholder.empty()
        with st.chat_message("assistant", avatar=None):
            st.markdown(f'<div class="assistant-message">{respuesta}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

        # Temas sensibles → caja roja con Belén
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

        st.rerun()

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco  © 2025
</div>
""", unsafe_allow_html=True)
