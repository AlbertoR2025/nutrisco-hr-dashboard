# pages/4_🤖_Chatbot Colaboradores.py
import streamlit as st
import pandas as pd
import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="Chatbot Colaboradores – Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CSS NUCLEAR - ELIMINAR CORONA Y AVATARES ====================
st.markdown("""
<style>
    /* === ELIMINACIÓN COMPLETA DE TODOS LOS ELEMENTOS STREAMLIT === */
    
    /* 1. ELIMINAR CORONA (DEPLOY BUTTON) - MÁS AGRESIVO */
    [data-testid="stDeployButton"],
    .stAppDeployButton,
    button[title="View app source"],
    button[title="Deploy this app"],
    [data-testid="baseButton-secondary"] {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
        height: 0px !important;
        opacity: 0 !important;
        position: absolute !important;
        left: -9999px !important;
        z-index: -9999 !important;
    }
    
    /* 2. ELIMINAR HEADER COMPLETO */
    header, [data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
        visibility: hidden !important;
    }
    
    /* 3. ELIMINAR FOOTER Y TOOLBAR */
    footer, [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 4. ELIMINAR AVATARES COMPLETAMENTE */
    [data-testid="stChatMessage"] [data-testid="stAvatar"],
    [data-testid="stChatMessage"] img,
    [data-testid="stChatMessage"] svg,
    [data-testid="stChatInput"] [data-testid="stAvatar"],
    [data-testid="stChatInput"] img,
    [data-testid="stChatInput"] svg {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    
    /* === ESTILOS DE LA APLICACIÓN === */
    .main .block-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
        padding-bottom: 120px !important;
    }
    
    .stApp {
        background-color: #0e1117 !important;
    }
    
    .header-box {
        background: linear-gradient(90deg, #ea580c, #c2410c);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(234,88,12,0.4);
    }
    
    .user-msg {
        background: #262730;
        color: white;
        border-radius: 18px;
        padding: 14px 20px;
        margin: 12px 0 12px auto;
        max-width: 75%;
        box-shadow: 0 2px 10px rgba(0,0,0,0.4);
    }
    
    .assistant-msg {
        background: linear-gradient(135deg, #ea580c, #f97316);
        color: white;
        border-radius: 18px;
        padding: 14px 20px;
        margin: 12px auto 12px 0;
        max-width: 75%;
        box-shadow: 0 4px 15px rgba(249,115,22,0.5);
    }
    
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #64748b;
        padding: 2rem 0;
    }
    
    /* === INPUT PERSONALIZADO CON Z-INDEX MUY ALTO === */
    .custom-input-container {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: #0e1117 !important;
        padding: 1rem !important;
        border-top: 1px solid #333 !important;
        z-index: 2147483647 !important; /* Máximo z-index posible */
        display: flex !important;
        justify-content: center !important;
    }
    
    .custom-input-wrapper {
        display: flex !important;
        gap: 10px !important;
        width: 90% !important;
        max-width: 800px !important;
        align-items: center !important;
    }
    
    .custom-text-input {
        flex: 1 !important;
        background: #1e1e1e !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        outline: none !important;
        z-index: 2147483647 !important;
    }
    
    .custom-text-input:focus {
        border-color: #ea580c !important;
        box-shadow: 0 0 0 2px rgba(234, 88, 12, 0.2) !important;
    }
    
    .custom-send-button {
        background: #ea580c !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 18px !important;
        z-index: 2147483647 !important;
    }
    
    .custom-send-button:hover {
        background: #c2410c !important;
    }
    
    @media (max-width: 768px) {
        .custom-input-wrapper {
            width: 95% !important;
        }
        
        .user-msg, .assistant-msg {
            max-width: 85% !important;
        }
        
        .header-box {
            padding: 1.5rem !important;
        }
    }
</style>

<!-- JAVASCRIPT MÁS AGRESIVO PARA ELIMINAR LA CORONA -->
<script>
function eliminarCoronaYAvatares() {
    // ELIMINAR CORONA Y BOTONES DE DEPLOY
    const elementosCorona = document.querySelectorAll([
        '[data-testid="stDeployButton"]',
        '.stAppDeployButton', 
        'button[title*="Deploy"]',
        'button[title*="View"]',
        '[data-testid="baseButton-secondary"]',
        'header',
        '[data-testid="stHeader"]'
    ].join(','));
    
    elementosCorona.forEach(el => {
        el.remove();
        el.style.display = 'none';
        el.style.visibility = 'hidden';
        el.style.opacity = '0';
    });
    
    // ELIMINAR AVATARES
    const avatares = document.querySelectorAll([
        '[data-testid="stAvatar"]',
        '[data-testid="stChatMessageAvatar"]',
        '.stChatMessage img',
        '.stChatMessage svg'
    ].join(','));
    
    avatares.forEach(avatar => {
        avatar.remove();
        avatar.style.display = 'none';
    });
    
    // FORZAR ELIMINACIÓN DE ELEMENTOS EN EL BODY
    document.querySelectorAll('*').forEach(el => {
        const style = window.getComputedStyle(el);
        if (style.position === 'fixed' && (style.top === '0px' || style.right === '0px')) {
            if (el.innerHTML.includes('Deploy') || el.innerHTML.includes('Streamlit')) {
                el.remove();
            }
        }
    });
}

// EJECUTAR INMEDIATAMENTE Y PERSISTENTEMENTE
document.addEventListener('DOMContentLoaded', eliminarCoronaYAvatares);
setTimeout(eliminarCoronaYAvatares, 100);
setTimeout(eliminarCoronaYAvatares, 500);
setTimeout(eliminarCoronaYAvatares, 1000);

// EJECUTAR CADA SEGUNDO DURANTE 10 SEGUNDOS
let ejecuciones = 0;
const intervalo = setInterval(() => {
    eliminarCoronaYAvatares();
    ejecuciones++;
    if (ejecuciones > 10) clearInterval(intervalo);
}, 1000);
</script>
""", unsafe_allow_html=True)

