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

# ========== CSS + JS PARA OCULTAR FOTO/CORONA Y MEJORAR UI ==========
st.markdown("""
<style>
/* Ocultar elementos Streamlit */
header, footer,
[data-testid="stToolbar"],
[data-testid="stDeployButton"],
.stDeployButton,
[data-testid="stStatusWidget"],
a[href*="github"],
a[href*="streamlit"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] > div,
button[title*="View app source"],
button[title*="Deploy"] {
    display: none !important;
    visibility: hidden !important;
}

/* Fondo */
.stApp {background:#0e1117;}
.block-container {
    max-width:900px;
    padding:1rem 1rem 130px 1rem;
}

/* Header */
.header {
    background:linear-gradient(90deg,#ea580c,#c2410c);
    padding:2.5rem;
    border-radius:22px;
    text-align:center;
    color:white;
    margin-bottom:2rem;
    box-shadow:0 14px 40px rgba(234,88,12,0.5);
}
.header h1 {font-size:2.3rem;font-weight:800;margin:0;letter-spacing:-0.5px;}
.header h2 {font-size:1.4rem;font-weight:500;margin:12px 0 0 0;}
.header p {margin:12px 0 0 0;opacity:0.92;font-size:1.08rem;}

/* Burbujas */
.user {
    background:#262730;
    color:white;
    border-radius:20px;
    padding:15px 22px;
    margin:14px 8% 14px auto;
    max-width:75%;
    box-shadow:0 4px 16px rgba(0,0,0,0.5);
}
.bot {
    background:linear-gradient(135deg,#ea580c,#f97316);
    color:white;
    border-radius:20px;
    padding:15px 22px;
    margin:14px auto 14px 8%;
    max-width:75%;
    box-shadow:0 6px 22px rgba(249,115,22,0.65);
}

/* Footer */
.footer {
    text-align:center;
    margin-top:4rem;
    color:#64748b;
    font-size:0.95rem;
}

/* ==== INPUT FIJO MEJORADO ==== */
.fixed-input {
    position:fixed;
    bottom:0;
    left:0;
    width:100%;
    background:rgba(15,23,42,0.98);
    padding:12px 8px 16px 8px;
    box-sizing:border-box;
    z-index:10000;
    border-top:1px solid #1f2937;
    backdrop-filter:blur(10px);
    display:flex;
    justify-content:center;
}
.input-container {
    max-width:900px;
    margin:0 auto;
    display:flex;
    gap:12px;
    align-items:center;
    width:100%;
    padding:0 8px;
}

/* Barra de texto (input) */
input[type="text"] {
    flex:1;
    padding:16px 22px !important;
    border-radius:30px !important;
    border:1.5px solid #374151 !important;
    background:radial-gradient(circle at top left,#1a202c,#0f172a) !important;
    color:#e5e7eb !important;
    font-size:1.1rem !important;
    outline:none !important;
    transition:all 0.3s ease !important;
    box-shadow:inset 0 2px 6px rgba(0,0,0,0.3) !important;
}
input[type="text"]::placeholder {
    color:#6b7280 !important;
}
input[type="text"]:focus {
    border-color:#f97316 !important;
    box-shadow:
        0 0 0 2px rgba(249,115,22,0.5),
        0 0 22px rgba(249,115,22,0.4),
        inset 0 2px 6px rgba(0,0,0,0.3) !important;
}

/* Botón de envío */
button[data-testid="baseButton-secondary"] {
    background:radial-gradient(circle at 35% 35%,#fbbf24,#ea580c,#c2410c) !important;
    color:white !important;
    border-radius:50% !important;
    width:62px !important;
    height:62px !important;
    min-width:62px !important;
    font-size:26px !important;
    font-weight:bold !important;
    box-shadow:0 8px 24px rgba(234,88,12,0.6) !important;
    border:none !important;
    padding:0 !important;
    margin:0 !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    transition:all 0.25s ease !important;
    cursor:pointer !important;
}
button[data-testid="baseButton-secondary"]:hover {
    background:radial-gradient(circle at 35% 35%,#fcd34d,#f97316,#b91c1c) !important;
    transform:translateY(-2px) scale(1.05) !important;
    box-shadow:0 12px 32px rgba(234,88,12,0.75) !important;
}
button[data-testid="baseButton-secondary"]:active {
    transform:translateY(1px) scale(0.97) !important;
    box-shadow:0 4px 14px rgba(234,88,12,0.5) !important;
}

/* Responsive móvil */
@media (max-width: 768px) {
    .header {padding:2rem;}
    .header h1 {font-size:1.9rem;}
    .header h2 {font-size:1.2rem;}
    .user, .bot {max-width:88%;padding:13px 18px;}
    input[type="text"] {
        padding:13px 18px !important;
        font-size:1.02rem !important;
    }
    button[data-testid="baseButton-secondary"] {
        width:54px !important;
        height:54px !important;
        min-width:54px !important;
        font-size:22px !important;
    }
    .input-container {gap:10px;}
}
</style>

<script>
// Ocultar avatares y elementos Streamlit persistentemente
function ocultarElementos() {
    document.querySelectorAll(
        'header, footer, [data-testid="stToolbar"], ' +
        '[data-testid="stDeployButton"], .stDeployButton, ' +
        '[data-testid="stDecoration"], [data-testid="stStatusWidget"], ' +
        'button[title*="Deploy"], button[title*="View"], ' +
        'a[href*="github"], a[href*="streamlit"]'
    ).forEach(el => {
        el.style.display = 'none';
        el.style.visibility = 'hidden';
    });
}
document.addEventListener('DOMContentLoaded', ocultarElementos);
setTimeout(ocultarElementos, 500);
setTimeout(ocultarElementos, 1500);
setInterval(ocultarElementos, 3000);
</script>
""", unsafe_allow_html=True)

# ========== LÓGICA CHATBOT ==========
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("⚠️ Falta OPENAI_API_KEY en el entorno.")
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

# ========== INPUT FIJO ==========
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
