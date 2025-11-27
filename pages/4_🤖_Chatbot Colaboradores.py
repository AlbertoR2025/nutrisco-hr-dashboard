# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN DEFINITIVA (sin errores + 100% humana)
import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Agrega esto justo después de los imports
st.markdown("""
<style>
    /* Ocultar avatar del usuario, corona y barra de herramientas en chat */
    .st-emotion-cache-1r1k0y8 { display: none !important; }  /* Oculta la corona y avatar */
    .st-emotion-cache-1b7s5q1 { display: none !important; }  /* Oculta la barra superior con foto */
    .stToolbar { display: none !important; }                  /* Oculta toda la toolbar de Streamlit */
    .stDeployButton { display: none !important; }             /* Oculta botón Deploy rojo */
    .st-emotion-cache-1f3q5l2 { display: none !important; } /* Avatar del usuario en chat */
    .st-emotion-cache-1p0r8n3 { display: none !important; } /* Corona y badge */
    .st-emotion-cache-1q2s4t5 { display: none !important; } /* Botón de herramientas adicionales */
    .stAppView .main .block-container { padding-top: 1rem; }  /* Ajusta padding para que quede limpio */
</style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Falta OPENAI_API_KEY en .env")
    st.stop()

# ==================== ESTILO VISUAL PRO + HUMANO ====================
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
    .footer {text-align: center; margin-top: 4rem; color: #64748b; font-size: 0.9rem;}
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

# Inicializar chat
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"
    }]

# Mostrar mensajes anteriores
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

# Input + efecto humano
if pregunta := st.chat_input("Escribe tu consulta aquí..."):
    # 1. Guardar y mostrar pregunta
    st.session_state.messages.append({"role": "user", "content": pregunta})
    st.markdown(f'<div class="user-message">{pregunta}</div>', unsafe_allow_html=True)

    # 2. Efecto "Escribiendo..." (1.3 segundos)
    placeholder = st.empty()
    placeholder.markdown('<div class="typing">Escribiendo<span style="animation: blink 1s infinite;">...</span></div>', unsafe_allow_html=True)
    import time; time.sleep(1.3)
    placeholder.empty()

    # 3. Llamar a ChatGPT
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Eres una persona real del equipo de RR.HH. de Nutrisco. Hablas en español, súper cercano, cálido y profesional. Nunca digas que eres IA. Si es tema delicado (acoso, conflicto, agresión), deriva con mucho tacto a Belén Bastías (interno 7219)."},
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

    # 4. Mostrar respuesta
    st.markdown(f'<div class="assistant-message">{respuesta}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

    # 5. Tema sensible → caja roja
    if any(palabra in pregunta.lower() for palabra in ["agresi", "acoso", "conflicto", "denuncia", "pelea", "maltrato", "insulto"]):
        st.markdown("""
        <div class="belén-box">
            Este tema es muy importante<br>
            <strong>Belén Bastías Hurtado</strong> te puede ayudar personalmente<br>
            Correo: belen.bastias@nutrisco.com | Interno: 7219
        </div>
        """, unsafe_allow_html=True)

    # 6. GUARDAR EN EXCEL (siempre)
    nuevo = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Pregunta": pregunta,
        "Respuesta": respuesta
    }])
    archivo = "data/historial_chatbot.xlsx"
    if os.path.exists(archivo):
        historial = pd.read_excel(archivo)
        historial = pd.concat([historial, nuevo], ignore_index=True)
    else:
        historial = nuevo
    historial.to_excel(archivo, index=False)

    # 7. Recargar suavemente (funciona en todas las versiones)
    st.rerun()   # ← ESTA ES LA LÍNEA CORRECTA

# Footer limpio y corporativo (solo Nutrisco)
st.markdown("""
<div class="footer">
    <p style="margin:0; font-size:0.95rem; color:#94a3b8;">
        Inteligencia Artificial al servicio de las personas – Nutrisco
    </p>
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
