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

# ==================== CSS NUCLEAR - ELIMINACIÓN COMPLETA ====================
st.markdown("""
<style>
/* === ELIMINACIÓN TOTAL DE ELEMENTOS STREAMLIT === */
header, footer,
[data-testid="stToolbar"],
[data-testid="stDeployButton"],
.stDeployButton,
[data-testid="stStatusWidget"],
[data-testid="stDecoration"],
button[title*="Deploy"],
button[title*="View"],
a[href*="github"],
a[href*="streamlit"],
[data-testid="stChatMessageAvatar"],
[data-testid="stAvatar"],
.stChatMessage img,
.stChatMessage svg,
[data-testid="stChatMessage"] img,
[data-testid="stChatMessage"] svg {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    width: 0px !important;
    height: 0px !important;
    min-width: 0px !important;
    min-height: 0px !important;
}

/* === FONDO === */
.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    min-height: 100vh;
}

.block-container {
    max-width: 800px !important;
    margin: 0 auto !important;
    padding: 2rem 1rem 140px 1rem !important;
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
    position: relative;
    z-index: 1;
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

/* === INPUT PERSONALIZADO - NO USAR st.chat_input === */
.custom-input-container {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    background: rgba(15, 23, 42, 0.98) !important;
    padding: 16px 12px 24px 12px !important;
    border-top: 1px solid rgba(71, 85, 105, 0.4) !important;
    backdrop-filter: blur(20px) !important;
    z-index: 2147483647 !important;
    box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.4) !important;
}

.custom-input-wrapper {
    max-width: 800px !important;
    margin: 0 auto !important;
    display: flex !important;
    gap: 12px !important;
    align-items: center !important;
    position: relative !important;
}

.custom-text-input {
    flex: 1 !important;
    border-radius: 26px !important;
    border: 2px solid #334155 !important;
    background: #1e293b !important;
    color: #f1f5f9 !important;
    font-size: 1rem !important;
    padding: 16px 70px 16px 20px !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
    resize: none !important;
    transition: all 0.2s ease !important;
    outline: none !important;
    font-family: inherit !important;
}

.custom-text-input::placeholder {
    color: #64748b !important;
}

.custom-text-input:focus {
    border-color: #ea580c !important;
    box-shadow: 0 0 0 3px rgba(234, 88, 12, 0.2), 0 4px 16px rgba(0, 0, 0, 0.3) !important;
}

.custom-send-button {
    background: linear-gradient(135deg, #ea580c, #dc2626) !important;
    border-radius: 50% !important;
    width: 52px !important;
    height: 52px !important;
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
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
}

.custom-send-button:hover {
    background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
    transform: translateY(-50%) scale(1.08) !important;
    box-shadow: 0 8px 20px rgba(234, 88, 12, 0.55) !important;
}

.custom-send-button:active {
    transform: translateY(-50%) scale(0.96) !important;
}

/* === RESPONSIVE MEJORADO === */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 0.8rem 150px 0.8rem !important;
    }
    
    .header {
        padding: 2rem 1.5rem;
        margin-bottom: 2rem;
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
        margin: 8px 0 8px auto;
    }
    
    .bot {
        margin: 8px auto 8px 0;
    }
    
    .custom-input-container {
        padding: 14px 10px 20px 10px !important;
    }
    
    .custom-text-input {
        font-size: 0.92rem !important;
        padding: 14px 60px 14px 16px !important;
    }
    
    .custom-send-button {
        width: 46px !important;
        height: 46px !important;
        right: 6px !important;
        font-size: 16px !important;
    }
}

/* === ELIMINAR ESPACIOS DE AVATARES === */
[data-testid="stChatMessage"] > div {
    gap: 0px !important;
    padding-left: 0px !important;
    padding-right: 0px !important;
}

[data-testid="stChatMessage"] > div > div:first-child {
    display: none !important;
    width: 0px !important;
    min-width: 0px !important;
}
</style>

<!-- JAVASCRIPT MÁS AGRESIVO -->
<script>
function eliminarElementosNoDeseados() {
    // Eliminar por selectores
    const selectores = [
        'header', 'footer',
        '[data-testid="stToolbar"]',
        '[data-testid="stDeployButton"]',
        '.stDeployButton',
        '[data-testid="stStatusWidget"]',
        '[data-testid="stDecoration"]',
        'button[title*="Deploy"]',
        'button[title*="View"]',
        'a[href*="github"]',
        'a[href*="streamlit"]',
        '[data-testid="stChatMessageAvatar"]',
        '[data-testid="stAvatar"]',
        '.stChatMessage img',
        '.stChatMessage svg',
        '[data-testid="stChatMessage"] img',
        '[data-testid="stChatMessage"] svg'
    ];
    
    selectores.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.remove();
            el.style.display = 'none';
            el.style.visibility = 'hidden';
        });
    });
    
    // Eliminar contenedores de avatares
    document.querySelectorAll('[data-testid="stChatMessage"] > div > div:first-child').forEach(el => {
        el.remove();
        el.style.display = 'none';
    });
    
    // Eliminar cualquier elemento en esquinas
    document.querySelectorAll('*').forEach(el => {
        const rect = el.getBoundingClientRect();
        if ((rect.top === 0 && rect.right <= 100) || (rect.top === 0 && rect.left >= window.innerWidth - 100)) {
            el.remove();
        }
    });
}

// Ejecutar inmediatamente y persistentemente
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', eliminarElementosNoDeseados);
} else {
    eliminarElementosNoDeseados();
}

// Ejecutar múltiples veces
setTimeout(eliminarElementosNoDeseados, 100);
setTimeout(eliminarElementosNoDeseados, 500);
setTimeout(eliminarElementosNoDeseados, 1000);

// Ejecutar cada 2 segundos por 10 segundos
let count = 0;
const interval = setInterval(() => {
    eliminarElementosNoDeseados();
    count++;
    if (count > 5) clearInterval(interval);
}, 2000);
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

# ==================== INPUT PERSONALIZADO - NO USAR st.chat_input ====================
st.markdown("""
<div class="custom-input-container">
    <div class="custom-input-wrapper">
        <input type="text" class="custom-text-input" id="customChatInput" placeholder="Escribe tu consulta aquí..." />
        <button class="custom-send-button" onclick="sendMessage()">➤</button>
    </div>
</div>

<script>
function sendMessage() {
    const input = document.getElementById('customChatInput');
    const message = input.value.trim();
    
    if (message) {
        // Usar query parameters para enviar el mensaje
        const url = new URL(window.location);
        url.searchParams.set('user_message', message);
        window.history.pushState({}, '', url);
        
        // Recargar la página
        window.location.reload();
    }
}

// Enviar con Enter
document.getElementById('customChatInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Focus automático
setTimeout(() => {
    const input = document.getElementById('customChatInput');
    if (input) input.focus();
}, 1000);
</script>
""", unsafe_allow_html=True)

# ==================== PROCESAR MENSAJES ====================
query_params = st.experimental_get_query_params()
user_message = query_params.get("user_message", [None])[0]

if user_message and user_message != st.session_state.get("last_processed_message", ""):
    st.session_state.last_processed_message = user_message
    
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    # Obtener respuesta
    try:
        response = requests.post(
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
                    {"role": "user", "content": user_message},
                ],
            },
            timeout=30,
        )
        answer = response.json()["choices"][0]["message"]["content"]
    except Exception:
        answer = (
            "⚠️ Problema de conexión. Contacta a Belén Bastías: "
            "belen.bastias@nutrisco.com"
        )
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
    
    # Limpiar parámetros
    st.experimental_set_query_params()
    
    # Recargar para mostrar nuevos mensajes
    st.rerun()

st.markdown(
    '<div class="footer">'
    'Inteligencia Artificial al servicio de las personas – Nutrisco © 2025'
    '</div>',
    unsafe_allow_html=True,
)
