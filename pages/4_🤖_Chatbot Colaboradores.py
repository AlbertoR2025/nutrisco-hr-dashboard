# ==== CSS + JS DEFINITIVO 2025 ====

css_js = """
<style>
/* ============================================
   1) OCULTAR CORONA (BOTÓN DEPLOY)
============================================ */
button[kind="header"], 
button[title="Manage app"],
[data-testid="stStatusWidget"],
[data-testid="stToolbar"],
.stAppDeployButton,
.stDeployButton,
.st-emotion-cache-gi0tri,   /* iPhone */
.st-emotion-cache-12fmjuu   /* variación */
{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
}

/* ============================================
   2) OCULTAR AVATAR CHAT INPUT (TODAS VERSIONES)
============================================ */
[data-testid="stChatInput"] img,
[data-testid="stChatInput"] svg,
[data-testid="stChatInput"] div:has(img),
[data-testid="stChatInput"] div:has(svg) {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* ============================================
   3) OCULTAR AVATAR EN MENSAJES
============================================ */
[data-testid="stChatMessage"] img,
[data-testid="stChatMessage"] svg,
[data-testid="stChatMessage"] div:has(img),
[data-testid="stChatMessage"] div:has(svg) {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
}

/* ============================================
   4) EVITAR QUE SE OCULTE EL INPUT COMPLETO
============================================ */
[data-testid="stChatInput"] {
    display: flex !important;
    opacity: 1 !important;
}
</style>

<script>
// =====================
// ELIMINACIÓN DINÁMICA
// =====================
const hideStuff = () => {
    // Avatares mensajes
    document.querySelectorAll('[data-testid="stChatMessage"] img, [data-testid="stChatMessage"] svg')
        .forEach(el => el.remove());

    // Avatar input
    document.querySelectorAll('[data-testid="stChatInput"] img, [data-testid="stChatInput"] svg')
        .forEach(el => el.remove());

    // Corona deploy
    document.querySelectorAll(
        'button[kind="header"], button[title="Manage app"], .stAppDeployButton, .stDeployButton, [data-testid="stStatusWidget"], [data-testid="stToolbar"]'
    ).forEach(el => el.remove());
};

// Observador dinámico
const obs = new MutationObserver(hideStuff);
obs.observe(document.body, { childList: true, subtree: true });

// Corre una vez también
setTimeout(hideStuff, 300);
</script>
"""

st.markdown(css_js, unsafe_allow_html=True)
