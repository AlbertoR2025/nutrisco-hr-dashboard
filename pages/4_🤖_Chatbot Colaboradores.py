# app_simple.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Chat Nutrisco", layout="centered")

st.title("💬 Chatbot Nutrisco")
st.write("**Atención a Personas**")

# Historial de chat
if "chat" not in st.session_state:
    st.session_state.chat = []

# Mostrar historial
for mensaje in st.session_state.chat:
    if mensaje["rol"] == "usuario":
        st.write(f"**Tú:** {mensaje['texto']}")
    else:
        st.write(f"**Asistente:** {mensaje['texto']}")

# Input
pregunta = st.text_input("Escribe tu pregunta:")

if pregunta:
    # Agregar pregunta al historial
    st.session_state.chat.append({"rol": "usuario", "texto": pregunta})
    
    # Obtener respuesta
    try:
        respuesta = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": pregunta}],
                "temperature": 0.7
            }
        ).json()["choices"][0]["message"]["content"]
    except:
        respuesta = "Contacta a belen.bastias@nutrisco.com"
    
    # Agregar respuesta al historial
    st.session_state.chat.append({"rol": "asistente", "texto": respuesta})
    
    # Recargar
    st.rerun()

st.write("---")
st.write("Inteligencia Artificial al servicio de las personas – Nutrisco © 2025")
