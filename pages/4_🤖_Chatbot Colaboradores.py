import streamlit as st

st.set_page_config(
    page_title="Chatbot Colaboradores – Nutrisco",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==== CSS + JS: OCULTAR CORONA, AVATARES Y CHAT INPUT NATIVO ====
css_js = """
<style>
/* Ocultar corona / deploy / toolbar / footer */
header, footer, [data-testid="stToolbar"],
[data-testid="stDeployButton"], .stAppDeployButton,
button[title*="Deploy"], button[title*="View"],
[data-testid="baseButton-secondary"] {
    display: none !important;
    visibility: hidden !important;
}

/* Ocultar avatares en mensajes e input */
[data-testid="stChatMessage"] [data-testid="stAvatar"],
[data-testid="stChatMessage"] img,
[data-testid="stChatMessage"] svg,
[data-testid="stChatInput"] [data-testid="stAvatar"],
[data-testid="stChatInput"] img,
[data-testid="stChatInput"] svg {
    display: none !important;
    visibility: hidden !important;
}

/* Forzar que el chat_input nativo NO quede tapado */
[data-testid="stChatInput"] {
    z-index: 1000 !important;
}

/* Layout general */
.main .block-container {
    max-width: 800px !important;
    margin: 0 auto !important;
    padding: 1rem 1rem 6rem 1rem !important; /* espacio abajo para input */
}
.stApp {
    background-color: #0e1117 !important;
}
</style>

<script>
// Eliminar restos de botones de deploy al cargar
document.addEventListener("DOMContentLoaded", function() {
    const selectors = [
        '[data-testid="stDeployButton"]',
        '.stAppDeployButton',
        'button[title*="Deploy"]',
        'button[title*="View"]'
    ];
    selectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(el => {
            el.style.display = "none";
            el.style.visibility = "hidden";
        });
    });
});
</script>
"""
st.markdown(css_js, unsafe_allow_html=True)
