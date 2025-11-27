# Panel de Control.py → VERSIÓN FINAL 100% FUNCIONAL EN LA NUBE (26-nov-2025)
import streamlit as st
import pandas as pd
import plotly.express as px

# IMPORTS LIMPIOS (sin importlib.reload
from utils.data_loader import load_data
from utils.kpi_calculator import calculate_kpis

st.set_page_config(
    page_title="Nutrisco - Inteligencia RR.HH.",
    page_icon="circle",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILO NUTRISCO ====================
st.markdown("""
<style>
    .main {background-color: #0f172a; color: white;}
    .header-section {
        background: linear-gradient(90deg, #ea580c, #f97316);
        padding: 1.3rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 25px rgba(234,88,12,0.35);
    }
    .kpi-card {
        background: #1e293b;
        padding: 1.8rem 1rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-card:hover {transform: translateY(-5px); transition: 0.2s;}
    .metric-label {font-size: 1rem; color: #94a3b8;}
    .metric-value {font-size: 3rem; font-weight: bold; color: #f97316;}
    .section-title {color: #f97316; font-size: 1.9rem; margin: 2.5rem 0 1rem;}
</style>
""", unsafe_allow_html=True)

# ==================== CABECERA ====================
st.markdown("""
<div class="header-section">
    <h1 style="margin:0; color:white; font-size:3.2rem; font-weight:800;">nutrisco.</h1>
    <p style="margin:8px 0 0 0; color:#fff; font-size:1.4rem; font-weight:300;">
        Dashboard Ejecutivo • Atención a Personas
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== CARGA DE DATOS ====================
@st.cache_data(ttl=3600)
def get_data():
    return load_data()

df = get_data()
if df is None:
    st.error("No se pudo cargar el archivo.")
    st.info("Asegúrate de que esté en la carpeta **data/**")
    st.stop()

st.session_state.df = df

# ==================== KPIs ====================
try:
    kpis = calculate_kpis(df)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="kpi-card"><div class="metric-label">Total Consultas</div><div class="metric-value">{kpis["total_consultas"]:,}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card"><div class="metric-label">Consultas Urgentes</div><div class="metric-value">{kpis["urgentes"]}</div></div>', unsafe_allow_html=True)
    with c3:
        color = "#10b981" if kpis["trpc"] >= 70 else "#f87171"
        st.markdown(f'<div class="kpi-card"><div class="metric-label">Resolución 1er Contacto</div><div class="metric-value">{kpis["trpc"]:.1f}%</div><div style="color:{color}">Meta >70%</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="kpi-card"><div class="metric-label">Tasa Derivación</div><div class="metric-value">{kpis["tasa_derivacion"]:.1f}%</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([1.7, 1.3])
    with col1:
        st.markdown("<h3 class='section-title'>Top 5 Temas Más Recurrentes</h3>", unsafe_allow_html=True)
        top = kpis['top_categorias'].copy()
        top['Categoría'] = top['Categoría'].replace('Otro', 'Consulta General')
        st.dataframe(top, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("<h3 class='section-title'>Distribución por Área</h3>", unsafe_allow_html=True)
        fig = px.pie(kpis['distribucion_area'], values='Frecuencia', names='Área', hole=0.5,
                     color_discrete_sequence=px.colors.sequential.Oranges)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("<h3 class='section-title'>Colaboradores con Más Consultas</h3>", unsafe_allow_html=True)
    st.dataframe(kpis['ranking_empleados'].head(10), use_container_width=True, hide_index=True)

    st.markdown("<h3 class='section-title'>Últimas 10 Consultas</h3>", unsafe_allow_html=True)
    ult = df.copy()
    ult['Fecha '] = pd.to_datetime(ult['Fecha '], errors='coerce')
    ult = ult.sort_values('Fecha ', ascending=False).head(10)
    ult['Colaborador'] = ult['Nombre '].fillna('').astype(str).str.strip()
    ult = ult[ult['Colaborador'].str.len() > 0]
    ult['Tema'] = ult['Categoria_Consulta'].fillna('Sin categoría').replace('Otro', 'Consulta General')
    ult['Estado'] = ult['Estado_Normalizado'].fillna('Pendiente')
    ult['Fecha'] = ult['Fecha '].dt.strftime('%d/%m/%Y')
    st.dataframe(ult[['Fecha', 'Colaborador', 'Tema', 'Estado']], use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Error: {e}")

# ==================== FOOTER ====================
st.markdown("""
<div class="footer">
    <br>
    Inteligencia Artificial al servicio de las personas – Nutrisco  © 2025
</div>
""", unsafe_allow_html=True)
