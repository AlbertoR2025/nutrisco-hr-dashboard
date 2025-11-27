# pages/4_🤖_Chatbot Colaboradores.py → 100% LIMPIO – FUNCIONA EN TODOS LOS MÓVILES Y PC – NOV 2025
import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Chatbot Nutrisco", page_icon="💬", layout="centered")

# === ELIMINA TODO LO DE STREAMLIT DE UNA VEZ ===
st.markdown("""
<style>
    header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"], 
    .stDeployButton, [data-testid="stStatusWidget"], a[href*="github"], a[href*="streamlit"] {display:none!important;}
    .stApp {background:#0e1117;}
    .block-container {max-width:900px;padding:1rem;}
    .header{background:linear-gradient(90deg,#ea580c,#c2410c);padding:2rem;border-radius:20px;text-align:center;color:white;margin-bottom:2rem;}
    .msg-user{background:#262730;color:white;border-radius:18px;padding:14px 20px;margin:10px 10% 10px auto;max-width:75%;box-shadow:0 2px 10px rgba(0,0,0,0.4);}
    .msg-bot{background:linear-gradient(135deg,#ea580c,#f97316);color:white;border-radius:18px;padding:14px 20px;margin:10px auto 10px 10%;max-width:75%;box-shadow:0 4px 15px rgba(249,115,22,0.5);}
    .footer{text-align:center;margin-top:3rem;color:#64748b;padding-bottom:100px;}
    .input-fixed{position:fixed;bottom:0;left:0;width:100%;background:#0e1117;padding:15px;box-sizing:border-box;z-index:1000;}
    .input-fixed input{width:100%;padding:16px 20px;border-radius:30px;border:none;background:#1f2937;color:white;font-size:1.1rem;}
    .input-fixed input:focus{outline:none;background:#374151;}
</style>
""", unsafe_allow_html=True)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("Falta OPENAI_API_KEY")
    st.stop()

# HEADER
st.markdown('<div class="header"><h1>Chatbot Colaboradores</h1><h2>Nutrisco – Atención Personas</h2><p>Escribe tu duda y te respondo al instante</p></div>', unsafe_allow_html=True)

# INICIALIZAR
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"bot","content":"¡Hola! Soy parte del equipo de **Atención a Personas** de Nutrisco.\n\nPuedes preguntarme cualquier cosa: licencias, beneficios, BUK, finiquitos, vestimenta, bono Fisherman, etc.\n\n¡Estoy aquí para ayudarte!"}]

# MOSTRAR CHAT
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg-bot">{msg["content"]}</div>', unsafe_allow_html=True)

# INPUT FIJO ABAJO (SIN FOTO NI CORONA)
st.markdown("""
<div class="input-fixed">
    <input type="text" placeholder="Escribe tu consulta aquí..." id="inputbox" autofocus>
</div>
<script>
    const input = document.getElementById('inputbox');
    input.focus();
    input.addEventListener("keydown", function(e){
        if(e.key === "Enter" && input.value.trim()){
            location.href = location.pathname + "?msg=" + encodeURIComponent(input.value.trim());
        }
    });
</script>
""", unsafe_allow_html=True)

# PROCESAR MENSAJE
msg = st.experimental_get_query_params().get("msg", [None])[0]
if msg:
    st.session_state.messages.append({"role":"user","content":msg})
    st.markdown(f'<div class="msg-user">{msg}</div>', unsafe_allow_html=True)
    
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization":f"Bearer {API_KEY}"},
            json={"model":"gpt-4o-mini","temperature":0.7,"max_tokens":600,
                  "messages":[{"role":"system","content":"Eres del equipo RRHH Nutrisco Chile. Hablas español chileno cercano y profesional."},
                              {"role":"user","content":msg}]})
        resp = r.json()["choices"][0]["message"]["content"]
    except:
        resp = "Problema de conexión. Escribe a belen.bastias@nutrisco.com"

    st.markdown(f'<div class="msg-bot">{resp}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role":"bot","content":resp})
    st.experimental_set_query_params()
    st.rerun()

# FOOTER
st.markdown('<div class="footer"><br>Inteligencia Artificial al servicio de las personas – Nutrisco © 2025</div>', unsafe_allow_html=True)
