# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN SIN AVATARES DEFINITIVA
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

# ==================== MÉTODO STREAMLIT NATIVO + CSS NUCLEAR ====================
st.markdown("""
<style>
    /* ELIMINACIÓN TOTAL DE AVATARES - ENFOQUE NUCLEAR */
    [data-testid="stChatMessage"] > div > div:first-child,
    [data-testid="stChatMessageAvatar"],
    [data-testid="stAvatar"],
    .stChatMessage img,
    .stChatMessage svg,
    [kind="user"] > div:first-child,
    [kind="assistant"] > div:first-child,
    [data-testid="stChatMessage"] img,
    [data-testid="stChatMessage"] svg {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
        height: 0px !important;
        min-width: 0px !important;
        min-height: 0px !important;
        opacity: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
    }

    /* ELIMINAR COMPLETAMENTE EL CONTENEDOR DEL AVATAR */
    [data-testid="stChatMessage"] > div > div:first-child {
        display: none !important;
        width: 0px !important;
        min-width: 0px !important;
    }

    /* ELIMINAR EL ESPACIO DEL AVATAR */
    [data-testid="stChatMessage"] > div {
        gap: 0px !important;
        margin-left: 0px !important;
        margin-right: 0px !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
    }

    /* ELIMINAR FOOTER STREAMLIT */
    footer, [data-testid="stToolbar"], [data-testid="stDeployButton"] {
        display: none !important;
    }

    /* ESTILOS DE LA APLICACIÓN */
    .main .block-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }

    .user-message {
        background: #262730;
        color: white;
        border-radius: 18px;
        padding: 14px 20px;
        margin: 12px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.4);
    }

    .assistant-message {
        background: linear-gradient(135deg, #ea580c, #f97316);
        color: white;
        border-radius: 18px;
        padding: 14px 20px;
        margin: 12px 0;
        max-width: 80%;
        margin-right: auto;
        box-shadow: 0 4px 15px rgba(249,115,22,0.5);
    }

    .header-box {
        background: linear-gradient(90deg, #ea580c, #c2410c);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(234,88,12,0.4);
        margin: 0 auto 2rem auto;
    }

    .belén-box {
        background: #dc2626;
        color: white;
        padding: 1.3rem;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        margin: 2rem auto;
        font-size: 1.15rem;
        box-shadow: 0 4px 15px rgba(220,38,38,0.4);
    }

    .footer {
        text-align: center;
        margin-top: 4rem;
        color: #64748b;
        font-size: 0.95rem;
        padding: 2rem 0;
    }

    .typing {
        font-style: italic;
        color: #94a3b8;
        margin: 15px 0;
        text-align: left;
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }

    @media (max-width: 768px) {
        .user-message, .assistant-message {
            max-width: 95%;
            padding: 12px 16px;
            margin: 10px 0;
        }
        .header-box {
            padding: 1.5rem;
        }
        .belén-box {
            font-size: 1rem;
            padding: 1rem;
        }
    }
</style>

<!-- JAVASCRIPT DE ELIMINACIÓN INMEDIATA -->
<script>
function eliminarAvataresCompletamente() {
    // Eliminar todos los avatares y contenedores
    const elementos = document.querySelectorAll([
        '[data-testid="stChatMessageAvatar"]',
        '[data-testid="stAvatar"]',
        '[data-testid="stChatMessage"] img',
        '[data-testid="stChatMessage"] svg',
        '.stChatMessage img',
        '.stChatMessage svg',
        '[kind="user"] > div:first-child',
        '[kind="assistant"] > div:first-child'
    ].join(','));
    
    elementos.forEach(el => {
        el.remove();
        el.style.display = 'none';
        el.style.visibility = 'hidden';
    });

    // Eliminar contenedores padre de avatares
    document.querySelectorAll('[data-testid="stChatMessage"] > div > div:first-child').forEach(div => {
        div.remove();
        div.style.display = 'none';
    });
}

// Ejecutar inmediatamente y repetidamente
document.addEventListener('DOMContentLoaded', eliminarAvataresCompletamente);
setTimeout(eliminarAvataresCompletamente, 100);
setTimeout(eliminarAvataresCompletamente, 500);
setTimeout(eliminarAvataresCompletamente, 1000);
setTimeout(eliminarAvataresCompletamente, 2000);
setInterval(eliminarAvataresCompletamente, 3000);
</script>
""", unsafe_allow_html=True)

