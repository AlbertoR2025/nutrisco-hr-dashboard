# pages/1_KPIs Estratégicos.py → VERSIÓN FINAL DEFINITIVA (26-nov-2025)
import streamlit as st
import plotly.express as px

# ================================================
# VERIFICAR DATOS
# ================================================
if 'df' not in st.session_state or st.session_state.df is None:
    st.error("Ve al **Panel de Control** primero para cargar los datos.")
    st.stop()

df = st.session_state.df
from utils.kpi_calculator import calculate_kpis
kpis = calculate_kpis(df)

# ================================================
# ESTILO FINAL NUTRISCO (MISMA FRANJA QUE LAS DEMÁS PÁGINAS)
# ================================================
st.markdown("""
<style>
    .main {background-color: #0f172a; color: white;}
    .header-kpi {
        background: linear-gradient(90deg, #ea580c, #f97316);
        padding: 2.2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 12px 35px rgba(234, 88, 12, 0.45);
    }
    .kpi-card {
        background: #1e293b;
        padding: 2rem 1rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-card:hover {transform: translateY(-6px); transition: 0.2s;}
    .metric-label {font-size: 1.1rem; color: #94a3b8; margin-bottom: 0.8rem;}
    .metric-value {font-size: 3.2rem; font-weight: bold; color: #f97316; margin: 0.5rem 0;}
    .metric-delta {font-size: 1rem; font-weight: bold;}
    .section-title {color: #f97316; font-size: 2rem; margin: 3rem 0 1.5rem; font-weight: 600;}
    .footer {text-align: center; margin-top: 6rem; color: #64748b; font-size: 0.9rem;}
</style>
""", unsafe_allow_html=True)

# ==================== FRANJA NARANJA IGUAL QUE LAS DEMÁS ====================
st.markdown("""
<div class="header-kpi">
    <h1 style="margin:0; color:white; font-size:3.6rem; font-weight:800;">
        KPIs Estratégicos
    </h1>
    <p style="margin:14px 0 0 0; color:#fff; font-size:1.6rem; font-weight:300;">
        Métricas clave para la toma de decisiones ejecutivas
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== 4 KPIs PRINCIPALES ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="metric-label">Total Consultas Gestionadas</div>
        <div class="metric-value">{kpis['total_consultas']:,}</div>
        <div class="metric-delta" style="color:#34d399;">+0 vs mes anterior</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    color_trpc = "#10b981" if kpis['trpc'] >= 70 else "#f87171"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="metric-label">Resolución en Primer Contacto</div>
        <div class="metric-value">{kpis['trpc']:.1f}%</div>
        <div class="metric-delta" style="color:{color_trpc}">Meta >70%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="metric-label">Consultas Urgentes</div>
        <div class="metric-value">{kpis['urgentes']}</div>
        <div class="metric-delta" style="color:#f87171;">↓ reducción objetivo</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="metric-label">Tasa de Derivación</div>
        <div class="metric-value">{kpis['tasa_derivacion']:.1f}%</div>
        <div class="metric-delta" style="color:#34d399;">↓ menor es mejor</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================== TOP 10 + DONA + BARRAS HORIZONTALES ====================
col1, col2 = st.columns([1.6, 1.4])

with col1:
    st.markdown("<h3 class='section-title'>Top 10 Temas Más Recurrentes</h3>", unsafe_allow_html=True)
    top10 = kpis['top_categorias'].head(10).copy()
    top10['Categoría'] = top10['Categoría'].replace('Otro', 'Consulta General')
    
    fig = px.bar(top10, x='Frecuencia', y='Categoría', orientation='h',
                 color='Frecuencia', color_continuous_scale="Oranges",
                 text='Frecuencia', height=580)
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False,
                      xaxis_title="Número de consultas", yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("<h3 class='section-title'>Distribución por Área</h3>", unsafe_allow_html=True)
    
    area_col = next((c for c in ['Nombre Gerencia', 'Gerencia', 'Área'] if c in df.columns), 'Nombre Gerencia')
    distribucion = df[area_col].value_counts().head(8).reset_index()
    distribucion.columns = ['Área', 'Frecuencia']
    
    # Gráfico circular (dona) + barras horizontales debajo
    fig_dona = px.pie(distribucion, values='Frecuencia', names='Área',
                      hole=0.5, color_discrete_sequence=px.colors.sequential.Oranges)
    fig_dona.update_traces(textposition='inside', textinfo='percent+label')
    fig_dona.update_layout(showlegend=False, height=380)
    st.plotly_chart(fig_dona, use_container_width=True)
    
    # Barras horizontales atractivas
    fig_bar = px.bar(distribucion, x='Frecuencia', y='Área', orientation='h',
                     color='Frecuencia', color_continuous_scale="Oranges",
                     text='Frecuencia', height=200)
    fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False,
                          xaxis_title=None, yaxis_title=None, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# ==================== RANKING + PUNTOS DE DOLOR ====================
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 class='section-title'>Colaboradores con Más Consultas</h3>", unsafe_allow_html=True)
    ranking = kpis['ranking_empleados'].head(10).copy()
    st.dataframe(ranking, use_container_width=True, hide_index=True)

with col2:
    st.markdown("<h3 class='section-title'>Puntos de Dolor Detectados</h3>", unsafe_allow_html=True)
    if 'Es_Punto_Dolor' in df.columns and df['Es_Punto_Dolor'].any():
        dolor = df[df['Es_Punto_Dolor'] == True]['Categoria_Consulta'].value_counts().head(8)
        fig_d = px.bar(y=dolor.index, x=dolor.values, orientation='h',
                       color=dolor.values, color_continuous_scale="Reds")
        fig_d.update_layout(height=400, yaxis={'categoryorder': 'total ascending'},
                            xaxis_title="Frecuencia", yaxis_title=None)
        st.plotly_chart(fig_d, use_container_width=True)
    else:
        st.success("No hay puntos de dolor críticos detectados")

# ==================== FOOTER ====================
# Footer limpio y corporativo (solo Nutrisco)
st.markdown("""
<div class="footer">
    <p style="margin:0; font-size:0.95rem; color:#94a3b8;">
        Inteligencia Artificial al servicio de las personas – Nutrisco
    </p>
</div>
""", unsafe_allow_html=True)
