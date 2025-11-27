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
/* === ELIMINAR STREAMLIT === */
header, footer,
[data-testid="stToolbar"],
[data-testid="stDeployButton"],
.stDeployButton,
[data-testid="stStatusWidget"],
[data-testid="stDecoration"],
button[title*="Deploy"],
button[title*="View"],
a[href*="github"],
a[href*="streamlit"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* === FONDO === */
.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}

.block-container {
    max-width: 800px !important;
    margin: 0 auto !important;
    padding: 2rem 1rem 120px 1rem !important;
}

/* === HEADER === */
.header {
    background: linear-gradient(135deg, #ea580c 0%, #dc2626 100%);
    padding: 2.8rem 2rem;
    border-radius: 24px;
    text-align: center;
    color: white;
    margin-bottom: 2.5rem;
    box-shadow: 0 20px 50px rgba(234, 88, 12, 0.35);
}

.header h1 {
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0;
}

.header h2 {
    font-size: 1.25rem;
    font-weight: 400;
    margin: 0.8rem 0 0 0;
    opacity: 0.95;
}

.header p {
    margin: 0.8rem 0 0 0;
    opacity: 0.9;
    font-size: 1rem;
}

/* === BURBUJAS MODERNAS === */
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

.footer {
    text-align: center;
    margin-top: 3rem;
    color: #94a3b8;
    font-size: 0.85rem;
    opacity: 0.7;
}

/* === CHAT INPUT (z-index máximo para que quede siempre visible) === */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    background: rgba(15, 23, 42, 0.98) !important;
    padding: 14px 12px 20px 12px !important;
    border-top: 1px solid rgba(71, 85, 105, 0.4) !important;
    backdrop-filter: blur(14px) !important;
    z-index: 2147483647 !important;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.25) !important;
}

[data-testid="stChatInput"] > div {
    max-width: 800px !important;
    margin: 0 auto !important;
    display: flex !important;
    gap: 10px !important;
    align-items: center !important;
    position: relative !important;
}

/* Input texto */
[data-testid="stChatInput"] textarea {
    border-radius: 26px !important;
    border: 2px solid #334155 !important;
    background: #1e293b !important;
    color: #f1f5f9 !important;
    font-size: 1rem !important;
    padding: 14px 60px 14px 20px !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
    resize: none !important;
    transition: all 0.2s ease !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #ea580c !important;
    box-shadow:
        0 0 0 3px rgba(234, 88, 12, 0.2),
        0 4px 16px rgba(0, 0, 0, 0.3) !important;
    outline: none !important;
}

/* Botón de envío (z-index altísimo para que siempre esté encima) */
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #ea580c, #dc2626) !important;
    border-radius: 50% !important;
    width: 50px !important;
    height: 50px !important;
    min-width: 50px !important;
    min-height: 50px !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    box-shadow: 0 6px 16px rgba(234, 88, 12, 0.45) !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    position: absolute !important;
    right: 8px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    z-index: 2147483647 !important;
    cursor: pointer !important;
}

[data-testid="stChatInput"] button svg {
    width: 20px !important;
    height: 20px !important;
    color: white !important;
}

[data-testid="stChatInput"] button:hover {
    background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
    transform: translateY(-50%) scale(1.08) !important;
    box-shadow: 0 8px 20px rgba(234, 88, 12, 0.55) !important;
}

[data-testid="stChatInput"] button:active {
    transform: translateY(-50%) scale(0.96) !important;
}

/* === RESPONSIVE === */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 0.8rem 130px 0.8rem !important;
    }
    
    .header {
        padding: 2rem 1.5rem;
    }
    
    .header h1 {
        font-size: 1.8rem;
    }
    
    .user, .bot {
        max-width: 85%;
        padding: 11px 16px;
        font-size: 0.9rem;
    }
    
    [data-testid="stChatInput"] textarea {
        font-size: 0.92rem !important;
        padding: 12px 56px 12px 18px !important;
    }
    
    [data-testid="stChatInput"] button {
        width: 44px !important;
        height: 44px !important;
        min-width: 44px !important;
        min-height: 44px !important;
        right: 6px !important;
    }
}
</style>

<script>
// Eliminar corona/foto/elementos streamlit agresivamente
(function() {
    function kill() {
        const badSelectors = [
            'header', 'footer',
            '[data-testid="stToolbar"]',
            '[data-testid="stDeployButton"]',
            '.stDeployButton',
            '[data-testid="stStatusWidget"]',
            '[data-testid="stDecoration"]',
            'button[title*="Deploy"]',
            'button[title*="View"]',
            'a[href*="github"]',
            'a[href*="streamlit"]'
        ];
        badSelectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => el.remove());
        });
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', kill);
    } else {
        kill();
    }
    
    setInterval(kill, 500);
})();
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
        "content": (
            "¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\n"
            "Puedes preguntarme sobre: licencias, beneficios, BUK, finiquitos, "
            "vestimenta, bono Fisherman y más.\n\n¡Estoy aquí para ayudarte!"
        )
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
                    {
                        "role": "system",
                        "content": (
                            "Eres del equipo RRHH de Nutrisco Chile. Hablas español chileno, "
                            "cercano y profesional. Para temas sensibles deriva a Belén Bastías."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=30,
        )
        answer = resp.json()["choices"][0]["message"]["content"]
    except Exception:
        answer = (
            "⚠️ Problema de conexión. Contacta a Belén Bastías: "
            "belen.bastias@nutrisco.com"
        )
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

st.markdown(
    '<div class="footer">'
    'Inteligencia Artificial al servicio de las personas – Nutrisco © 2025'
    '</div>',
    unsafe_allow_html=True,
)
