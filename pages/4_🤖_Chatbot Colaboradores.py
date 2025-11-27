# pages/4_🤖_Chatbot Colaboradores.py → FUNCIONA 100% – SIN FOTO – SIN CORONA – SIMÉTRICO
import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Chatbot Nutrisco", page_icon="💬", layout="centered")

# ELIMINA TODO LO DE STREAMLIT
st.markdown("""
<style>
    header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"], 
    .stDeployButton, [data-testid="stStatusWidget"], a[href*="github"], 
    a[href*="streamlit"] {display:none!important;}
    .stApp {background:#0e1117;}
    .block-container {max-width:900px;padding:1rem;padding-bottom:100px;}
    .header{background:linear-gradient(90deg,#ea580c,#c2410c);padding:2.5rem;border-radius:20px;text-align:center;color:white;margin-bottom:2rem;}
    .user{background:#262730;color:white;border-radius:18px;padding:14px 20px;margin:12px 8% 12px auto;max-width:75%;box-shadow:0 2px 10px rgba(0,0,0,0.4);}
    .bot{background:linear-gradient(135deg,#ea580c,#f97316);color:white;border-radius:18px;padding:14px 20px;margin:12px auto 12px 8%;max-width:75%;box-shadow:0 4px 15px rgba(249,115,22,0.5);}
    .footer{text-align:center;margin-top:4rem;color:#64748b;font-size:0.95rem;}
</style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Falta OPENAI_API_KEY")
    st.stop()

st.markdown('<div class="header"><h1>Chatbot Colaboradores</h1><h2>Nutrisco – Atención Personas</h2><p>Escribe tu duda y te respondo al instante</p></div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"bot","content":"¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"}]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot">{msg["content"]}</div>', unsafe_allow_html=True)

# INPUT PERSONALIZADO CON BOTÓN ENVIAR
st.markdown("""
<div style="position:fixed;bottom:0;left:0;width:100%;background:#0e1117;padding:15px;box-sizing:border-box;z-index:1000;display:flex;justify-content:center;">
    <div style="width:90%;max-width:800px;display:flex;gap:10px;">
        <input type="text" id="msg" placeholder="Escribe tu consulta aquí..." style="flex:1;padding:16px 20px;border-radius:30px;border:none;background:#1f2937;color:white;font-size:1.1rem;" autofocus>
        <button onclick="send()" style="background:#ea580c;color:white;border:none;border-radius:50%;width:50px;height:50px;cursor:pointer;font-size:20px;">➤</button>
    </div>
</div>
<script>
function send() {
    const input = document.getElementById('msg');
    if (input.value.trim()) {
        location.href = location.pathname + "?q=" + encodeURIComponent(input.value.trim());
    }
}
document.getElementById('msg').addEventListener('keypress', e => { if (e.key === 'Enter') send(); });
</script>
""", unsafe_allow_html=True)

# PROCESAR MENSAJE
q = st.experimental_get_query_params().get("q", [None])[0]
if q:
    st.session_state.messages.append({"role":"user","content":q})
    st.markdown(f'<div class="user">{q}</div>', unsafe_allow_html=True)
    
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization":f"Bearer {API_KEY}"},
            json={"model":"gpt-4o-mini","temperature":0.7,"max_tokens":600,
                  "messages":[{"role":"system","content":"Eres del equipo RRHH Nutrisco Chile. Hablas español chileno cercano y profesional."},
                              {"role":"user","content":q}]})
        resp = r.json()["choices"][0]["message"]["content"]
    except:
        resp = "Problema de conexión."

    st.markdown(f'<div class="bot">{resp}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role":"bot","content":resp})
    st.experimental_set_query_params()
    st.rerun()

st.markdown('<div class="footer"><br>Inteligencia Artificial al servicio de las personas – Nutrisco © 2025</div>', unsafe_allow_html=True)
