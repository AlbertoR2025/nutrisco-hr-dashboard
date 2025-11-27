# pages/4_🤖_Chatbot Colaboradores.py → DISEÑO MODERNO
import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Chatbot Nutrisco", page_icon="💬", layout="centered")

# CSS MODERNO Y ELEGANTE
st.markdown("""
<style>
    /* === ELIMINAR ELEMENTOS STREAMLIT === */
    header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"], 
    .stDeployButton, [data-testid="stStatusWidget"], a[href*="github"], 
    a[href*="streamlit"] {
        display: none !important;
    }
    
    /* === FONDO Y CONTENEDOR PRINCIPAL === */
    .stApp {
        background: #0e1117;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .block-container {
        max-width: 900px;
        padding: 1rem;
        padding-bottom: 140px;
    }
    
    /* === HEADER MODERNO === */
    .modern-header {
        background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
        padding: 2.5rem;
        border-radius: 24px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(234, 88, 12, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    .modern-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .modern-header h2 {
        margin: 8px 0 0 0;
        font-weight: 400;
        font-size: 1.3rem;
        opacity: 0.9;
    }
    
    .modern-header p {
        margin: 15px 0 0 0;
        opacity: 0.8;
        font-size: 1.1rem;
    }
    
    /* === MENSAJES DE CHAT MODERNOS === */
    .user-message {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border-radius: 20px;
        padding: 18px 24px;
        margin: 16px 8% 16px auto;
        max-width: 70%;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        backdrop-filter: blur(10px);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #ea580c 0%, #dc2626 100%);
        color: white;
        border-radius: 20px;
        padding: 18px 24px;
        margin: 16px auto 16px 8%;
        max-width: 70%;
        box-shadow: 0 8px 25px rgba(234, 88, 12, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        backdrop-filter: blur(10px);
    }
    
    /* === INPUT MODERNO Y ELEGANTE === */
    .modern-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(20px);
        padding: 20px;
        box-sizing: border-box;
        z-index: 1000;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    
    .modern-input-wrapper {
        max-width: 900px;
        margin: 0 auto;
        display: flex;
        gap: 12px;
        align-items: center;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 25px;
        padding: 8px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .modern-text-input {
        flex: 1;
        padding: 16px 20px;
        border: none;
        background: transparent;
        color: white;
        font-size: 1.1rem;
        outline: none;
        border-radius: 20px;
    }
    
    .modern-text-input::placeholder {
        color: #94a3b8;
    }
    
    .modern-send-button {
        background: linear-gradient(135deg, #ea580c 0%, #dc2626 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 56px;
        height: 56px;
        cursor: pointer;
        font-size: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(234, 88, 12, 0.4);
    }
    
    .modern-send-button:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 25px rgba(234, 88, 12, 0.6);
    }
    
    .modern-send-button:active {
        transform: translateY(0) scale(0.95);
    }
    
    /* === FOOTER ELEGANTE === */
    .modern-footer {
        text-align: center;
        margin-top: 4rem;
        color: #64748b;
        font-size: 0.95rem;
        padding: 2rem 0;
        opacity: 0.8;
    }
    
    /* === EFECTOS DE TEXTO === */
    .message-typing {
        display: inline-block;
        animation: typing 1.5s infinite;
    }
    
    @keyframes typing {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    
    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .modern-header {
            padding: 2rem 1.5rem;
            border-radius: 20px;
        }
        
        .modern-header h1 {
            font-size: 2rem;
        }
        
        .user-message, .bot-message {
            max-width: 85%;
            padding: 16px 20px;
            margin: 12px 4% 12px auto;
        }
        
        .modern-input-wrapper {
            margin: 0 10px;
        }
        
        .modern-text-input {
            font-size: 1rem;
            padding: 14px 18px;
        }
        
        .modern-send-button {
            width: 50px;
            height: 50px;
        }
    }
    
    /* === EFECTO DE CARGA === */
    .loading-dots {
        display: inline-flex;
        gap: 4px;
    }
    
    .loading-dots span {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: currentColor;
        animation: loading 1.4s ease-in-out infinite both;
    }
    
    .loading-dots span:nth-child(1) { animation-delay: -0.32s; }
    .loading-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes loading {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Falta OPENAI_API_KEY")
    st.stop()

# HEADER MODERNO
st.markdown("""
<div class="modern-header">
    <h1>🤖 Chatbot Colaboradores</h1>
    <h2>Nutrisco – Atención Personas</h2>
    <p>Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

# INICIALIZAR MENSAJES
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "bot", 
        "content": "¡Hola! 👋 Soy tu asistente virtual de **Atención a Personas** en Nutrisco.\n\nPuedes consultarme sobre:\n\n• **Licencias y permisos**\n• **Beneficios corporativos**  \n• **Plataforma BUK**\n• **Finiquitos y liquidaciones**\n• **Vestimenta y uniformes**\n• **Bono Fisherman**\n• **Y mucho más...**\n\n¡Estoy aquí para ayudarte! 💪"
    }]

