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

# ========== CSS MODERNO Y LIMPIO ==========
st.markdown("""
<style>
/* Ocultar elementos Streamlit agresivamente */
header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"],
.stDeployButton, [data-testid="stStatusWidget"], [data-testid="stDecoration"],
button[title*="Deploy"], button[title*="View"], a[href*="github"], a[href*="streamlit"] {
    display: none !important;
    visibility: hidden !important;
    position: absolute !important;
    left: -9999px !important;
}

/* Fondo limpio */
.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}

.block-container {
    max-width: 800px !important;
    margin: 0 auto !important;
    padding: 2rem 1rem 110px 1rem !important;
}

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

.header h1 {
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.02em;
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
    word-wrap: break-word;
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
    word-wrap: break-word;
}

.footer {
    text-align: center;
    margin-top: 3rem;
    color: #94a3b8;
    font-size: 0.85rem;
    opacity: 0.7;
}

/* Chat input fijo y limpio */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    background: rgba(15, 23, 42, 0.95) !important;
    padding: 12px !important;
    border-top: 1px solid rgba(71, 85, 105, 0.3) !important;
    backdrop-filter: blur(12px) !important;
    z-index: 999999 !important;
}

[data-testid="stChatInput"] > div {
    max-width: 800px !important;
    margin: 0 auto !important;
    display: flex !important;
    gap: 10px !important;
    align-items: center !important;
}

/* Input de texto moderno */
[data-testid="stChatInput"] textarea {
    border-radius: 24px !important;
    border: 1.5px solid #334155 !important;
    background: #1e293b !important;
    color: #f1f5f9 !important;
    font-size: 0.95rem !important;
    padding: 12px 60px 12px 18px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    resize: none !important;
    transition: all 0.2s ease !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #ea580c !important;
    box-shadow: 0 0 0 3px rgba(234, 88, 12, 0.15), 0 4px 12px rgba(0, 0, 0, 0.25) !important;
    outline: none !important;
}

/* Botón de envío moderno y visible */
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #ea580c, #dc2626) !important;
    border-radius: 50% !important;
    width: 48px !important;
    height: 48px !important;
    min-width: 48px !important;
    min-height: 48px !important;
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(234, 88, 12, 0.4) !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    position: absolute !important;
    right: 6px !important;
    bottom: 6px !important;
    z-index: 10 !important;
}

[data-testid="stChatInput"] button svg {
    width: 20px !important;
    height: 20px !important;
    color: white !important;
}

[data-testid="stChatInput"] button:hover {
    background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
    transform: scale(1.05) !important;
    box-shadow: 0 6px 16px rgba(234, 88, 12, 0.5) !important;
}

[data-testid="stChatInput"] button:active {
    transform: scale(0.95) !important;
}

/* Responsive móvil */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 0.8rem 110px 0.8rem !important;
    }
    
    .header {
        padding: 2rem 1.5rem;
        border-radius: 20px;
    }
    
    .header h1 {
        font-size: 1.8rem;
    }
    
    .header h2 {
        font-size: 1.1rem;
    }
    
    .user, .bot {
        max-width: 85%;
        padding: 11px 16px;
        font-size: 0.9rem;
    }
    
    [data-testid="stChatInput"] textarea {
        font-size: 0.9rem !important;
        padding: 11px 55px 11px 16px !important;
    }
    
    [data-testid="stChatInput"] button {
        width: 42px !important;
        height: 42px !important;
        min-width: 42px !important;
        min-height: 42px !important;
    }
}
</style>

<script>
// Eliminar elementos Streamlit persistentemente
(function() {
    function removeStreamlitElements() {
        const selectors = [
            'header', 'footer', '[data-testid="stToolbar"]',
            '[data-testid="stDeployButton"]', '.stDeployButton',
            '[data-testid="stStatusWidget"]', '[data-testid="stDecoration"]',
            'button[title*="Deploy"]', 'button[title*="View"]',
            'a[href*="github"]', 'a[href*="streamlit"]'
        ];
        selectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => {
                el.remove();
            });
        });
    }
    
    document.addEventListener('DOMContentLoaded', removeStreamlitElements);
    setInterval(removeStreamlitElements, 1000);
})();
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

# Input con Enter automático
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
