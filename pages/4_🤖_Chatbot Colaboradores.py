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

# ==================== ELIMINACIÓN TOTAL CON JAVASCRIPT + CSS ====================
st.markdown("""
<script>
// ELIMINACIÓN NUCLEAR DE AVATARES Y CORONAS
function eliminarTodo() {
    // Eliminar por selectores
    const selectores = [
        '[data-testid="stChatMessageAvatar"]',
        '[class*="avatar"]',
        '[class*="Avatar"]',
        'img',
        'svg',
        '[data-testid*="avatar"]',
        '[alt*="avatar"]',
        '[class*="crown"]',
        '[class*="Crown"]',
        '[data-testid*="crown"]'
    ];
    
    selectores.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            el.remove();
            el.style.display = 'none';
            el.style.visibility = 'hidden';
            el.style.opacity = '0';
            el.style.width = '0';
            el.style.height = '0';
        });
    });
    
    // Eliminar contenedores de avatares
    document.querySelectorAll('[data-testid="stChatMessage"] > div > div:first-child').forEach(div => {
        if (div.querySelector('img') || div.querySelector('svg') || div.innerHTML.includes('avatar')) {
            div.remove();
        }
    });
    
    // Eliminar por contenido
    document.querySelectorAll('*').forEach(el => {
        if (el.innerHTML && (
            el.innerHTML.toLowerCase().includes('crown') || 
            el.innerHTML.toLowerCase().includes('avatar') ||
            el.outerHTML.toLowerCase().includes('crown') ||
            el.outerHTML.toLowerCase().includes('avatar')
        )) {
            el.remove();
        }
    });
}

// Ejecutar inmediatamente
setTimeout(eliminarTodo, 100);
setTimeout(eliminarTodo, 500);
setTimeout(eliminarTodo, 1000);
setTimeout(eliminarTodo, 2000);

// Ejecutar cada 500ms por 10 segundos
let count = 0;
const interval = setInterval(() => {
    eliminarTodo();
    count++;
    if (count > 20) clearInterval(interval);
}, 500);
</script>

<style>
    /* ELIMINACIÓN RADICAL CON CSS */
    [data-testid="stChatMessageAvatar"],
    [data-testid="stChatMessage"] [data-testid="stAvatar"],
    [data-testid="stChatMessage"] img,
    [data-testid="stChatMessage"] svg,
    [class*="stAvatar"],
    [class*="avatar"],
    [class*="Avatar"],
    [class*="crown"],
    [class*="Crown"],
    [data-testid*="crown"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0px !important;
        height: 0px !important;
        min-width: 0px !important;
        min-height: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
    }
    
    /* ELIMINAR CONTENEDORES DE AVATAR */
    [data-testid="stChatMessage"] > div > div:first-child,
    [data-testid="stChatMessage"] > div > div:first-of-type {
        display: none !important;
        width: 0px !important;
        min-width: 0px !important;
    }
    
    /* AJUSTAR ESPACIOS SIN AVATAR */
    [data-testid="stChatMessage"] > div {
        gap: 0px !important;
        margin-left: 0px !important;
        margin-right: 0px !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
    }
    
    /* ELIMINAR HEADER Y FOOTER STREAMLIT */
    [data-testid="stAppViewContainer"] header,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="collapsedControl"],
    .stDeployButton,
    footer {
        display: none !important;
    }
    
    /* ESTILOS DE LA APLICACIÓN */
    .main {
        background-color: #0e1117;
        padding: 1rem;
        padding-top: 0.5rem !important;
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
        border: 1px solid #404040;
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
        border: 1px solid #f97316;
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
        box-shadow: 0 4px 12px rgba(220,38,38,0.4);
    }
    
    .typing {
        font-style: italic;
        color: #94a3b8;
        text-align: left;
        margin: 15px 0;
    }
    
    .footer {
        text-align: center;
        margin-top: 4rem;
        color: #94a3b8;
        font-size: 0.95rem;
    }
    
    /* ANIMACIÓN TYPING */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
</style>
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

    # Mostrar indicador de escritura
    placeholder = st.empty()
    placeholder.markdown(
        '<div class="typing">Escribiendo<span style="animation: blink 1s infinite;">...</span></div>', 
        unsafe_allow_html=True
    )
    
    # Simular tiempo de respuesta
    import time
    time.sleep(1.3)
    placeholder.empty()

    # Obtener respuesta de OpenAI
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

    # Mostrar respuesta
    st.markdown(f'<div class="assistant-message">{respuesta}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

    # Detectar temas sensibles
    temas_sensibles = ["agresi", "acoso", "conflicto", "denuncia", "pelea", "maltrato", "insulto", "abus", "discrimin"]
    if any(p in pregunta.lower() for p in temas_sensibles):
        st.markdown("""
        <div class="belén-box">
            Este tema es muy importante<br>
            <strong>Belén Bastías Hurtado</strong> te puede ayudar personalmente<br>
            Correo: belen.bastias@nutrisco.com | Interno: 7219
        </div>
        """, unsafe_allow_html=True)

    # Guardar historial en Excel
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
            # Crear directorio si no existe
            os.makedirs("data", exist_ok=True)
            historial_completo = nuevo_registro
            
        historial_completo.to_excel(archivo_historial, index=False)
        
    except Exception as e:
        # Silenciar errores de archivo para no interrumpir la experiencia
        pass

    st.rerun()

# ==================== FOOTER CORPORATIVO ====================
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco  © 2025
</div>
""", unsafe_allow_html=True)

# ==================== INYECCIÓN FINAL DE JAVASCRIPT ====================
st.markdown("""
<script>
// EJECUCIÓN FINAL PARA GARANTIZAR ELIMINACIÓN
setTimeout(() => {
    // Eliminación final de cualquier elemento residual
    const elementos = document.querySelectorAll('img, svg, [class*="avatar"], [data-testid*="avatar"]');
    elementos.forEach(el => {
        el.remove();
        el.style.display = 'none';
    });
    
    // Forzar eliminación de contenedores
    document.querySelectorAll('div').forEach(div => {
        if (div.innerHTML.includes('avatar') || div.innerHTML.includes('crown')) {
            div.remove();
        }
    });
}, 3000);
</script>
""", unsafe_allow_html=True)
