# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN FINAL 2025: MODERNO, FUNCIONAL Y RESPONSIIVO
import streamlit as st
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Chatbot Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== CSS MODERNO Y LIMPIO + OCULTAR CORONA Y AVATAR ==========
st.markdown("""
<style>
/* Ocultar elementos Streamlit agresivamente */
header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"],
.stDeployButton, [data-testid="stStatusWidget"], [data-testid="stDecoration"] {
    display: none !important;
}

/* Fondo limpio */
.stApp {background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);}
.block-container {max-width: 800px !important; margin: 0 auto !important; padding: 2rem 1rem 100px 1rem !important;}

/* Header moderno y centrado */
.header {
    background: linear-gradient(135deg, #ea580c 0%, #dc2626 100%);
    padding: 2.8rem 2rem;
    border-radius: 24px;
    text-align: center;
    color: white;
    margin-bottom: 2.5rem;
    box-shadow: 0 20px 50px rgba(234, 88, 12, 0.35);
}
.header h1 {font-size: 2.2rem; font-weight: 700; margin: 0;}
.header h2 {font-size: 1.25rem; font-weight: 400; margin: 0.8rem 0 0 0; opacity: 0.95;}
.header p {margin: 0.8rem 0 0 0; opacity: 0.9; font-size: 1rem;}

/* Burbujas estilo WhatsApp/iOS modernas */
.user {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 18px;
    margin: 10px 0 10px auto;
    max-width: 70%;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
    font-size: 0.95rem;
    line-height: 1.5;
}

.bot {
    background: linear-gradient(135deg, #ea580c, #f97316);
    color: white;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 18px;
    margin: 10px auto 10px 0;
    max-width: 70%;
    box-shadow: 0 2px 8px rgba(234, 88, 12, 0.3);
    font-size: 0.95rem;
    line-height: 1.5;
}

.footer {text-align: center; margin-top: 3rem; color: #94a3b8; font-size: 0.85rem; opacity: 0.7;}

/* Responsive móvil */
@media (max-width: 768px) {
    .block-container {padding: 1rem 0.8rem 100px 0.8rem !important;}
    .header {padding: 2rem 1.5rem;}
    .header h1 {font-size: 1.8rem;}
    .user, .bot {max-width: 85%; padding: 11px 16px; font-size: 0.9rem;}
}

/* OCULTAR CORONA ROJA Y AVATAR EN EL INPUT */
[data-testid="stChatInput"] > div > div > div > img,
[data-testid="stChatInput"] > div > div > div > svg,
[data-testid="stChatInput"] > div > div > div > [alt*="avatar"],
[data-testid="stChatInput"] > div > div > div > [data-testid="stAvatar"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
}

/* OCULTAR AVATARES EN MENSAJES DEL CHAT */
[data-testid="stChatMessage"] > div > img,
[data-testid="stChatMessage"] > div > svg,
[data-testid="stChatMessage"] > div > [data-testid="stAvatar"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
}

/* OCULTAR CONTENEDOR DEL AVATAR EN INPUT */
[data-testid="stChatInput"] > div > div > div {
    display: none !important;
}

/* OCULTAR CONTENEDOR DEL AVATAR EN MENSAJES */
[data-testid="stChatMessage"] > div {
    display: none !important;
}
</style>

<script>
// Ocultar corona y avatar específicos
function hideCrownAndAvatar() {
    // Oculta la corona roja
    const crown = document.querySelector('.stAppDeployButton') || 
                 document.querySelector('[data-testid="stDeployButton"]') || 
                 document.querySelector('.stDeployButton');
    if (crown) {
        crown.style.display = 'none';
        crown.style.visibility = 'hidden';
    }

    // Oculta avatar en input
    const avatarInInput = document.querySelector('[data-testid="stChatInput"] > div > div > div > img') ||
                         document.querySelector('[data-testid="stChatInput"] > div > div > div > svg') ||
                         document.querySelector('[data-testid="stChatInput"] > div > div > div > [alt*="avatar"]');
    if (avatarInInput) {
        avatarInInput.style.display = 'none';
        avatarInInput.style.visibility = 'hidden';
    }

    // Oculta avatares en mensajes
    const messageAvatars = document.querySelectorAll('[data-testid="stChatMessage"] > div > img, [data-testid="stChatMessage"] > div > svg, [data-testid="stChatMessage"] > div > [data-testid="stAvatar"]');
    messageAvatars.forEach(el => {
        el.style.display = 'none';
        el.style.visibility = 'hidden';
    });
}

// Ejecutar al cargar
document.addEventListener('DOMContentLoaded', function() {
    hideCrownAndAvatar();
});

// Reintentar cada segundo durante 10 segundos
let attempts = 0;
setInterval(function() {
    hideCrownAndAvatar();
    attempts++;
    if (attempts > 10) clearInterval(this);
}, 1000);
</script>
""", unsafe_allow_html=True)

# ========== LÓGICA DEL CHATBOT ==========
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("⚠️ Falta configurar OPENAI_API_KEY")
    st.stop()

st.markdown("""
<div class="header">
    <h1>Chatbot Colaboradores</h1>
    <h2>Nutrisco – Atención Personas</h2>
    <p>Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme sobre: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman y más.\n\n¡Estoy aquí para ayudarte!"
    }]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot">{msg["content"]}</div>', unsafe_allow_html=True)

# Input con Enter automático
if prompt := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions  ",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 600,
                "messages": [
                    {"role": "system", "content": "Eres del equipo RRHH de Nutrisco Chile. Hablas español chileno, cercano y profesional. Para temas sensibles deriva a Belén Bastías."},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=30,
        )
        answer = resp.json()["choices"][0]["message"]["content"]
    except Exception:
        answer = "⚠️ Problema de conexión. Contacta a Belén Bastías: belen.bastias@nutrisco.com"
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

st.markdown('<div class="footer">Inteligencia Artificial al servicio de las personas – Nutrisco © 2025</div>', unsafe_allow_html=True)
