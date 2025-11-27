# pages/4_🤖_Chatbot Colaboradores.py → VERSIÓN FINAL 2025: SIN FOTO/CORONA, SIMÉTRICO DESKTOP/MÓVIL (FIX V1.38 DISCUSS #80477)
import streamlit as st
import pandas as pd
import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# ==================== CONFIGURACIÓN GLOBAL ====================
st.set_page_config(
    page_title="Chatbot Colaboradores – Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"  # Hamburguesa visible para volver atrás
)

# ==================== CSS DEFINITIVO 2025 (DE DISCUSS #80477 – .stAppDeployButton PARA CORONA) ====================
st.markdown("""
<style>
    /* OCULTAR CORONA ROJA (DEPLOY BUTTON V1.38+ - DE DISCUSS #80477) */
    .stAppDeployButton {visibility: hidden !important; display: none !important;}
    button[data-testid="stDeployButton"], .stDeployButton {display: none !important; visibility: hidden !important; height: 0 !important; z-index: -1 !important;}

    /* OCULTAR HOSTED FOOTER Y LOGO GITHUB (DE FOROS NOV 2025) */
    footer, [data-testid="stStatusWidget"], div[class*="hosted"], div:contains("Streamlit") {display: none !important; visibility: hidden !important; height: 0 !important;}
    a[href*="github.com"] {display: none !important;}  /* Oculta logo GitHub/fork */

    /* OCULTAR FOTO/AVATAR/CUADRADO EN INPUT (FIX #12132 MÓVIL - CONTENEDOR PRIMERO) */
    [data-testid="stChatInput"] > div:first-child {display: none !important;}  /* Oculta el contenedor del avatar */
    [data-testid="stChatInput"] img, [data-testid="stChatInput"] svg, [data-testid="stChatInput"] [alt*="avatar"] {display: none !important; visibility: hidden !important; width: 0 !important; height: 0 !important; opacity: 0 !important;}

    /* OCULTAR AVATARES EN MENSAJES */
    [data-testid="stChatMessage"] img, [data-testid="stChatMessage"] svg, [data-testid="stAvatar"] {display: none !important; visibility: hidden !important; width: 0 !important; height: 0 !important;}

    /* LAYOUT SIMÉTRICO RESPONSIVO (SIN DESCUADRADO – MEDIA QUERIES NOV 2025) */
    .main .block-container {max-width: 800px !important; margin: 0 auto !important; padding: 1rem !important; width: auto !important;}
    @media (max-width: 768px) {
        .main .block-container {width: 95% !important; padding: 0.5rem !important;}
        [data-testid="stChatInput"] {max-width: 100% !important; margin: 0 auto !important; padding-bottom: 2rem !important;}
    }
    .stApp {background-color: #0e1117 !important;}

    /* ESTILOS MENSAJES SIMÉTRICOS (MARGIN IGUAL IZQUIERDA/DERECHA) */
    [data-testid="stChatMessage"] {padding: 0 !important; gap: 0 !important;}
    .user-message {background: #262730 !important; color: white !important; border-radius: 18px !important; padding: 14px 20px !important; margin: 16px 8% 16px auto !important; max-width: 75% !important; box-shadow: 0 2px 10px rgba(0,0,0,0.4) !important;}
    .assistant-message {background: linear-gradient(135deg, #ea580c, #f97316) !important; color: white !important; border-radius: 18px !important; padding: 14px 20px !important; margin: 16px auto 16px 8% !important; max-width: 75% !important; box-shadow: 0 4px 15px rgba(249,115,22,0.5) !important;}
    @media (max-width: 768px) {.user-message, .assistant-message {max-width: 90% !important; padding: 12px 16px !important; margin: 12px 4% 12px auto !important;}}  /* Simétrico en móvil */
    .header-box {background: linear-gradient(90deg, #ea580c, #c2410c) !important; padding: 2rem !important; border-radius: 20px !important; text-align: center !important; color: white !important; box-shadow
