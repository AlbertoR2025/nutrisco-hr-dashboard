# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN ULTRA-LIMPIA: SIN CHAT_MESSAGE, 100% CSS PERSONALIZADO, RESPONSIVO MÓVIL (NOV 2025)
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
    layout="centered",  # Centrado responsivo
    initial_sidebar_state="collapsed"
)

# ==================== CSS DEFINITIVO: SIN AVATARES, RESPONSIVO, ANTI-CACHE (2025) ====================
st.markdown("""
<style>
    /* ELIMINAR TODO LO DE STREAMLIT (header, toolbar, footer, hosted) */
    header, footer, [data-testid="stHeader"], [data-testid="stToolbar"], 
    [data-testid="collapsedControl"], [data-testid="stDecoration"], 
    [data-testid="stStatusWidget"], #MainMenu, .stDeployButton, 
    button[title*="Deploy"], button[title*="View source"], 
    div[class*="hosted"], div:contains("Streamlit") { 
        display: none !important; visibility: hidden !important; height: 0px !important; 
        opacity: 0 !important; 
    }

    /* CONTENEDOR PRINCIPAL RESPONSIVO (centrado perfecto en móvil/desktop) */
    .main .block-container { 
        max-width: 800px !important; margin: 0 auto !important; padding: 1rem !important; 
        width: 95% !important; 
    }
    @media (max-width: 768px) { 
        .main .block-container { width: 98% !important; padding: 0.5rem !important; } 
    }
    .stApp { background-color: #0e1117; }

    /* MENSAJES PERSONALIZADOS (sin chat_message, puro CSS) */
    .chat-container { max-width: 100%; margin: 0 auto; }
    .user-message {
        background: #262730; color: white; border-radius: 18px; padding: 14px 20px;
        margin: 16px 0; max-width: 80%; margin-left: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.4);
        word-wrap: break-word; 
    }
    .assistant-message {
        background: linear-gradient(135deg, #ea580c, #f97316); color: white; border-radius: 18px; 
        padding: 14px 20px; margin: 16px 0; max-width: 80%; margin-right: auto; 
        box-shadow: 0 4px 15px rgba(249,115,22,0.5); word-wrap: break-word;
    }
    @media (max-width: 768px) { 
        .user-message, .assistant-message { max-width: 95% !important; padding: 12px 16px !important; font-size: 1.1rem !important; } 
    }

    /* HEADER CORPORATIVO */
    .header-box {
        background: linear-gradient(90deg, #ea580c, #c2410c); padding: 2rem; border-radius: 20px; 
        text-align: center; color: white; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(234,88,12,0.4);
    }
    @media (max-width: 768px) { .header-box { padding: 1.5rem !important; } }

    /* CAJA BELÉN (temas sensibles) */
    .belén-box {
        background: #dc2626; color: white; padding: 1.3rem; border-radius: 15px; text-align: center; 
        font-weight: bold; margin: 2rem 0; font-size: 1.15rem; box-shadow: 0 4px 15px rgba(220,38,38,0.4);
    }
    @media (max-width: 768px) { .belén-box { font-size: 1rem !important; padding: 1rem !important; } }

    /* TYPING INDICATOR */
    .typing {
        font-style: italic; color: #94a3b8; margin: 15px 0; text-align: left;
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

# ==================== CABECERA CORPORATIVA ====================
st.markdown("""
<div class="header-box">
    <h1 style="margin:0; font-size: 2.4rem; font-weight: 800;">Chatbot Colaboradores</h1>
    <h2 style="margin:10px 0 0 0; font-weight: 400; font-size: 1.4rem;">Nutrisco – Atención Personas</h2>
    <p style="margin:15px 0 0 0; opacity: 0.9;">Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

# ==================== CONTENEDOR CHAT RESPONSIVO ====================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# ==================== INICIALIZAR CHAT ====================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "¡Hola! 👋 Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"
    }]

# ==================== MOSTRAR HISTORIAL CON MARKDOWN ====================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

# ==================== INPUT Y PROCESAMIENTO ====================
if pregunta := st.chat_input("Escribe tu consulta aquí..."):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": pregunta})
    st.markdown(f'<div class="user-message">{pregunta}</div>', unsafe_allow_html=True)

    # Typing indicator
    st.markdown('<div class="typing">Escribiendo<span style="animation: blink 1s infinite;">...</span></div>', unsafe_allow_html=True)
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

    # Limpiar typing y mostrar respuesta
    st.experimental_rerun()  # Para limpiar el typing (en 2025, usa st.rerun() si experimental no funciona)

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

st.markdown('</div>', unsafe_allow_html=True)  # Cierra chat-container

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco © 2025<br>
    Desarrollado por Alberto Reyes
</div>
""", unsafe_allow_html=True)