# MOSTRAR HISTORIAL DE CHAT
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{msg["content"]}</div>', unsafe_allow_html=True)

# INPUT MODERNO CON BOTÓN ELEGANTE
st.markdown("""
<div class="modern-input-container">
    <div class="modern-input-wrapper">
        <input type="text" class="modern-text-input" id="modernChatInput" placeholder="Escribe tu mensaje aquí..." />
        <button class="modern-send-button" onclick="sendModernMessage()">
            <span style="transform: rotate(90deg); display: inline-block;">➤</span>
        </button>
    </div>
</div>

<script>
function sendModernMessage() {
    const input = document.getElementById('modernChatInput');
    const message = input.value.trim();
    
    if (message) {
        // Agregar parámetro a la URL
        const url = new URL(window.location);
        url.searchParams.set('user_message', message);
        window.history.pushState({}, '', url);
        
        // Recargar para procesar
        window.location.reload();
    }
}

// Enviar con Enter
document.getElementById('modernChatInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendModernMessage();
    }
});

// Focus automático
setTimeout(() => {
    const input = document.getElementById('modernChatInput');
    if (input) input.focus();
}, 500);
</script>
""", unsafe_allow_html=True)

# PROCESAR MENSAJES
query_params = st.experimental_get_query_params()
user_message = query_params.get("user_message", [None])[0]

if user_message and user_message != st.session_state.get("last_processed_message", ""):
    st.session_state.last_processed_message = user_message
    
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.markdown(f'<div class="user-message">{user_message}</div>', unsafe_allow_html=True)
    
    # Mostrar indicador de escritura
    with st.spinner(""):
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="bot-message">
            Escribiendo respuesta<span class="loading-dots"><span></span><span></span><span></span></span>
        </div>
        """, unsafe_allow_html=True)
        
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
                            "content": """Eres un asistente de RRHH de Nutrisco en Chile. 
                            Responde de manera profesional, cercana y amable. 
                            Usa emojis apropiados y un tono cálido pero profesional.
                            Para temas delicados (acoso, conflicto, denuncia), deriva con tacto a Belén Bastías."""
                        },
                        {"role": "user", "content": user_message}
                    ]
                },
                timeout=30
            )
            respuesta = response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            respuesta = "⚠️ **¡Ups! Parece que hay un problema de conexión.**\n\nPor favor, contacta directamente a:\n\n📧 **Belén Bastías Hurtado**  \n📞 Interno: 7219  \n✉️ belen.bastias@nutrisco.com"
    
    # Limpiar indicador y mostrar respuesta
    typing_placeholder.empty()
    st.session_state.messages.append({"role": "bot", "content": respuesta})
    st.markdown(f'<div class="bot-message">{respuesta}</div>', unsafe_allow_html=True)
    
    # Detectar temas sensibles
    temas_sensibles = ["agresi", "acoso", "denuncia", "conflicto", "pelea", "maltrato", "insulto", "abus", "discrimin"]
    if any(p in user_message.lower() for p in temas_sensibles):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); color: white; padding: 1.5rem; border-radius: 16px; margin: 1.5rem auto; max-width: 70%; box-shadow: 0 8px 25px rgba(220, 38, 38, 0.3); border: 1px solid rgba(255,255,255,0.1);">
            <div style="text-align: center; font-size: 1.1rem;">
                <div style="font-size: 1.3rem; margin-bottom: 8px;">💡 <strong>Asistencia Personalizada</strong></div>
                Para este tipo de consultas, te recomendamos contactar directamente a:<br><br>
                <strong>Belén Bastías Hurtado</strong><br>
                📧 belen.bastias@nutrisco.com<br>
                📞 Interno: 7219
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Limpiar parámetros y recargar
    st.experimental_set_query_params()
    st.rerun()

# FOOTER ELEGANTE
st.markdown("""
<div class="modern-footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco © 2025
</div>
""", unsafe_allow_html=True)
