st.markdown("""
<style>
    /* ==================== OCULTAR CORONA ROJA (DEPLOY BUTTON / CROWN) ==================== */
    .stAppDeployButton { display: none !important; }
    button[data-testid="stDeployButton"], .stDeployButton { display: none !important; visibility: hidden !important; height: 0 !important; z-index: -1 !important; }
    [data-testid="stDeployButton"] { display: none !important; }

    /* ==================== OCULTAR LOGO GITHUB Y FOOTER ==================== */
    footer { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    div[class*="hosted"] { display: none !important; }
    a[href*="github.com"] { display: none !important; }
    /* Oculta también el texto "Hosted with Streamlit" si aparece */
    span:contains("Streamlit") { display: none !important; }

    /* ==================== OCULTAR AVATAR/IMAGEN EN INPUT DE CHAT ==================== */
    [data-testid="stChatInput"] > div:first-child { display: none !important; }
    [data-testid="stChatInput"] img, 
    [data-testid="stChatInput"] svg, 
    [data-testid="stChatInput"] [alt*="avatar"],
    [data-testid="stChatInput"] [data-testid="stAvatar"] { 
        display: none !important; 
        visibility: hidden !important; 
        width: 0 !important; 
        height: 0 !important; 
        opacity: 0 !important;
    }

    /* ==================== OCULTAR AVATARES EN MENSAJES DEL CHAT ==================== */
    [data-testid="stChatMessage"] img, 
    [data-testid="stChatMessage"] svg, 
    [data-testid="stAvatar"], 
    [data-testid="stChatMessage"] [data-testid="stAvatar"] { 
        display: none !important; 
        visibility: hidden !important; 
        width: 0 !important; 
        height: 0 !important; 
    }

    /* ==================== LAYOUT SIMÉTRICO RESPONSIVO ==================== */
    .main .block-container { 
        max-width: 800px !important; 
        margin: 0 auto !important; 
        padding: 1rem !important; 
        width: auto !important; 
    }
    @media (max-width: 768px) {
        .main .block-container { 
            width: 95% !important; 
            padding: 0.5rem !important; 
        }
        [data-testid="stChatInput"] { 
            max-width: 100% !important; 
            margin: 0 auto !important; 
            padding-bottom: 2rem !important; 
        }
    }
    .stApp { background-color: #0e1117 !important; }

    /* ==================== ESTILOS MENSAJES SIMÉTRICOS ==================== */
    [data-testid="stChatMessage"] { padding: 0 !important; gap: 0 !important; }
    .user-message { 
        background: #262730 !important; 
        color: white !important; 
        border-radius: 18px !important; 
        padding: 14px 20px !important; 
        margin: 16px 8% 16px auto !important; 
        max-width: 75% !important; 
        box-shadow: 0 2px 10px rgba(0,0,0,0.4) !important;
    }
    .assistant-message { 
        background: linear-gradient(135deg, #ea580c, #f97316) !important; 
        color: white !important; 
        border-radius: 18px !important; 
        padding: 14px 20px !important; 
        margin: 16px auto 16px 8% !important; 
        max-width: 75% !important; 
        box-shadow: 0 4px 15px rgba(249,115,22,0.5) !important;
    }
    @media (max-width: 768px) { 
        .user-message, .assistant-message { 
            max-width: 90% !important; 
            padding: 12px 16px !important; 
            margin: 12px 4% 12px auto !important; 
        } 
    }

    /* ==================== HEADER ==================== */
    .header-box { 
        background: linear-gradient(90deg, #ea580c, #c2410c) !important; 
        padding: 2rem !important; 
        border-radius: 20px !important; 
        text-align: center !important; 
        color: white !important; 
        box-shadow: 0 10px 30px rgba(234,88,12,0.4) !important; 
        margin: 0 auto !important; 
    }
    @media (max-width: 768px) { 
        .header-box { padding: 1.5rem !important; } 
    }

    /* ==================== BELÉN BOX (SI LO NECESITAS) ==================== */
    .belén-box { 
        background: #dc2626 !important; 
        color: white !important; 
        padding: 1.3rem !important; 
        border-radius: 15px !important; 
        text-align: center !important; 
    }

    /* ==================== EXTRA: OCULTAR BOTÓN DE "FORK" O "GITHUB" SI APARECE ==================== */
    [data-testid="stGitHubButton"] { display: none !important; }
    button[aria-label="Fork this app"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }

</style>
""", unsafe_allow_html=True)
