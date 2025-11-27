# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN NUCLEAR SIN AVATARES
import streamlit as st
import pandas as pd
import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIGURACIÓN INICIAL ====================
st.set_page_config(
    page_title="Chatbot Colaboradores – Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CSS NUCLEAR - ELIMINACIÓN TOTAL ====================
st.markdown("""
<style>
    /* === ELIMINACIÓN TOTAL DE ELEMENTOS STREAMLIT === */
    
    /* 1. ELIMINAR HEADER COMPLETO DE STREAMLIT */
    header, [data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        max-height: 0px !important;
    }
    
    /* 2. ELIMINAR FOOTER Y ELEMENTOS GITHUB */
    footer, [data-testid="stStatusWidget"], 
    [data-testid="stToolbar"], [data-testid="stDeployButton"],
    .stDeployButton, .stAppDeployButton {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        opacity: 0 !important;
    }
    
    /* 3. ELIMINAR CORONA Y BOTONES DE DEPLOY */
    button[title="View app source"], button[title="Deploy this app"],
    [data-testid="baseButton-secondary"] {
        display: none !important;
    }
    
    /* 4. ELIMINACIÓN RADICAL DE AVATARES EN MENSAJES */
    [data-testid="stChatMessage"] [data-testid="stAvatar"],
    [data-testid="stChatMessage"] img,
    [data-testid="stChatMessage"] svg,
    [kind="user"] [data-testid="stAvatar"],
    [kind="assistant"] [data-testid="stAvatar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
        height: 0px !important;
        min-width: 0px !important;
        min-height: 0px !important;
        opacity: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* 5. ELIMINAR CONTENEDORES DE AVATARES */
    [data-testid="stChatMessage"] > div > div:first-child,
    [data-testid="stChatMessage"] > div > div:nth-child(1) {
        display: none !important;
        width: 0px !important;
        min-width: 0px !important;
        visibility: hidden !important;
    }
    
    /* 6. ELIMINAR AVATAR DEL INPUT DE CHAT */
    [data-testid="stChatInput"] [data-testid="stAvatar"],
    [data-testid="stChatInput"] img,
    [data-testid="stChatInput"] svg {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
        height: 0px !important;
    }
    
    /* 7. CORREGIR ESPACIOS SIN AVATARES */
    [data-testid="stChatMessage"] > div {
        gap: 0px !important;
        margin-left: 0px !important;
        margin-right: 0px !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
    }
    
    /* === ESTILOS DE LA APLICACIÓN === */
    
    /* Fondo de la aplicación */
    .stApp {
        background-color: #0e1117 !important;
    }
    
    /* Contenedor principal */
    .main .block-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
        padding-bottom: 100px !important; /* Espacio para el input fijo */
    }
    
    /* Mensajes de usuario */
    .user-message {
        background: #262730;
        color: white;
        border-radius: 18px;
        padding: 14px 20px;
        margin: 12px 0 12px auto;
        max-width: 75%;
        box-shadow: 0 2px 10px rgba(0,0,0,0.4);
    }
    
    /* Mensajes del asistente */
    .assistant-message {
        background: linear-gradient(135deg, #ea580c, #f97316);
        color: white;
        border-radius: 18px;
        padding: 14px 20px;
        margin: 12px auto 12px 0;
        max-width: 75%;
        box-shadow: 0 4px 15px rgba(249,115,22,0.5);
    }
    
    /* Header */
    .header-box {
        background: linear-gradient(90deg, #ea580c, #c2410c);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(234,88,12,0.4);
        margin: 0 auto 2rem auto;
    }
    
    /* Box de Belén */
    .belen-box {
        background: #dc2626;
        color: white;
        padding: 1.3rem;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        margin: 2rem auto;
        box-shadow: 0 4px 15px rgba(220,38,38,0.4);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #64748b;
        padding: 2rem 0;
    }
    
    /* === CORRECCIÓN CRÍTICA DEL INPUT === */
    
    /* Contenedor del input - posicionamiento fijo */
    [data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: #0e1117 !important;
        padding: 1rem !important;
        border-top: 1px solid #333 !important;
        z-index: 9999 !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
    }
    
    /* Textarea del input - completamente visible */
    [data-testid="stChatInput"] textarea {
        flex: 1 !important;
        background: #1e1e1e !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        min-height: 50px !important;
        resize: none !important;
        display: block !important;
        visibility: visible !important;
    }
    
    [data-testid="stChatInput"] textarea:focus {
        outline: none !important;
        border-color: #ea580c !important;
        box-shadow: 0 0 0 2px rgba(234, 88, 12, 0.2) !important;
    }
    
    /* Botón de enviar */
    [data-testid="stChatInput"] button {
        background: #ea580c !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
    }
    
    /* Responsive para móviles */
    @media (max-width: 768px) {
        .main .block-container {
            width: 95% !important;
            padding: 0.5rem !important;
            padding-bottom: 120px !important;
        }
        
        .user-message, .assistant-message {
            max-width: 85% !important;
            padding: 12px 16px !important;
            margin: 10px 0 !important;
        }
        
        .header-box {
            padding: 1.5rem !important;
        }
        
        [data-testid="stChatInput"] {
            padding: 0.8rem !important;
        }
        
        [data-testid="stChatInput"] textarea {
            padding: 10px 16px !important;
            font-size: 14px !important;
        }
    }
</style>

<!-- JAVASCRIPT DE RESPALDO PARA ELIMINAR ELEMENTOS PERSISTENTES -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Función para eliminar elementos persistentes
    function eliminarElementosPersistentes() {
        // Eliminar cualquier avatar residual
        const avatares = document.querySelectorAll([
            '[data-testid="stAvatar"]',
            '[data-testid="stChatMessageAvatar"]',
            '.stChatMessage img',
            '.stChatMessage svg',
            'img[alt*="avatar"]',
            'svg[data-testid*="avatar"]'
        ].join(','));
        
        avatares.forEach(avatar => {
            avatar.remove();
            avatar.style.display = 'none';
        });
        
        // Eliminar footer y elementos GitHub
        const elementosStreamlit = document.querySelectorAll([
            'footer',
            '[data-testid="stToolbar"]',
            '[data-testid="stDeployButton"]',
            '[data-testid="stStatusWidget"]',
            'a[href*="github"]',
            'button[title*="Deploy"]',
            'button[title*="View"]'
        ].join(','));
        
        elementosStreamlit.forEach(elemento => {
            elemento.remove();
            elemento.style.display = 'none';
        });
    }
    
    // Ejecutar múltiples veces
    setTimeout(eliminarElementosPersistentes, 100);
    setTimeout(eliminarElementosPersistentes, 500);
    setTimeout(eliminarElementosPersistentes, 1000);
    setInterval(eliminarElementosPersistentes, 2000);
});
</script>
""", unsafe_allow_html=True)

# ==================== INICIALIZACIÓN ====================
API_KEY = os.getenv("OPENAI_API_KEY")

# ==================== INTERFAZ PRINCIPAL ====================
# Header
st.markdown("""
<div class="header-box">
    <h1 style="margin:0; font-size: 2.2rem;">Chatbot Colaboradores</h1>
    <h2 style="margin:8px 0 0 0; font-weight:300; font-size: 1.3rem;">Nutrisco – Atención Personas</h2>
    <p style="margin:15px 0 0 0; opacity: 0.9;">Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

# Mensaje de bienvenida inicial
st.markdown("""
<div class="assistant-message">
    <strong>¡Hola! 👋</strong> Soy parte del equipo de <strong>Atención a Personas</strong> de Nutrisco.<br><br>
    Puedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.<br><br>
    ¡Estoy aquí para ayudarte!
</div>
""", unsafe_allow_html=True)

# ==================== LÓGICA DEL CHAT ====================
# Inicializar mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de mensajes
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

# Input de chat - ESTA PARTE DEBE SER VISIBLE
user_input = st.chat_input("Escribe tu consulta aquí...")

if user_input:
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Mostrar mensaje del usuario
    st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)
    
    # Mostrar indicador de escritura
    with st.spinner("Escribiendo respuesta..."):
        time.sleep(1)
        
        # Obtener respuesta
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
                            {"role": "user", "content": user_input}
                        ],
                        "temperature": 0.7,
                        "max_tokens": 500
                    },
                    timeout=30
                )
                respuesta = response.json()["choices"][0]["message"]["content"]
            else:
                respuesta = "⚠️ Error: No se configuró OPENAI_API_KEY"
        except Exception as e:
            respuesta = "⚠️ Error de conexión. Contacta a Belén Bastías: belen.bastias@nutrisco.com"
        
        # Agregar y mostrar respuesta
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        st.markdown(f'<div class="assistant-message">{respuesta}</div>', unsafe_allow_html=True)
        
        # Detectar temas sensibles
        temas_sensibles = ["agresi", "acoso", "denuncia", "conflicto", "pelea", "maltrato", "insulto"]
        if any(p in user_input.lower() for p in temas_sensibles):
            st.markdown("""
            <div class="belen-box">
                💡 <strong>Para este tema específico</strong><br>
                Contacta directamente a <strong>Belén Bastías Hurtado</strong><br>
                📧 belen.bastias@nutrisco.com | ☎ Interno: 7219
            </div>
            """, unsafe_allow_html=True)
    
    # Recargar para limpiar input
    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco © 2025
</div>
""", unsafe_allow_html=True)
