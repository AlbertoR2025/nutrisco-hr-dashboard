# app_ultra_simple.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Nutrisco Chat", layout="centered")

# CSS mínimo
st.markdown("""
<style>header, footer, [data-testid="stToolbar"] {display:none;}</style>
""", unsafe_allow_html=True)

st.title("💬 Asistente Nutrisco")
st.write("Hola! ¿En qué puedo ayudarte?")

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    st.write(f"**{'Tú' if msg['role']=='user' else 'Asistente'}:** {msg['content']}")

pregunta = st.text_input("Escribe aquí...")

if pregunta:
    st.session_state.history.append({"role": "user", "content": pregunta})
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": pregunta}],
                "temperature": 0.7
            }
        )
        respuesta = response.json()["choices"][0]["message"]["content"]
    except:
        respuesta = "Contacta a belen.bastias@nutrisco.com"
    
    st.session_state.history.append({"role": "assistant", "content": respuesta})
    st.rerun()

st.write("---")
st.write("Inteligencia Artificial al servicio de las personas – Nutrisco © 2025")
