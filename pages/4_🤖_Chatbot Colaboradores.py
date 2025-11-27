import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Chatbot Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
/* === ELIMINAR TODOS LOS ELEMENTOS STREAMLIT NO DESEADOS === */
header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"],
.stDeployButton, [data-testid="stStatusWidget"], [data-testid="stDecoration"],
button[title*="Deploy"], button[title*="View"], a[href*="github"], a[href*="streamlit"] {
    display: none !important;
}

/* === ELIMINAR COMPLETAMENTE FOTOS/AVATARES DEL CHAT === */
[data-testid="stChatMessageAvatar"],
[data-testid="stChatMessage"] [data-testid="stAvatar"],
[data-testid="stChatMessage"] img,
[data-testid="stChatMessage"] svg,
.stChatMessage img,
.stChatMessage svg {
    display: none !important;
    visibility: hidden !important;
    width: 0px !important;
    height: 0px !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* === ELIMINAR EL CONTENEDOR DE AVATARES === */
[data-testid="stChatMessage"] > div > div:first-child {
    display: none !important;
    width: 0px !important;
    min-width: 0px !important;
}

/* === ELIMINAR EL ESPACIO DE AVATARES === */
[data-testid="stChatMessage"] > div {
    gap: 0px !important;
    margin-left: 0px !important;
    margin-right: 0px !important;
    padding-left: 0px !important;
}

/* === ESTILOS EXISTENTES MEJORADOS === */
.stApp {background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);}
.block-container {max-width: 800px !important; margin: 0 auto !important; padding: 2rem 1rem 100px 1rem !important;}

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

/* === MEJORAS PARA EL INPUT EN MÓVIL === */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    background: rgba(15, 23, 42, 0.95) !important;
    backdrop-filter: blur(10px) !important;
    padding: 16px 12px 20px 12px !important;
    border-top: 1px solid rgba(71, 85, 105, 0.4) !important;
    z-index: 10000 !important;
}

[data-testid="stChatInput"] > div {
    max-width: 800px !important;
    margin: 0 auto !important;
}

@media (max-width: 768px) {
    .block-container {padding: 1rem 0.8rem 120px 0.8rem !important;}
    .header {padding: 2rem 1.5rem;}
    .header h1 {font-size: 1.8rem;}
    .user, .bot {max-width: 85%; padding: 11px 16px; font-size: 0.9rem;}
    
    [data-testid="stChatInput"] {
        padding: 14px 10px 18px 10px !important;
    }
}
</style>

<!-- JAVASCRIPT PARA ELIMINACIÓN PERSISTENTE -->
<script>
function eliminarElementosPersistentes() {
    // Eliminar avatares del chat
    const avatares = document.querySelectorAll([
        '[data-testid="stChatMessageAvatar"]',
        '[data-testid="stChatMessage"] [data-testid="stAvatar"]',
        '[data-testid="stChatMessage"] img',
        '[data-testid="stChatMessage"] svg',
        '.stChatMessage img',
        '.stChatMessage svg'
    ].join(','));
    
    avatares.forEach(avatar => {
        avatar.remove();
        avatar.style.display = 'none';
    });
    
    // Eliminar contenedores de avatar
    document.querySelectorAll('[data-testid="stChatMessage"] > div > div:first-child').forEach(contenedor => {
        contenedor.remove();
        contenedor.style.display = 'none';
    });
    
    // Eliminar elementos de Streamlit (corona, etc.)
    const elementosStreamlit = document.querySelectorAll([
        'header', 'footer',
        '[data-testid="stToolbar"]',
        '[data-testid="stDeployButton"]',
        '[data-testid="stStatusWidget"]',
        'button[title*="Deploy"]',
        'button[title*="View"]'
    ].join(','));
    
    elementosStreamlit.forEach(elemento => {
        elemento.remove();
        elemento.style.display = 'none';
    });
}

// Ejecutar inmediatamente y de forma persistente
document.addEventListener('DOMContentLoaded', eliminarElementosPersistentes);
setTimeout(eliminarElementosPersistentes, 100);
setTimeout(eliminarElementosPersistentes, 500);
setTimeout(eliminarElementosPersistentes, 1000);

// Ejecutar cada 2 segundos para elementos que puedan reaparecer
setInterval(eliminarElementosPersistentes, 2000);
</script>
""", unsafe_allow_html=True)

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

if prompt := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
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
