# pages/2_Tendencias y Gráficos.py → VERSIÓN FINAL NUTRISCO (26-nov-2025)
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ================================================
# VERIFICAR DATOS
# ================================================
if 'df' not in st.session_state or st.session_state.df is None:
    st.error("Ve al **Panel de Control** primero para cargar los datos.")
    st.stop()

df = st.session_state.df.copy()

# ================================================
# ESTILO CORPORATIVO NUTRISCO (SIN LOGO)
# ================================================
st.markdown("""
<style>
    .main {background-color: #0f172a; color: white;}
    .header-tendencias {
        background: linear-gradient(90deg, #ea580c, #f97316);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 8px 25px rgba(234, 88, 12, 0.35);
    }
    .section-title {
        color: #f97316;
        font-size: 2rem;
        margin: 3rem 0 1.5rem;
        font-weight: 600;
        text-align: center;
    }
    .chart-card {
        background: #1e293b;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .footer {text-align: center; margin-top: 6rem; color: #64748b; font-size: 0.9rem;}
</style>
""", unsafe_allow_html=True)

# ==================== CABECERA ELEGANTE (SIN LOGO) ====================
st.markdown("""
<div class="header-tendencias">
    <h1 style="margin:0; color:white; font-size:3.4rem; font-weight:800;">
        Análisis de Tendencias y Gráficos
    </h1>
    <p style="margin:10px 0 0 0; color:#fff; font-size:1.4rem; font-weight:300;">
        Volumen, categorías y comportamiento de consultas en el tiempo
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== GRÁFICO 1: TENDENCIA POR DÍA ====================
st.markdown("<h3 class='section-title'>Volumen de Consultas por Día</h3>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    
    df['Día'] = pd.to_datetime(df['Fecha '], errors='coerce').dt.normalize()
    consultas_diarias = df.groupby('Día').size().reset_index(name='Consultas')
    
    fig_line = px.line(
        consultas_diarias,
        x='Día',
        y='Consultas',
        markers=True,
        color_discrete_sequence=["#f97316"],
        height=500
    )
    fig_line.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Fecha",
        yaxis_title="Número de Consultas",
        font=dict(color="white")
    )
    fig_line.update_traces(line=dict(width=4), marker=dict(size=8))
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== GRÁFICO 2: DISTRIBUCIÓN POR CATEGORÍA ====================
st.markdown("<h3 class='section-title'>Distribución por Temas Más Consultados</h3>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    
    categoria_col = next((col for col in ['Categoria_Consulta', 'Categoría', 'Tema'] if col in df.columns), None)
    if categoria_col:
        top_categorias = df[categoria_col].value_counts().head(12).reset_index()
        top_categorias.columns = ['Categoría', 'Frecuencia']
        top_categorias['Categoría'] = top_categorias['Categoría'].replace('Otro', 'Consulta General')
        
        fig_bar = px.bar(
            top_categorias,
            x='Frecuencia',
            y='Categoría',
            orientation='h',
            color='Frecuencia',
            color_continuous_scale="Oranges",
            text='Frecuencia',
            height=560
        )
        fig_bar.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Número de Consultas",
            yaxis_title=None,
            font=dict(color="white")
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("No se encontró columna de categorías")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== FOOTER ====================
# Footer limpio y corporativo (solo Nutrisco)
st.markdown("""
<div class="footer">
    <p style="margin:0; font-size:0.95rem; color:#94a3b8;">
        Inteligencia Artificial al servicio de las personas – Nutrisco
    </p>
</div>
""", unsafe_allow_html=True)
