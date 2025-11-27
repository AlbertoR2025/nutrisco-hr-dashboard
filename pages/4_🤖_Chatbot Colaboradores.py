# app_nutrisco_sin_chat.py
import streamlit as st
import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIGURACIÓN MÍNIMA ====================
st.set_page_config(
    page_title="Asistente Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== CSS COMPLETO - ELIMINAR TODO ====================
st.markdown("""
<style>
    /* ELIMINAR ABSOLUTAMENTE TODO DE STREAMLIT */
    header {display: none !important; height: 0px !important;}
    footer {display: none !important; height: 0px !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDeployButton"] {display: none !important;}
    [data-testid="stChatMessage"] {display: none !important;}
    [data-testid="stChatInput"] {display: none !important;}
    .stChatMessage {display: none !important;}
    
    /* ELIMINAR CUALQUIER ELEMENTO CON AVATAR O CORONA */
    [class*="avatar"], [class*="Avatar"], [data-testid*="avatar"], 
    [class*="crown"], [class*="Crown"], [data-testid*="crown"],
    img, svg, [alt*="avatar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
        height: 0px !important;
        opacity: 0 !important;
    }
    
    /* ESTILOS PARA CHAT PERSONALIZADO */
    .main {
        background-color: #0e1117;
        padding: 0px !important;
    }
    
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        min-height: 100vh;
    }
    
    .header {
        background: linear-gradient(90deg, #ea580c, #c2410c);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(234,88,12,0.4);
    }
    
    .chat-area {
        min-height: 400px;
        margin-bottom: 100px;
    }
    
    .message {
        padding: 12px 18px;
        margin: 10px 0;
        border-radius: 18px;
        max-width: 70%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: #262730;
        color: white;
        margin-left: auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #ea580c, #f97316);
        color: white;
        margin-right: auto;
        box-shadow: 0 4px 12px rgba(249,115,22,0.4);
    }
    
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #0e1117;
        padding: 1rem;
        border-top: 1px solid #333;
        z-index: 1000;
    }
    
    .input-box {
        width: 100%;
        padding: 12px 16px;
        border-radius: 25px;
        border: 1px solid #444;
        background: #1e1e1e;
        color: white;
        font-size: 16px;
    }
    
    .input-box:focus {
        outline: none;
        border-color: #ea580c;
    }
    
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #64748b;
        padding: 2rem 0;
    }
    
    .typing {
        font-style: italic;
        color: #94a3b8;
        margin: 10px 0;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    @media (max-width: 768px) {
        .container {
            padding: 10px;
        }
        .message {
            max-width: 85%;
        }
        .header {
            padding: 1.5rem;
        }
    }
</style>

<!-- JAVASCRIPT PARA ELIMINAR ELEMENTOS PERSISTENTES -->
<script>
function eliminarTodo() {
    // Eliminar cualquier elemento de Streamlit
    const elementos = document.querySelectorAll([
        'header', 'footer', '[data-testid="stToolbar"]', 
        '[data-testid="stDeployButton"]', '[data-testid="stChatMessage"]',
        '.stChatMessage', 'img', 'svg', '[class*="avatar"]'
    ].join(','));
    
    elementos.forEach(el => {
        el.remove();
        el.style.display = 'none';
    });
}

// Ejecutar inmediatamente y cada segundo
eliminarTodo();
setInterval(eliminarTodo, 1000);
</script>
""", unsafe_allow_html=True)

# ==================== INICIALIZACIÓN ====================
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("⚠️ Configura OPENAI_API_KEY en Secrets")
    st.stop()

# Inicializar mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "assistant", "content": "¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"}
    ]

# ==================== INTERFAZ PERSONALIZADA ====================
st.markdown("""
<div class="container">
    <div class="header">
        <h1 style="margin:0; font-size: 2.2rem;">Asistente Colaboradores</h1>
        <p style="margin:10px 0 0 0; font-size: 1.1rem;">Nutrisco - Atención a Personas</p>
    </div>
    
    <div class="chat-area">
""", unsafe_allow_html=True)

# Mostrar mensajes
for msg in st.session_state.mensajes:
    if msg["role"] == "user":
        st.markdown(f'<div class="message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # Cerrar chat-area

# ==================== INPUT PERSONALIZADO ====================
st.markdown("""
<div class="input-container">
    <form id="chat-form">
        <input type="text" class="input-box" name="pregunta" placeholder="Escribe tu consulta aquí..." autocomplete="off">
    </form>
</div>
""", unsafe_allow_html=True)

# ==================== PROCESAR INPUT ====================
# Usar query parameters para evitar reruns automáticos
query_params = st.experimental_get_query_params()
pregunta = query_params.get("pregunta", [""])[0]

if pregunta and pregunta != st.session_state.get("ultima_pregunta", ""):
    st.session_state.ultima_pregunta = pregunta
    
    # Agregar mensaje del usuario
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    
    # Mostrar indicador de escritura
    typing_placeholder = st.empty()
    typing_placeholder.markdown('<div class="typing">Escribiendo<span style="animation: blink 1s infinite;">...</span></div>', unsafe_allow_html=True)
    
    # Obtener respuesta
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Eres un asistente de RR.HH. de Nutrisco en Chile. Responde de manera profesional y cercana."},
                    {"role": "user", "content": pregunta}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            },
            timeout=30
        )
        respuesta = response.json()["choices"][0]["message"]["content"]
    except:
        respuesta = "⚠️ Ahora tengo problemas de conexión. Por favor contacta a Belén Bastías: belen.bastias@nutrisco.com o interno 7219."
    
    # Agregar respuesta
    st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
    
    # Limpiar query params
    st.experimental_set_query_params()
    
    # Rerun para mostrar nuevos mensajes
    st.rerun()

# Footer
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco © 2025
</div>
</div>  <!-- Cerrar container -->
""", unsafe_allow_html=True)

# ==================== JAVASCRIPT PARA ENVIAR FORMULARIO ====================
st.markdown("""
<script>
// Enviar formulario cuando se presione Enter
document.querySelector('.input-box').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const pregunta = this.value;
        if (pregunta.trim() !== '') {
            // Actualizar URL con parámetro
            const url = new URL(window.location);
            url.searchParams.set('pregunta', pregunta);
            window.history.pushState({}, '', url);
            
            // Recargar la página
            window.location.reload();
        }
    }
});

// Focus en el input al cargar
document.querySelector('.input-box').focus();
</script>
""", unsafe_allow_html=True)
