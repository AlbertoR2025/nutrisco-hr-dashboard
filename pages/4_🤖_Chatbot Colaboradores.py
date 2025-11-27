import streamlit as st
import requests
import os

# Configuración MUY básica
st.set_page_config(page_title="Nutrisco Chat", layout="centered")

# Título simple
st.title("💬 Asistente Nutrisco")
st.write("**Atención a Personas**")

# Inicializar chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte?"}
    ]

# Mostrar historial SIMPLE
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.write(f"**Tú:** {msg['content']}")
    else:
        st.write(f"**Asistente:** {msg['content']}")

# Input simple
user_input = st.text_input("Escribe tu consulta:")

if user_input:
    # Agregar mensaje usuario
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Obtener respuesta
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": user_input}],
                "temperature": 0.7
            },
            timeout=30
        )
        respuesta = response.json()["choices"][0]["message"]["content"]
    except:
        respuesta = "Por favor contacta a belen.bastias@nutrisco.com"
    
    # Agregar respuesta
    st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
    
    # Recargar
    st.rerun()

# Footer simple
st.write("---")
st.write("Inteligencia Artificial al servicio de las personas – Nutrisco © 2025")
