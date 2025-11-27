js_code = """
<script>
document.addEventListener("DOMContentLoaded", function() {

    // Ocultar botón de deploy (corona)
    const crownSelectors = [
        '[data-testid="stDeployButton"]',
        '[data-testid="stAppDeployButton"]',
        '.stAppDeployButton',
        '.stDeployButton',
        'button[title="Manage app"]'
    ];
    crownSelectors.forEach(sel => {
        const el = document.querySelector(sel);
        if (el) { el.style.display = "none"; el.style.visibility = "hidden"; }
    });

    // Ocultar avatar del INPUT del chat
    const intervalInput = setInterval(() => {
        const avatarInput = document.querySelector('[data-testid="stChatInput"] img');
        if (avatarInput) {
            avatarInput.remove();
            clearInterval(intervalInput);
        }
    }, 200);

    // Ocultar contenedor del avatar del input
    const intervalContainer = setInterval(() => {
        const avatarContainer = document.querySelector('[data-testid="stChatInput"] div div div');
        if (avatarContainer) {
            avatarContainer.style.display = "none";
            clearInterval(intervalContainer);
        }
    }, 200);

    // Ocultar todos los avatares dentro de los mensajes
    const observer = new MutationObserver(() => {
        document.querySelectorAll('[data-testid="stChatMessage"] img, [data-testid="stChatMessage"] svg').forEach(el => {
            el.style.display = "none";
            el.style.visibility = "hidden";
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });

});
</script>
"""
