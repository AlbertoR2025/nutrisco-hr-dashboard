import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# CONFIGURACIÓN
st.set_page_config(
    page_title="Chatbot Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS ESTILO ÚNICO (modifica sólo el botón nativo Streamlit)
st.markdown("""
<style>
header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"],
.stDeployButton, [data-testid="stStatusWidget"], a[href*="github"], a[href*="streamlit"] {
    display:none!important;
}

.stApp {background:#0e1117;}
.block-container {max-width:900px;padding:1rem;padding-bottom:120px;}

.header{
    background:linear-gradient(90deg,#ea580c,#c2410c);
    padding:2.5rem;
    border-radius:20px;
    text-align:center;
    color:white;
    margin-bottom:2rem;
    box-shadow:0 12px 35px rgba(234,88,12,0.45);
}
.header h1 {font-size:2.2rem;font-weight:800;margin:0;}
.header h2 {font-size:1.35rem;font-weight:500;margin:10px 0 0 0;}
.header p  {margin:10px 0 0 0;opacity:0.9;font-size:1.05rem;}

.user{
    background:#262730;
    color:white;
    border-radius:18px;
    padding:14px 20px;
    margin:12px 8% 12px auto;
    max-width:75%;
    box-shadow:0 3px 14px rgba(0,0,0,0.45);
}
.bot{
    background:linear-gradient(135deg,#ea580c,#f97316);
    color:white;
    border-radius:18px;
    padding:14px 20px;
    margin:12px auto 12px 8%;
    max-width:75%;
    box-shadow:0 6px 20px rgba(249,115,22,0.6);
}

/* Input fijo */
.fixed-input {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(15,23,42,0.96);
    padding: 13px 8px 15px 8px;
    box-sizing: border-box;
    z-index: 1000;
    border-top: 1px solid #1f2937;
    backdrop-filter: blur(8px);
    display: flex;
    justify-content: center;
}

.input-container {
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    gap: 10px;
    align-items: center;
    width: 100%;
    padding: 0 8px;
}

.text-input {
    flex: 1;
    padding: 14px 20px;
    border-radius: 999px;
    border: 1px solid #374151;
    background: radial-gradient(circle at top left,#111827,#020617);
    color: #e5e7eb;
    font-size: 1.1rem;
    outline: none;
    transition: all 0.25s ease;
    box-shadow: inset 0 0 0 1px rgba(15,23,42,0.9);
}

.text-input::placeholder {color:#6b7280;}
.text-input:focus {
    border-color: #f97316;
    box-shadow:0 0 0 1px #ea580c,0 0 18px rgba(249,115,22,0.35);
}

button[data-testid="baseButton-secondary"] {
    background: radial-gradient(circle at 30% 30%,#facc15,#ea580c);
    color: white;
    border-radius: 999px;
    width: 60px !important;
    height: 46px !important;
    font-size: 25px !important;
    font-weight: bold;
    box-shadow: 0 6px 22px rgba(234,88,12,0.55);
    border: none;
    padding: 0;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
}

button[data-testid="baseButton-secondary"]:hover {
    background: #c2410c;
    color: #fff;
}

button[data-testid="baseButton-secondary"]:active {
    transform: scale(0.98);
    box-shadow: 0 2px 9px rgba(234,88,12,0.38);
}

@media (max-width: 768px) {
    .header {padding: 2rem;}
    .user, .bot {max-width: 85%;}
    .text-input {padding: 11px 16px;font-size:0.98rem;}
    button[data-testid="baseButton-secondary"] {width: 45px !important;height: 38px !important;font-size:19px !important;}
    .input-container {gap: 7px;}
}
</style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Falta OPENAI_API_KEY.")
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
        "role": "bot",
        "content": (
            "¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\n"
            "Puedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, "
            "vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"
        )
    }]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot">{msg["content"]}</div>', unsafe_allow_html=True)

# ========== INPUT Y UN SOLO BOTÓN =============
st.markdown('<div class="fixed-input"><div class="input-container">', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "Escribe tu consulta aquí...",
        placeholder="Escribe tu consulta aquí...",
        key="chat_input",
        label_visibility="collapsed"
    )
with col2:
    send_clicked = st.button("➤", key="send_button", use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

if send_clicked and user_input.strip():
    texto = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": texto})
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
                            "Eres del equipo RRHH Nutrisco Chile. Hablas español chileno, "
                            "cercano y profesional. Para temas delicados, deriva a Belén Bastías."
                        ),
                    },
                    {"role": "user", "content": texto},
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

    st.session_state.messages.append({"role": "bot", "content": answer})
    st.rerun()

st.markdown(
    '<div class="footer">'
    'Inteligencia Artificial al servicio de las personas – Nutrisco © 2025'
    '</div>',
    unsafe_allow_html=True,
)
