# pages/3_Resumen Automático IA.py → VERSIÓN FINAL 100% PROFESIONAL (26-nov-2025)
import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# ================================================
# VERIFICAR DATOS
# ================================================
if 'df' not in st.session_state or st.session_state.df is None:
    st.error("Ve al **Panel de Control** primero para cargar los datos.")
    st.stop()

df = st.session_state.df.copy()
API_KEY = os.getenv("OPENAI_API_KEY")

# ================================================
# ESTILO FINAL NUTRISCO
# ================================================
st.markdown("""
<style>
    .main {background-color: #0f172a; color: white;}
    .header-resumen {
        background: linear-gradient(90deg, #ea580c, #f97316);
        padding: 2.2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 12px 35px rgba(234, 88, 12, 0.45);
    }
    .input-card {
        background: #1e293b;
        padding: 2rem;
        border-radius: 18px;
        border: 1px solid #334155;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        margin-bottom: 2rem;
    }
    .stTextArea > div > div > textarea {
        background-color: #334155 !important;
        color: white !important;
        border-radius: 14px;
        font-size: 1.1rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #ea580c, #f97316);
        color: white;
        font-weight: bold;
        border-radius: 14px;
        padding: 1rem 3rem;
        border: none;
        box-shadow: 0 6px 20px rgba(234,88,12,0.5);
        font-size: 1.1rem;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #f97316, #ea580c);
        transform: translateY(-3px);
    }
    .response-box {
        background: #1e293b;
        padding: 2rem;
        border-radius: 18px;
        border-left: 6px solid #f97316;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        margin-top: 2rem;
    }
    .footer {text-align: center; margin-top: 8rem; color: #64748b; font-size: 0.9rem;}
</style>
""", unsafe_allow_html=True)

# ==================== CABECERA LIMPIA Y ELEGANTE ====================
st.markdown("""
<div class="header-resumen">
    <h1 style="margin:0; color:white; font-size:3.6rem; font-weight:800;">
        Resumen Automático IA
    </h1>
    <p style="margin:14px 0 0 0; color:#fff; font-size:1.6rem; font-weight:300;">
        Pregunta en lenguaje natural y la IA analiza todo el historial de consultas
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== INPUT + BOTÓN ====================
with st.container():
    st.markdown("<div class='input-card'>", unsafe_allow_html=True)
    
    pregunta = st.text_area(
        "",
        placeholder="Ejemplos:\n• ¿Existe algún punto de dolor recurrente?\n• ¿Qué gerencia genera más consultas?\n• Resumen ejecutivo del último mes\n• ¿Cuáles son los 5 temas más consultados?\n• ¿Hay colaboradores con alta recurrencia?",
        height=200,
        label_visibility="collapsed"
    )
    
    generar = st.button("Generar Resumen", type="primary", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== GENERAR RESUMEN (SIN MENSAJE VERDE) ====================
if generar and pregunta.strip():
    with st.spinner("Analizando todo el historial con inteligencia artificial..."):
        try:
            datos = df[['Consulta', 'Categoria_Consulta', 'Nombre Gerencia', 'Respuesta', 'Estado_Normalizado', 'Nombre ']].fillna('').astype(str)
            datos_limpios = datos.head(300).to_dict(orient='records')
            
            contexto = f"""
            Eres un analista senior de RR.HH. de Nutrisco (Chile).
            Tienes acceso completo a {len(df):,} consultas reales.
            Aquí tienes los primeros 300 registros para análisis:
            {datos_limpios}
            
            Responde en español, ejecutivo, claro y con datos concretos.
            Usa viñetas y recomendaciones estratégicas.
            """

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": contexto},
                        {"role": "user", "content": pregunta}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1200
                },
                timeout=60
            )
            respuesta = response.json()["choices"][0]["message"]["content"]
            
            # Mostrar respuesta directamente (sin "Resumen generado exitosamente")
            st.markdown("<div class='response-box'>", unsafe_allow_html=True)
            st.markdown(f"### Análisis IA:\n{respuesta}")
            st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error("Error temporal al conectar con la IA. Inténtalo en unos segundos.")

elif generar and not pregunta.strip():
    st.warning("Por favor escribe una pregunta antes de generar el resumen.")

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco  © 2025
</div>
""", unsafe_allow_html=True)
