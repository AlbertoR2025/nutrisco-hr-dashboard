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

# ==================== CSS NUCLEAR - ELIMINAR TODO Y BOTÓN VISIBLE ====================
st.markdown("""
<style>
    /* === ELIMINACIÓN RADICAL DE ELEMENTOS STREAMLIT === */
    header, [data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
        visibility: hidden !important;
    }
    
    footer, [data-testid="stToolbar"], [data-testid="stDeployButton"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* === ELIMINAR COMPLETAMENTE AVATARES Y CORONAS === */
    [data-testid="stChatMessage"] [data-testid="stAvatar"],
    [data-testid="stChatMessage"] img,
    [data-testid="stChatMessage"] svg,
    [data-testid="stChatInput"] [data-testid="stAvatar"],
    [data-testid="stChatInput"] img,
    [data-testid="stChatInput"] svg,
    .stChatMessage img,
    .stChatMessage svg {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
    
    /* === CONTENEDOR PRINCIPAL CON ESPACIO PARA INPUT === */
    .main .block-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
        padding-bottom: 120px !important; /* Espacio extra para input fijo */
    }
    
    .stApp {
        background-color: #0e1117 !important;
    }
    
    /* === ESTILOS VISUALES === */
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
    
    /* === SOLUCIÓN CRÍTICA: INPUT PERSONALIZADO CON BOTÓN === */
    .custom-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #0e1117;
        padding: 1rem;
        border-top: 1px solid #333;
        z-index: 10000;
        display: flex;
        gap: 10px;
        align-items: center;
        justify-content: center;
    }
    
    .custom-input-wrapper {
        display: flex;
        gap: 10px;
        width: 90%;
        max-width: 800px;
        align-items: center;
    }
    
    .custom-text-input {
        flex: 1;
        background: #1e1e1e;
        color: white;
        border: 1px solid #444;
        border-radius: 25px;
        padding: 12px 20px;
        font-size: 16px;
        outline: none;
    }
    
    .custom-text-input:focus {
        border-color: #ea580c;
        box-shadow: 0 0 0 2px rgba(234, 88, 12, 0.2);
    }
    
    .custom-send-button {
        background: #ea580c;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    
    .custom-send-button:hover {
        background: #c2410c;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .custom-input-wrapper {
            width: 95%;
        }
        
        .user-msg, .assistant-msg {
            max-width: 85%;
        }
        
        .header-box {
            padding: 1.5rem;
        }
    }
</style>

<!-- JAVASCRIPT PARA ELIMINAR ELEMENTOS PERSISTENTES -->
<script>
function eliminarElementosNoDeseados() {
    // Eliminar cualquier avatar residual
    const avatares = document.querySelectorAll('[data-testid="stAvatar"], img, svg');
    avatares.forEach(el => {
        if (el.parentElement && el.closest('[data-testid="stChatMessage"]')) {
            el.remove();
        }
    });
    
    // Eliminar elementos del header
    document.querySelectorAll('header, [data-testid="stHeader"]').forEach(el => {
        el.remove();
    });
}

// Ejecutar múltiples veces
setTimeout(eliminarElementosNoDeseados, 100);
setTimeout(eliminarElementosNoDeseados, 500);
setInterval(eliminarElementosNoDeseados, 1000);
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

# ==================== INPUT PERSONALIZADO CON BOTÓN ====================
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
document.getElementById('customChatInput').focus();
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
