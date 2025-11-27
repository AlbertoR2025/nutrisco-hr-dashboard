# pages/4_🤖_Chatbot Colaboradores.py → 100% LIMPIO – FUNCIONA EN TODOS LOS MÓVILES (27 NOV 2025)
import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Chatbot Nutrisco", page_icon="💬", layout="centered")

# OCULTA TODO LO DE STREAMLIT Y LA FOTO/CORONA
st.markdown("""
<style>
    header, footer, [data-testid="stToolbar"], [data-testid="stDeployButton"], 
    .stDeployButton, [data-testid="stStatusWidget"], a[href*="github"], 
    a[href*="streamlit"], [data-testid="stChatInput"] img, 
    [data-testid="stChatInput"] svg {display:none!important;}
    .stApp {background:#0e1117;}
    .block-container {max-width:900px;padding:1rem;}
    .header{background:linear-gradient(90deg,#ea580c,#c2410c);padding:2rem;border-radius:20px;text-align:center;color:white;}
    .user{background:#262730;color:white;border-radius:18px;padding:14px 20px;margin:12px 10% 12px auto;max-width:75%;}
    .bot{background:linear-gradient(135deg,#ea580c,#f97316);color:white;border-radius:18px;padding:14px 20px;margin:12px auto 12px 10%;max-width:75%;}
    .footer{text-align:center;margin-top:4rem;color:#64748b;padding-bottom:120px;}
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

# INPUT FIJO ABAJO SIN NADA DE STREAMLIT
st.markdown("""
<div style="position:fixed;bottom:0;left:0;width:100%;background:#0e1117;padding:15px;box-sizing:border-box;z-index:1000;">
    <input type="text" placeholder="Escribe tu consulta aquí..." id="msg" style="width:100%;padding:16px 20px;border-radius:30px;border:none;background:#1f2937;color:white;font-size:1.1rem;" autofocus>
</div>
<script>
    const input = document.getElementById('msg');
    input.focus();
    input.addEventListener("keydown", function(e){
        if(e.key === "Enter" && input.value.trim()){
            location.href = location.pathname + "?q=" + encodeURIComponent(input.value.trim());
        }
    });
</script>
""", unsafe_allow_html=True)

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
        resp = "Problema de conexión. Escribe a belen.bastias@nutrisco.com"

    st.markdown(f'<div class="bot">{resp}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role":"bot","content":resp})
    st.experimental_set_query_params()
    st.rerun()

st.stop()
st.markdown('<div class="footer"><br>Inteligencia Artificial al servicio de las personas – Nutrisco © 2025</div>', unsafe_allow_html=True)
