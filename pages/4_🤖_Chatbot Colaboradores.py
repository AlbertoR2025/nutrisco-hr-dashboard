# ===============================
# pages/4_🤖_Chatbot Colaboradores.py
# Versión final 2025 — Sin avatar, sin corona, full responsive
# ===============================

import streamlit as st
import os
import time
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIGURACIÓN GLOBAL ====================
st.set_page_config(
    page_title="Chatbot Colaboradores – Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CSS + JS — ELIMINA AVATAR Y CORONA ====================

css_code = """
<style>

    /* Fondo general */
    .stApp { background-color: #0e1117 !important; }

    /* Ocultar avatar del input del chat */
    [data-testid="stChatInput"] img,
    [data-testid="stChatInput"] svg {
        display: none !important;
        visibility: hidden !important;
    }

    /* Ocultar contenedor lateral del avatar del input */
    [data-testid="stChatInput"] div:first-child {
        display: none !important;
    }

    /* Ocultar avatares en los mensajes */
    [data-testid="stChatMessage"] img,
    [data-testid="stChatMessage"] svg {
        display: none !important;
        visibility: hidden !important;
    }

    /* Ocultar la corona roja (Deploy Button) */
    [data-testid="stDeployButton"],
    .stAppDeployButton,
    .stDeployButton,
    button[title="Manage app"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Ocultar toolbar, footer, logos externos */
    [data-testid="stToolbar"],
    footer,
    .stStatusWidget,
    .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    /* Mantener simetría del chat */
    [data-testid="stChatMessage"] { padding: 0 !important; gap: 0 !important; }

    /* Mensaje del usuario */
    .user-message {
        background: #262730 !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 14px 20px !important;
        margin: 16px 8% 16px auto !important;
        max-width: 75% !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.4) !important;
    }

    /* Mensaje del asistente */
    .assistant-message {
        background: linear-gradient(135deg, #ea580c, #f97316) !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 14px 20px !important;
        margin: 16px auto 16px 8% !important;
        max-width: 75% !important;
        box-shadow: 0 4px 15px rgba(249,115,22,0.5) !important;
    }

    /* Header Box */
    .header-box {
        background: linear-gradient(90deg, #ea580c, #c2410c) !important;
        padding: 2rem !important;
        border-radius: 20px !important;
        text-align: center !important;
        color: white !important;
        box-shadow: 0 10px 30px rgba(234,88,12,0.4) !important;
        margin-bottom: 15px !important;
        margin-top: 10px !important;
    }

    /* Responsivo móvil */
    @media (max-width: 768px) {
        .header-box { padding: 1.5rem !important; }
        .user-message, .assistant-message {
            max-width: 90% !important;
            margin-left: 4% !important;
            margin-right: 4% !important;
            padding: 12px 16px !important;
        }
    }

</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

js_code = """
<script>
document.addEventListener("DOMContentLoaded", function() {

    // Ocultar avatar del input (Streamlit móvil/desktop variación)
    const removeInputAvatar = setInterval(() => {
        const avatar = document.querySelector('[data-testid="stChatInput"] img');
        if (avatar) { avatar.remove(); clearInterval(removeInputAvatar); }
    }, 200);

    // Ocultar contenedor del avatar del input
    const removeContainer = setInterval(() => {
        const avatarDiv = document.querySelector('[data-testid="stChatInput"] div div div');
        if (avatarDiv) { avatarDiv.style.display = "none"; clearInterval(removeContainer); }
    }, 200);

    // Ocultar avatares dinámicos dentro del chat
    const observer = new MutationObserver(() => {
        document.querySelectorAll('[data-testid="stChatMessage"] img, [data-testid="stChatMessage"] svg')
        .forEach(el => { el.style.display = "none"; el.style.visibility = "hidden"; });
    });

    observer.observe(document.body, { childList: true, subtree: true });

    // Ocultar la corona / deploy button
    const crownSelectors = [
        '[data-testid="stDeployButton"]',
        '.stAppDeployButton',
        '.stDeployButton',
        'button[title="Manage app"]'
    ];
    crownSelectors.forEach(sel => {
        const el = document.querySelector(sel);
        if (el) { el.style.display = "none"; el.style.visibility = "hidden"; }
    });

});
</script>
"""
st.markdown(js_code, unsafe_allow_html=True)

# ==================== HEADER DEL CHAT ====================

st.markdown("""
<div class="header-box">
    <h1>Chatbot Colaboradores</h1>
    <p>Nutrisco – Atención Personas</p>
    <p>Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

# ==================== MENSAJE INICIAL ====================

st.markdown("""
<div class="assistant-message">
    ¡Hola! 🤝 Soy parte del equipo de <strong>Atención a Personas</strong> de Nutrisco.<br><br>
    Puedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta,
    bono Fisherman, etc.<br><br>
    ¡Estoy aquí para ayudarte!
</div>
""", unsafe_allow_html=True)

# ==================== INPUT DEL CHAT ====================

user_input = st.chat_input("Escribe tu consulta aquí...")

if user_input:
    # Mensaje del usuario
    st.markdown(
        f'<div class="user-message">{user_input}</div>',
        unsafe_allow_html=True
    )

    # Mensaje temporal del asistente
    st.markdown("""
    <div class="assistant-message">
        Gracias por tu pregunta. Estoy procesando la respuesta...
    </div>
    """, unsafe_allow_html=True)

    # Aquí conectas tu agente real en otro paso
    # respuesta = agente(user_input)
    # st.markdown(f'<div class="assistant-message">{respuesta}</div>', unsafe_allow_html=True)
