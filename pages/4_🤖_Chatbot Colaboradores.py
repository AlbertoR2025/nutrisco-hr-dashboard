st.markdown("""
<style>
.fixed-input {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(15,23,42,0.96);
    padding: 14px 10px 18px 10px;
    box-sizing: border-box;
    z-index: 1000;
    border-top: 1px solid #1f2937;
    backdrop-filter: blur(8px);
    display: flex;
    justify-content: center;
    align-items: center;
}
.input-container {
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    gap: 12px;
    align-items: center;
    width: 100%;
    padding: 0 10px;
}
.text-input {
    flex: 1;
    padding: 14px 20px;
    border-radius: 999px;
    border: 1px solid #374151;
    background: radial-gradient(circle at top left,#111827,#020617);
    color: #e5e7eb;
    font-size: 1.05rem;
    outline: none;
    transition: all 0.25s ease;
    box-shadow: inset 0 0 0 1px rgba(15,23,42,0.9);
}
.text-input::placeholder {color:#6b7280;}
.text-input:focus {
    border-color: #f97316;
    box-shadow:
        0 0 0 1px rgba(249,115,22,0.7),
        0 0 18px rgba(249,115,22,0.35);
}
.send-btn-wrapper {
    width: 72px;
    height: 46px;
    position: relative;
}
.send-btn-visible {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 30% 30%,#facc15,#ea580c);
    color: white;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 6px 18px rgba(234,88,12,0.55);
    cursor: pointer;
    transition: all 0.2s ease;
}
.send-btn-visible:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 26px rgba(234,88,12,0.8);
}
.send-btn-visible:active {
    transform: translateY(1px) scale(0.98);
    box-shadow: 0 4px 12px rgba(234,88,12,0.6);
}
@media (max-width: 768px) {
    .text-input {padding: 11px 16px;font-size:0.98rem;}
    .send-btn-wrapper {width: 62px;height: 42px;}
}
</style>
""", unsafe_allow_html=True)
