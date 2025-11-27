# pages/4_Chatbot Colaboradores.py → VERSIÓN 100% LIMPIA FINAL (SIN AVATAR, SIN CORONA, SIN "Hosted with Streamlit")
import streamlit as st
import pandas as pd
import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Chatbot Colaboradores – Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CSS + JS DEFINITIVO: BORRA TODO LO DE STREAMLIT EN TIEMPO REAL ====================
st.markdown("""
<style>
    /* OCULTAR TODO LO DE STREAMLIT */
    header, footer, [data-testid="stHeader"], [data-testid="stToolbar"], 
    [data-testid="collapsedControl"], [data-testid="stDecoration"], 
    #MainMenu, .stDeployButton, button[title*="Deploy"] {display: none !important;}

    /* BORRAR "Hosted with Streamlit" + avatar + corona */
    div[data-testid="stAppViewContainer"] > footer,
    div[class*="hosted"], div:contains("Streamlit"),
    img[alt="user avatar"], .css-1kyx0lz img, .css-1d391kg img {display: none !important;}

    .main .block-container {max-width: 800px; padding: 1rem;}
    .stApp {background: #0e1117;}

    .header-box {background: linear-gradient(90deg, #ea580c, #c2410c); padding: 2.5rem 2rem; border-radius: 20px; text-align: center; color: white; box-shadow: 0 10px 30px rgba(234,88,12,0.4);}
    .user-message {background: #262730; color: white; border-radius: 18px; padding: 14px 20px; margin: 16px 0; max-width: 80%; margin-left: auto; box-shadow: 0 2px 10px rgba(0,0,0,0.4);}
    .assistant-message {background: linear-gradient(135deg, #ea580c, #f97316); color: white; border-radius: 18px; padding: 14px 20px; margin: 16px 0; max-width: 80%; margin-right: auto; box-shadow: 0 4px 15px rgba(249,115,22,0.5);}
    .belén-box {background: #dc2626; color: white; padding: 1.3rem; border-radius: 15px; text-align: center; font-weight: bold; margin: 2rem 0;}
    .footer {text-align: center; margin-top: 4rem; color: #64748b; font-size: 0.95rem;}
    
    /* Input personalizado (reemplaza st.chat_input) */
    .chat-input-container {position: fixed; bottom: 0; left: 0; width: 100%; background: #0e1117; padding: 1rem; box-sizing: border-box; z-index: 1000;}
    .chat-input {width: 100%; padding: 14px 20px; border-radius: 30px; border: none; background: #1f2937; color: white; font-size: 1.1rem;}
    .chat-input:focus {outline: none; background: #374151;}
</style>

<!-- JavaScript que borra cualquier rastro de Streamlit en tiempo real -->
<script>
    setInterval(() => {
        document.querySelectorAll('footer, [data-testid="stHeader"], img[alt="user avatar"], div:contains("Streamlit"), div:contains("Hosted")').forEach(el => el.remove());
    }, 500);
</script>
""", unsafe_allow_html=True)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Falta OPENAI_API_KEY")
    st.stop()

# ==================== HEADER ====================
st.markdown("""
<div class="header-box">
    <h1 style="margin:0; font-size: 2.4rem;">Chatbot Colaboradores</h1>
    <h2 style="margin:10px 0 0 0; font-weight: 400;">Nutrisco – Atención Personas</h2>
    <p style="margin:15px 0 0 0;">Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

# ==================== INICIALIZAR ====================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"
    }]

# ==================== MOSTRAR MENSAJES ====================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

# ==================== INPUT PERSONALIZADO ====================
st.markdown("""
<div class="chat-input-container">
    <form id="chatForm">
        <input type="text" class="chat-input" placeholder="Escribe tu consulta aquí..." id="userInput" autocomplete="off">
    </form>
</div>
<script>
    const input = document.getElementById('userInput');
    input.focus();
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const value = input.value.trim();
            if (value) {
                window.parent.document.querySelector('iframe').contentWindow.location.href = 
                    window.location.href.split('?')[0] + '?q=' + encodeURIComponent(value);
            }
            input.value = '';
        }
    });
</script>
""", unsafe_allow_html=True)

# ==================== PROCESAR PREGUNTA ====================
query = st.experimental_get_query_params().get("q", [None])[0]
if query:
    pregunta = query[0] if isinstance(query, list) else query
    st.session_state.messages.append({"role": "user", "content": pregunta})
    st.markdown(f'<div class="user-message">{pregunta}</div>', unsafe_allow_html=True)

    with st.spinner(""):
        time.sleep(1)
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={"model": "gpt-4o-mini", "temperature": 0.7, "max_tokens": 600,
                     "messages": [{"role": "system", "content": "Eres del equipo de RR.HH. de Nutrisco Chile. Hablas español chileno, cercano y profesional. Nunca digas que eres IA."},
                                  {"role": "user", "content": pregunta}]}, timeout=30)
            respuesta = response.json()["choices"][0]["message"]["content"]
        except:
            respuesta = "Uy, problema de conexión. Escribe a belen.bastias@nutrisco.com o llama al 7219."

    st.markdown(f'<div class="assistant-message">{respuesta}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

    # Temas sensibles
    if any(p in pregunta.lower() for p in ["acoso","denuncia","conflicto","maltrato"]):
        st.markdown('<div class="belén-box">Tema importante<br><strong>Belén Bastías</strong><br>belen.bastias@nutrisco.com | Interno 7219</div>', unsafe_allow_html=True)

    # Guardar historial
    try:
        nuevo = pd.DataFrame([{"Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"), "Pregunta": pregunta, "Respuesta": respuesta}])
        archivo = "data/historial_chatbot.xlsx"
        os.makedirs("data", exist_ok=True)
        if os.path.exists(archivo):
            df = pd.read_excel(archivo)
            pd.concat([df, nuevo], ignore_index=True).to_excel(archivo, index=False)
        else:
            nuevo.to_excel(archivo, index=False)
    except: pass

    st.experimental_set_query_params()  # Limpia la URL
    st.rerun()

# ==================== FOOTER EXACTO COMO TÚ QUIERES ====================
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco © 2025
</div>
""", unsafe_allow_html=True)
