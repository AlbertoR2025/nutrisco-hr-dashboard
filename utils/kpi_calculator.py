# utils/kpi_calculator.py

import pandas as pd
from .config import *

def calculate_kpis(df):
    """Calcula los KPIs clave basados en el archivo procesado."""
    
    total_consultas = len(df)
    
    # 1. KPIs Globales y Operativos
    
    # Consultas urgentes: Conteo donde Nivel_Urgencia == 'Alta'
    urgentes = df[df[COL_URGENCIA] == 'Alta'].shape[0]
    
    # Consultas resueltas en primer contacto (TRPC)
    resueltas_pc = df[df[COL_TIPO_RESOLUCION] == 'Resuelto en Primer Contacto'].shape[0]
    trpc = (resueltas_pc / total_consultas) * 100 if total_consultas > 0 else 0
    
    # Tasa de derivación
    derivadas = df[df[COL_TIPO_RESOLUCION] == 'Derivado'].shape[0]
    tasa_derivacion = (derivadas / total_consultas) * 100 if total_consultas > 0 else 0
    
    # Distribución por área y cargo
    distribucion_area = df[COL_AREA].value_counts().head(5).reset_index()
    distribucion_area.columns = ['Área', 'Frecuencia']
    
    # 2. Métricas de Tendencia y Temas
    
    # Top 5 categorías de consulta
    top_categorias = df[COL_CATEGORIA].value_counts().head(5).reset_index()
    top_categorias.columns = ['Categoría', 'Frecuencia']
    
    # Puntos de dolor actuales
    puntos_dolor = df[df[COL_PUNTO_DOLOR] == True].shape[0]
    
    # Consultas pendientes o abiertas
    pendientes = df[df[COL_ESTADO_NORMALIZADO].isin(['Pendiente', 'Abierto'])].shape[0]
    
    # 3. Métricas para acción y supervisión
    
    # Ranking de empleados más activos
    ranking_empleados = df.groupby([COL_NOMBRE, COL_RUT])[COL_CONSULTAS_EMPLEADO].max().reset_index()
    ranking_empleados = ranking_empleados.sort_values(by=COL_CONSULTAS_EMPLEADO, ascending=False).head(5)
    ranking_empleados.columns = ['Nombre', 'RUT', 'Total Consultas']
    
    # Consultas recientes (las últimas 5)
    consultas_recientes = df.sort_values(by=COL_FECHA, ascending=False).head(5)

    return {
        'total_consultas': total_consultas,
        'urgentes': urgentes,
        'trpc': trpc,
        'tasa_derivacion': tasa_derivacion,
        'distribucion_area': distribucion_area,
        'top_categorias': top_categorias,
        'puntos_dolor': puntos_dolor,
        'pendientes': pendientes,
        'ranking_empleados': ranking_empleados,
        'consultas_recientes': consultas_recientes
    }