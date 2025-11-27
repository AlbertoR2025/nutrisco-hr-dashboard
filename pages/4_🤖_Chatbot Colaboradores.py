# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN FINAL 2025: SIN AVATAR EN INPUT/CORONA, CENTRADO RESPONSIVO (FIXES #11896/#12132)
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
    layout="centered",
    initial_sidebar_state="collapsed"  # Hamburguesa visible para navegación
)

# ==================== CSS + JS DEFINITIVO 2025 (BORRA AVATAR INPUT Y CORONA - DE RELEASE NOTES) ====================
st.markdown("""
<style>
    /* OCULTAR SOLO LO INNECESARIO (SIN TOCAR HAMBURGUESA) */
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}

    /* OCULTAR CORONA ROJA (DEPLOY BUTTON) Y HOSTED FOOTER (FIX #11896 MÓVIL) */
    button[data-testid="stDeployButton"], .stDeployButton, footer, [data-testid="stStatusWidget"], div[class*="hosted"], div:contains("Streamlit") {display: none !important; visibility: hidden !important; height: 0 !important; z-index: -1 !important; opacity: 0 !important;}

    /* OCULTAR AVATAR EN CHAT_INPUT (CUADRADO CON CARA - FIX #12132 RESIZE MÓVIL) */
    [data-testid="stChatInput"] img, [data-testid="stChatInput"] > div > div > img, [data-testid="stChatInput"] [alt*="avatar"], img[alt*="avatar"] {display: none !important; visibility: hidden !important; width: 0 !important; height: 0 !important; opacity: 0 !important; position: absolute !important;}

    /* OCULTAR AVATARES EN MENSAJES (POR SI ACASO) */
    [data-testid="stChatMessage"] img[src*="avatar"], [data-testid="stAvatar"] {display: none !important; visibility: hidden !important; width: 0 !important; height: 0 !important;}

    /* LAYOUT CENTRADO RESPONSIVO (SIN DESCUADRADO - WIDTH AUTO) */
    .main .block-container {max-width: 800px !important; margin: 0 auto !important; padding: 1rem !important; width: auto !important;}
    @media (max-width: 768px) {
        .main .block-container {width: 95% !important; padding: 0.5rem !important;}
        [data-testid="stChatInput"] {max-width: 100% !important; margin: 0 auto !important; padding-bottom: 0 !important;}
    }
    .stApp {background-color: #0e1117 !important;}

    /* ESTILOS MENSAJES (ALINEADOS SIN HUECOS) */
    [data-testid="stChatMessage"] {padding: 0 !important; gap: 0 !important;}
    .user-message {background: #262730 !important; color: white !important; border-radius: 18px !important; padding: 14px 20px !important; margin: 16px 0 !important; max-width: 80% !important; margin-left: auto !important; box-shadow: 0 2px 10px rgba(0,0,0,0.4) !important;}
    .assistant-message {background: linear-gradient(135deg, #ea580c, #f97316) !important; color: white !important; border-radius: 18px !important; padding: 14px 20px !important; margin: 16px 0 !important; max-width: 80% !important; margin-right: auto !important; box-shadow: 0 4px 15px rgba(249,115,22,0.5) !important;}
    @media (max-width: 768px) {.user-message, .assistant-message {max-width: 95% !important; padding: 12px 16px !important; margin: 12px 0 !important;}}
    .header-box {background: linear-gradient(90deg, #ea580c, #c2410c) !important; padding: 2rem !important; border-radius: 20px !important; text-align: center !important; color: white !important; box-shadow: 0 10px 30px rgba(234,88,12,0.4) !important; margin: 0 auto !important;}
    @media (max-width: 768px) {.header-box {padding: 1.5rem !important;}}
    .belén-box {background: #dc2626 !important; color: white !important; padding: 1.3rem !important; border-radius: 15px !important; text-align: center !important; font-weight: bold !important; margin: 2rem auto !important; font-size: 1.15rem !important; box-shadow: 0 4px 15px rgba(220,38,38,0.4) !important;}
    @media (max-width: 768px) {.belén-box {font-size: 1rem !important; padding: 1rem !important;}}
    .footer {text-align: center !important; margin-top: 4rem !important; color: #64748b !important; font-size: 0.95rem !important; padding: 2rem 0 !important; position: relative !important; z-index: 10 !important;}
    .typing {font-style: italic !important; color: #94a3b8 !important; margin: 15px 0 !important; text-align: left !important;}
    @keyframes blink {0%, 100% {opacity: 1;} 50% {opacity: 0;}}
</style>

<!-- JS DINÁMICO: BORRA AVATAR INPUT Y CORONA CADA 500MS (FIX DINÁMICO MÓVIL 2025) -->
<script>
    setInterval(() => {
        const elements = document.querySelectorAll('[data-testid="stChatInput"] img, button[data-testid="stDeployButton"], footer, [data-testid="stStatusWidget"], img[alt*="avatar"], div:contains("Streamlit"), div:contains("Hosted")');
        elements.forEach(el => { if (el) { el.style.display = 'none'; el.remove(); } });
    }, 500);
</script>
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

# ==================== INICIALIZAR CHAT ====================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "¡Hola! 👋 Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"
    }]

# ==================== MOSTRAR HISTORIAL ====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=None):
        st.markdown(f'<div class="{ "user-message" if msg["role"] == "user" else "assistant-message" }">{msg["content"]}</div>', unsafe_allow_html=True)

# ==================== INPUT Y PROCESAMIENTO ====================
if pregunta := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": pregunta})
    with st.chat_message("user", avatar=None):
        st.markdown(f'<div class="user-message">{pregunta}</div>', unsafe_allow_html=True)

    with st.chat_message("assistant", avatar=None):
        placeholder = st.empty()
        placeholder.markdown('<div class="typing">Escribiendo<span style="animation: blink 1s infinite;">...</span></div>', unsafe_allow_html=True)
        time.sleep(1.3)
        placeholder.empty()

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

        st.markdown(f'<div class="assistant-message">{respuesta}</div>', unsafe_allow_html=True)
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

    st.rerun()

# ==================== FOOTER EXACTO COMO TÚ QUIERES ====================
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco © 2025
</div>
""", unsafe_allow_html=True)
