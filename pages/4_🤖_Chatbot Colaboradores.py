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

# CSS + eliminación agresiva
st.markdown("""
<style>
header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"],
.stDeployButton, [data-testid="stStatusWidget"], [data-testid="stDecoration"],
button[title*="Deploy"], button[title*="View"], a[href*="github"], a[href*="streamlit"] {
    display: none !important;
}

.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}

.block-container {
    max-width: 800px !important;
    margin: 0 auto !important;
    padding: 2rem 1rem 130px 1rem !important;
}

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

.footer {
    text-align: center;
    margin-top: 3rem;
    color: #94a3b8;
    font-size: 0.85rem;
    opacity: 0.7;
}

/* Ocultar input y botón nativos */
[data-testid="stChatInput"] {
    display: none !important;
}

/* Input y botón custom en columnas de Streamlit */
.stTextInput > div > div > input {
    border-radius: 26px !important;
    border: 2px solid #334155 !important;
    background: #1e293b !important;
    color: #f1f5f9 !important;
    font-size: 1rem !important;
    padding: 14px 20px !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #64748b !important;
}

.stTextInput > div > div > input:focus {
    border-color: #ea580c !important;
    box-shadow: 0 0 0 3px rgba(234, 88, 12, 0.2), 0 4px 16px rgba(0, 0, 0, 0.3) !important;
    outline: none !important;
}

button[kind="secondary"] {
    background: linear-gradient(135deg, #ea580c, #dc2626) !important;
    border-radius: 50% !important;
    width: 54px !important;
    height: 54px !important;
    border: none !important;
    color: white !important;
    font-size: 22px !important;
    box-shadow: 0 6px 16px rgba(234, 88, 12, 0.45) !important;
}

button[kind="secondary"]:hover {
    background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
    transform: scale(1.05) !important;
}

@media (max-width: 768px) {
    .block-container {padding: 1rem 0.8rem 130px 0.8rem !important;}
    .header {padding: 2rem 1.5rem;}
    .header h1 {font-size: 1.8rem;}
    .user, .bot {max-width: 85%; padding: 11px 16px; font-size: 0.9rem;}
    button[kind="secondary"] {width: 48px !important; height: 48px !important;}
}
</style>
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

# Input custom con columnas
col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input(
        "Mensaje",
        placeholder="Escribe tu consulta aquí...",
        key="user_input",
        label_visibility="collapsed"
    )
with col2:
    send = st.button("➤", key="send")

if send and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
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
                    {"role": "user", "content": user_input},
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
