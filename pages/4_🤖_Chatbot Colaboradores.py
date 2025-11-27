# ==== CSS FINAL STREAMLIT CLOUD (solo CSS, 100% permitido) ====
css_cloud = """
<style>
/* Quitar avatar del input */
[data-testid="stChatInput"] img,
[data-testid="stChatInput"] svg {
    display: none !important;
    visibility: hidden !important;
}

/* Quitar contenedor del avatar en input */
[data-testid="stChatInput"] > div > div:nth-child(1) {
    display: none !important;
}

/* Quitar avatar de los mensajes */
[data-testid="stChatMessage"] img,
[data-testid="stChatMessage"] svg {
    display: none !important;
}

/* Quitar contenedor/avatar en cada mensaje */
[data-testid="stChatMessage"] > div:nth-child(1) {
    display: none !important;
}
</style>
"""

st.markdown(css_cloud, unsafe_allow_html=True)
