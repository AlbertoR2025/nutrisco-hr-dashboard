# ===============================
# pages/4_🤖_Chatbot Colaboradores.py
# Versión estable 2025 — SIN FOTO, SIN CORONA, INPUT FUNCIONANDO
# ===============================

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------
# CONFIGURACIÓN GLOBAL
# ---------------------------------------------------
st.set_page_config(
    page_title="Chatbot Colaboradores – Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# CSS — ESTILOS Y OCULTACIÓN (versión segura)
# ---------------------------------------------------

css_code = """
<style>

    /* Fondo */
    .stApp { background-color: #0e1117 !important; }

    /* MANTENER INPUT VISIBLE */
    [data-testid="stChatInput"] {
        display: flex !important;
        opacity: 1 !important;
    }

    /* OCULTAR SOLO EL AVATAR, NO EL CONTENEDOR */
    [data-testid="stChatInput"] img,
    [data-testid="stChatInput"] svg,
    [data-testid="stChatMessage"] img,
    [data-testid="stChatMessage"] svg {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
    }

    /* OCULTAR CORONA / DEPLOY BUTTON */
    [data-testid="stDeployButton"],
    .stDeployButton,
    .stAppDeployButton,
    button[title="Manage app"],
    [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }

    /* CAJA DEL INPUT */
    [data-testid="stChatInput"] textarea {
        color: white !important;
        border-radius: 12px !important;
        background: #1f1f23 !important;
        border: 1px solid #333 !important;
        padding: 12px !important;
    }

    /* Estilos mensajes */

    .user-message {
        background: #262730 !important;
        color: white !important;
        border-radius: 18px;
        padding: 14px 20px;
        margin: 16px 8% 16px auto;
        max-width: 75%;
        box-shadow: 0 2px 10px rgba(0,0,0,0.4);
    }

    .assistant-message {
        background: linear-gradient(135deg, #ea580c, #f97316);
        color: white !important;
        border-radius: 18px;
        padding: 14px 20px;
        margin: 16px auto 16px 8%;
        max-width: 75%;
        box-shadow: 0 4px 15px rgba(249,115,22,0.5);
    }

    /* Header */
    .header-box {
        background: linear-gradient(90deg, #ea580c, #c2410c);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(234,88,12,0.4);
        margin-bottom: 15px;
    }

</style>
"""

st.markdown(css_code, unsafe_allow_html=True)

# ---------------------------------------------------
# JAVASCRIPT — ELIMINACIÓN DINÁMICA DEL AVATAR Y CORONA
# ---------------------------------------------------

js_code = """
<script>
function hideElements() {
    // Avatar input
    document.querySelectorAll('[data-testid="stChatInput"] img, [data-testid="stChatInput"] svg')
        .forEach(el => el.remove());

    // Avatar mensajes
    document.querySelectorAll('[data-testid="stChatMessage"] img, [data-testid="stChatMessage"] svg')
        .forEach(el => el.remove());

    // Corona / deploy
    document.querySelectorAll(
        '[data-testid="stDeployButton"], .stDeployButton, .stAppDeployButton, button[title="Manage app"]'
    ).forEach(el => {
        el.style.display = "none";
        el.style.visibility = "hidden";
        el.remove();
    });
}

// Observer para DOM dinámico de Streamlit
const observer = new MutationObserver(hideElements);
observer.observe(document.body, { subtree: true, childList: true });

// Correr una vez también
setTimeout(hideElements, 500);
</script>
"""

st.markdown(js_code, unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("""
<div class="header-box">
    <h1>Chatbot Colaboradores</h1>
    <p>Nutrisco – Atención Personas</p>
    <p>Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# MENSAJE INICIAL
# ---------------------------------------------------

st.markdown("""
<div class="assistant-message">
    ¡Hola! 🤝 Soy parte del equipo de <strong>Atención a Personas</strong> de Nutrisco.<br><br>
    Puedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos,
    vestimenta, bono Fisherman, etc.<br><br>
    ¡Estoy aquí para ayudarte!
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------

user_input = st.chat_input("Escribe tu consulta aquí...")

if user_input:
    st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)

    # Respuesta temporal (luego conectamos tu agente real)
    st.markdown("""
    <div class="assistant-message">
        Déjame revisar eso... ⏳
    </div>
    """, unsafe_allow_html=True)