# ==================== LÓGICA DE LA APLICACIÓN ====================
API_KEY = os.getenv("OPENAI_API_KEY")

# Header
st.markdown("""
<div class="header-box">
    <h1 style="margin:0; font-size: 2.2rem;">Chatbot Colaboradores</h1>
    <h2 style="margin:8px 0 0 0; font-weight:300; font-size: 1.3rem;">Nutrisco – Atención Personas</h2>
    <p style="margin:15px 0 0 0; opacity: 0.9;">Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

# Mensaje de bienvenida
st.markdown("""
<div class="assistant-msg">
    <strong>¡Hola! 👋</strong> Soy parte del equipo de <strong>Atención a Personas</strong> de Nutrisco.<br><br>
    Puedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.<br><br>
    ¡Estoy aquí para ayudarte!
</div>
""", unsafe_allow_html=True)

# ==================== CHAT CON INPUT PERSONALIZADO ====================
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-msg">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-msg">{message["content"]}</div>', unsafe_allow_html=True)

# ==================== INPUT PERSONALIZADO CON BOTÓN VISIBLE ====================
st.markdown("""
<div class="custom-input-container">
    <div class="custom-input-wrapper">
        <input type="text" class="custom-text-input" id="customChatInput" placeholder="Escribe tu consulta aquí..." />
        <button class="custom-send-button" onclick="sendCustomMessage()">➤</button>
    </div>
</div>

<script>
function sendCustomMessage() {
    const input = document.getElementById('customChatInput');
    const message = input.value.trim();
    
    if (message) {
        // Usar Streamlit's set_query_params para enviar el mensaje
        const url = new URL(window.location);
        url.searchParams.set('user_message', message);
        window.history.pushState({}, '', url);
        
        // Recargar la página para procesar el mensaje
        window.location.reload();
    }
}

// Permitir enviar con Enter
document.getElementById('customChatInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendCustomMessage();
    }
});

// Focus en el input al cargar
setTimeout(() => {
    const input = document.getElementById('customChatInput');
    if (input) input.focus();
}, 1000);
</script>
""", unsafe_allow_html=True)

# ==================== PROCESAR MENSAJES DESDE URL ====================
# Obtener mensaje de los query parameters
query_params = st.experimental_get_query_params()
user_message = query_params.get("user_message", [None])[0]

if user_message and user_message != st.session_state.get("last_processed_message", ""):
    st.session_state.last_processed_message = user_message
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    # Display user message
    st.markdown(f'<div class="user-msg">{user_message}</div>', unsafe_allow_html=True)
    
    # Display assistant response
    with st.spinner("Pensando..."):
        time.sleep(1)
        
        # Get AI response
        try:
            if API_KEY:
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {
                                "role": "system", 
                                "content": "Eres un asistente de RR.HH. de Nutrisco. Responde de manera profesional y cercana. Para temas delicados, deriva a Belén Bastías."
                            },
                            {"role": "user", "content": user_message}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500
                    },
                    timeout=30
                )
                assistant_response = response.json()["choices"][0]["message"]["content"]
            else:
                assistant_response = "Error: No se configuró la API key"
        except Exception as e:
            assistant_response = "Error de conexión. Contacta a Belén Bastías: belen.bastias@nutrisco.com"
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # Clear query parameters
    st.experimental_set_query_params()
    
    # Rerun to show new messages
    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco © 2025
</div>
""", unsafe_allow_html=True)