# ==================== CLAVE OPENAI ====================
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("⚠️ Falta la clave OPENAI_API_KEY en Secrets o .env")
    st.stop()

# ==================== CABECERA CORPORATIVA ====================
st.markdown("""
<div class="header-box">
    <h1 style="margin:0; font-size: 2.2rem; font-weight: 700;">Chatbot Colaboradores</h1>
    <h2 style="margin:8px 0 0 0; font-weight: 400; font-size: 1.3rem;">Nutrisco – Atención Personas</h2>
    <p style="margin:15px 0 0 0; opacity: 0.9; font-size: 1.1rem;">Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

# ==================== INICIALIZAR CHAT ====================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"
    }]

# ==================== MOSTRAR HISTORIAL - SIN AVATARES ====================
for msg in st.session_state.messages:
    # USAR SOLO MARKDOWN - EVITAR st.chat_message COMPLETAMENTE
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

# ==================== INPUT Y PROCESAMIENTO ====================
if pregunta := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": pregunta})
    
    # Mostrar mensaje del usuario SIN usar chat_message
    st.markdown(f'<div class="user-message">{pregunta}</div>', unsafe_allow_html=True)

    # Indicador de escritura
    placeholder = st.empty()
    placeholder.markdown('<div class="typing">Escribiendo<span style="animation: blink 1s infinite;">...</span></div>', unsafe_allow_html=True)
    time.sleep(1.5)
    placeholder.empty()

    # Obtener respuesta de OpenAI
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
                        "content": "Eres un asistente de RR.HH. de Nutrisco. Responde de manera profesional y cercana. Para temas delicados, deriva a Belén Bastías."
                    },
                    {"role": "user", "content": pregunta}
                ]
            },
            timeout=30
        )
        respuesta = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        respuesta = "⚠️ Ahora tengo problemas de conexión. Contacta a Belén Bastías: belen.bastias@nutrisco.com o interno 7219."

    # Mostrar respuesta SIN usar chat_message
    st.markdown(f'<div class="assistant-message">{respuesta}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

    # Detectar temas sensibles
    temas_sensibles = ["agresi", "acoso", "denuncia", "conflicto", "pelea", "maltrato", "insulto"]
    if any(p in pregunta.lower() for p in temas_sensibles):
        st.markdown("""
        <div class="belén-box">
            💡 <strong>Para este tema específico</strong><br>
            Contacta directamente a <strong>Belén Bastías Hurtado</strong><br>
            📧 belen.bastias@nutrisco.com | ☎ Interno: 7219
        </div>
        """, unsafe_allow_html=True)

    # Guardar en historial
    try:
        nuevo = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Pregunta": pregunta,
            "Respuesta": respuesta
        }])
        
        archivo = "data/historial_chatbot.xlsx"
        os.makedirs("data", exist_ok=True)
        
        if os.path.exists(archivo):
            df_existente = pd.read_excel(archivo)
            df_final = pd.concat([df_existente, nuevo], ignore_index=True)
        else:
            df_final = nuevo
            
        df_final.to_excel(archivo, index=False)
    except Exception as e:
        pass  # Silenciar errores de archivo

    st.rerun()

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco © 2025
</div>
""", unsafe_allow_html=True)

# ==================== INYECCIÓN FINAL DE JAVASCRIPT ====================
st.markdown("""
<script>
// ELIMINACIÓN FINAL GARANTIZADA
setTimeout(() => {
    // Método nuclear: eliminar cualquier imagen o SVG en toda la app
    document.querySelectorAll('img, svg').forEach(element => {
        if (element.parentElement && 
            (element.closest('[data-testid="stChatMessage"]') || 
             element.getAttribute('alt')?.includes('avatar') ||
             element.innerHTML?.includes('avatar'))) {
            element.remove();
        }
    });
}, 3000);
</script>
""", unsafe_allow_html=True)
