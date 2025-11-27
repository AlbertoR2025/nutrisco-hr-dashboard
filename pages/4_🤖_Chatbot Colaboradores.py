# pages/4_Chatbot Colaboradores.py → VERSIÓN DEFINITIVA SIN AVATARES
import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIGURACIÓN INICIAL ====================
st.set_page_config(
    page_title="Chatbot RR.HH. Nutrisco", 
    page_icon="💬", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== APPROACH COMPLETAMENTE NUEVO ====================
st.markdown("""
<style>
    /* ELIMINAR COMPLETAMENTE EL HEADER DE STREAMLIT */
    header {visibility: hidden !important; height: 0px !important;}
    .stApp > header {display: none !important;}
    
    /* ELIMINAR HERRAMIENTAS DE STREAMLIT */
    #MainMenu {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    footer {visibility: hidden !important;}
    [data-testid="stToolbar"] {display: none !important;}
    
    /* ELIMINACIÓN ESPECÍFICA DE AVATARES EN CHAT */
    [data-testid="stChatMessage"] > div > div:first-child {
        display: none !important;
        width: 0px !important;
        min-width: 0px !important;
    }
    
    /* ELIMINAR CUALQUIER IMAGEN O SVG EN EL CHAT */
    [data-testid="stChatMessage"] img,
    [data-testid="stChatMessage"] svg,
    [data-testid="stChatMessageAvatar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
        height: 0px !important;
    }
    
    /* AJUSTAR EL LAYOUT SIN AVATARES */
    [data-testid="stChatMessage"] > div {
        gap: 0px !important;
        padding-left: 0px !important;
    }
    
    /* ESTILOS PERSONALIZADOS PARA LA APP */
    .main {
        background-color: #0e1117;
        padding: 1rem;
    }
    
    .user-message {
        background: #262730;
        color: white;
        border-radius: 18px;
        padding: 14px 18px;
        margin: 12px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #ea580c, #f97316);
        color: white;
        border-radius: 18px;
        padding: 14px 18px;
        margin: 12px 0;
        max-width: 80%;
        margin-right: auto;
        box-shadow: 0 4px 12px rgba(249,115,22,0.4);
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
    
    .belén-box {
        background: #dc2626;
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        margin: 1.5rem 0;
        font-size: 1.1rem;
    }
    
    .typing {
        font-style: italic;
        color: #94a3b8;
        text-align: left;
        margin: 15px 0;
    }
    
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #64748b;
        font-size: 0.9rem;
        padding: 1rem 0;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
</style>
""", unsafe_allow_html=True)

# ==================== APPROACH ALTERNATIVO: DESACTIVAR AVATARES A NIVEL DE CHAT ====================
st.markdown("""
<script>
// ENFOQUE DIRECTO: PREVENIR QUE STREAMLIT RENDERICE AVATARES
document.addEventListener('DOMContentLoaded', function() {
    // Override de la función que crea avatares
    const originalCreateElement = document.createElement;
    document.createElement = function(tagName) {
        const element = originalCreateElement.call(this, tagName);
        if (tagName.toLowerCase() === 'img' || tagName.toLowerCase() === 'svg') {
            element.style.display = 'none';
        }
        return element;
    };
    
    // Eliminar avatares existentes
    function removeAvatars() {
        const elements = document.querySelectorAll('[data-testid="stChatMessageAvatar"], img, svg');
        elements.forEach(el => {
            if (el.parentNode) {
                el.parentNode.removeChild(el);
            }
        });
    }
    
    // Ejecutar múltiples veces
    setTimeout(removeAvatars, 100);
    setTimeout(removeAvatars, 500);
    setTimeout(removeAvatars, 1000);
});
</script>
""", unsafe_allow_html=True)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Falta OPENAI_API_KEY en .env o en Streamlit Secrets")
    st.stop()

# ==================== CABECERA ====================
st.markdown("""
<div class="header-box">
    <h1 style="margin:0; font-size: 2.2rem;">Chatbot Colaboradores</h1>
    <h2 style="margin:8px 0 0 0; font-weight:300; font-size: 1.3rem;">Nutrisco – Atención Personas</h2>
    <p style="margin:15px 0 0 0; font-size: 1.1rem; opacity: 0.9;">Escribe tu duda y te respondo al instante</p>
</div>
""", unsafe_allow_html=True)

# ==================== INICIALIZAR CHAT ====================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"
    }]

# ==================== MOSTRAR HISTORIAL ====================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

# ==================== INPUT DEL USUARIO ====================
if pregunta := st.chat_input("Escribe tu consulta aquí..."):
    st.session_state.messages.append({"role": "user", "content": pregunta})
    st.markdown(f'<div class="user-message">{pregunta}</div>', unsafe_allow_html=True)

    placeholder = st.empty()
    placeholder.markdown(
        '<div class="typing">Escribiendo<span style="animation: blink 1s infinite;">...</span></div>', 
        unsafe_allow_html=True
    )
    
    import time
    time.sleep(1.3)
    placeholder.empty()

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system", 
                        "content": """Eres una persona real del equipo de RR.HH. de Nutrisco. 
                        Hablas en español, súper cercano y profesional. 
                        Nunca digas que eres IA. 
                        Si es tema delicado, deriva con tacto a Belén Bastías (interno 7219)."""
                    },
                    {"role": "user", "content": pregunta}
                ],
                "temperature": 0.7,
                "max_tokens": 600
            },
            timeout=30
        )
        respuesta = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        respuesta = "Uy, justo ahora tengo un pequeño problema de conexión. Mejor llámame al interno 7219 o escribe a belen.bastias@nutrisco.com. ¡Perdona las molestias!"

    st.markdown(f'<div class="assistant-message">{respuesta}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

    temas_sensibles = ["agresi", "acoso", "conflicto", "denuncia", "pelea", "maltrato", "insulto", "abus", "discrimin"]
    if any(p in pregunta.lower() for p in temas_sensibles):
        st.markdown("""
        <div class="belén-box">
            Este tema es muy importante<br>
            <strong>Belén Bastías Hurtado</strong> te puede ayudar personalmente<br>
            Correo: belen.bastias@nutrisco.com | Interno: 7219
        </div>
        """, unsafe_allow_html=True)

    try:
        nuevo_registro = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"), 
            "Pregunta": pregunta, 
            "Respuesta": respuesta
        }])
        
        archivo_historial = "data/historial_chatbot.xlsx"
        
        if os.path.exists(archivo_historial):
            historial_existente = pd.read_excel(archivo_historial)
            historial_completo = pd.concat([historial_existente, nuevo_registro], ignore_index=True)
        else:
            os.makedirs("data", exist_ok=True)
            historial_completo = nuevo_registro
            
        historial_completo.to_excel(archivo_historial, index=False)
        
    except Exception as e:
        pass

    st.rerun()

# ==================== FOOTER ACTUALIZADO ====================
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco  © 2025
</div>
""", unsafe_allow_html=True)
