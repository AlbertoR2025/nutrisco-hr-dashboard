# Panel de Control.py → VERSIÓN FINAL 100% PERFECTA (26-nov-2025)
import streamlit as st
import pandas as pd
import plotly.express as px
import importlib

# --------------------------------------------------------------
import utils.data_loader
importlib.reload(utils.data_loader)
from utils.data_loader import load_data
# --------------------------------------------------------------

st.set_page_config(
    page_title="Nutrisco - Inteligencia RR.HH.",
    page_icon="orange_circle",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILO FINAL IMPECABLE ====================
st.markdown("""
<style>
    .main {background-color: #0f172a; color: white;}
    .header-section {
        background: linear-gradient(90deg, #ea580c, #f97316);
        padding: 1.3rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 25px rgba(234, 88, 12, 0.35);
    }
    /* TODAS LAS TARJETAS KPIs DEL MISMO TAMAÑO */
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
    .metric-label {font-size: 1rem; color: #94a3b8; margin-bottom: 0.5rem;}
    .metric-value {font-size: 3rem; font-weight: bold; color: #f97316; margin: 0.4rem 0;}
    .metric-delta {font-size: 0.95rem; font-weight: bold;}
    .section-title {color: #f97316; font-size: 1.9rem; margin: 2.5rem 0 1rem; font-weight: 600;}
    .footer {text-align: center; margin-top: 6rem; color: #64748b; font-size: 0.9rem;}
</style>
""", unsafe_allow_html=True)

# ==================== CABECERA ELEGANTE ====================
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
    st.info("Asegúrate de que el archivo esté en la carpeta **data/**")
    st.stop()

st.session_state.df = df

# ==================== KPIs (TODAS IGUALES) ====================
try:
    from utils.kpi_calculator import calculate_kpis
    kpis = calculate_kpis(df)

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-label">Total Consultas</div>
            <div class="metric-value">{kpis['total_consultas']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-label">Consultas Urgentes</div>
            <div class="metric-value">{kpis['urgentes']}</div>
            <div class="metric-delta" style="color:#f87171;">Prioridad alta</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        color = "#10b981" if kpis['trpc'] >= 70 else "#f87171"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-label">Resolución Primer Contacto</div>
            <div class="metric-value">{kpis['trpc']:.1f}%</div>
            <div class="metric-delta" style="color:{color}">Meta >70%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="metric-label">Tasa de Derivación</div>
            <div class="metric-value">{kpis['tasa_derivacion']:.1f}%</div>
            <div class="metric-delta" style="color:#34d399;">Menor es mejor</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ==================== TOP TEMAS + ÁREA ====================
    col1, col2 = st.columns([1.7, 1.3])
    with col1:
        st.markdown("<h3 class='section-title'>Top 5 Temas Más Recurrentes</h3>", unsafe_allow_html=True)
        top_df = kpis['top_categorias'].copy()
        top_df['Categoría'] = top_df['Categoría'].replace('Otro', 'Consulta General')
        st.dataframe(top_df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("<h3 class='section-title'>Distribución por Área</h3>", unsafe_allow_html=True)
        fig = px.pie(kpis['distribucion_area'], values='Frecuencia', names='Área',
                     hole=0.5, color_discrete_sequence=px.colors.sequential.Oranges)
        fig.update_layout(showlegend=False, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ==================== RANKING ====================
    st.markdown("<h3 class='section-title'>Colaboradores con Más Consultas</h3>", unsafe_allow_html=True)
    st.dataframe(kpis['ranking_empleados'].head(10), use_container_width=True, hide_index=True)

            # ==================== ÚLTIMAS 10 CONSULTAS (100% LIMPIAS Y PROFESIONALES) ====================
    st.markdown("<h3 class='section-title'>Últimas 10 Consultas Recibidas</h3>", unsafe_allow_html=True)
    
    ultimas = df.copy()
    ultimas['Fecha '] = pd.to_datetime(ultimas['Fecha '], errors='coerce')
    ultimas = ultimas.sort_values('Fecha ', ascending=False).head(10)

    # LIMPIEZA TOTAL Y DEFINITIVA DEL NOMBRE
    def limpiar_nombre(nombre):
        if pd.isna(nombre):
            return ""
        texto = str(nombre).strip()
        if texto in ['', 'nan', 'None', '<NA>', 'Usuario Externo', 'Consulta Externa']:
            return ""
        return texto

    ultimas['Colaborador'] = ultimas['Nombre '].apply(limpiar_nombre)

    # Tema y Estado
    ultimas['Tema'] = ultimas['Categoria_Consulta'].fillna('Sin categoría').replace('Otro', 'Consulta General')
    ultimas['Estado'] = ultimas['Estado_Normalizado'].fillna('Pendiente')
    ultimas['Fecha'] = ultimas['Fecha '].dt.strftime('%d/%m/%Y')

    # Tabla final
    tabla = ultimas[['Fecha', 'Colaborador', 'Tema', 'Estado']].copy()

    # OPCIONAL: ocultar filas sin colaborador (recomendado para que quede súper limpio)
    tabla = tabla[tabla['Colaborador'] != ""]

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Colaborador": st.column_config.TextColumn(width="large"),
            "Tema": st.column_config.TextColumn(width="medium"),
            "Estado": st.column_config.TextColumn(width="small")
        }
    )

    # ==================== FOOTER ====================
    # Footer limpio y corporativo (solo Nutrisco)
st.markdown("""
<div class="footer">
    <p style="margin:0; font-size:0.95rem; color:#94a3b8;">
        Inteligencia Artificial al servicio de las personas – Nutrisco
    </p>
</div>
""", unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error: {e}")
