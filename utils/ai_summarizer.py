import os
import pandas as pd
from dotenv import load_dotenv

# Intentar importar OpenAI, pero continuar si no está disponible
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Cargar variables de entorno
load_dotenv()

# Configurar OpenAI solo si está disponible
if OPENAI_AVAILABLE:
    openai.api_key = os.getenv("OPENAI_API_KEY", "sk-demo-key")

def generate_hr_summary(df, summary_type):
    """
    Genera un resumen de los datos de RR.HH.
    Si OpenAI no está disponible, usa resumen básico automático.
    """
    
    # Si no hay OpenAI, usar resumen automático
    if not OPENAI_AVAILABLE:
        return generate_basic_summary(df, summary_type)
    
    # Si hay OpenAI pero no API key válida
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "sk-demo-key":
        return generate_basic_summary(df, summary_type)
    
    try:
        # Crear contexto basado en los datos
        context = create_data_context(df)
        
        prompt = create_prompt(summary_type, context)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Eres un analista senior de Recursos Humanos. Proporciona análisis concisos, profesionales y accionables."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        # Fallback a resumen básico si hay error con OpenAI
        return generate_basic_summary(df, summary_type)

def create_data_context(df):
    """Crea un contexto resumido de los datos para el prompt"""
    
    if df.empty:
        return "No hay datos disponibles para análisis."
    
    context = f"""
    Información General:
    - Total de empleados: {len(df)}
    - Empresas: {', '.join(df['Nombre Empresa'].unique())}
    - Áreas principales: {', '.join(df['Nombre Área'].value_counts().head(5).index.tolist())}
    - Ubicaciones: {', '.join(df['Lugar de Trabajo'].unique())}
    - Tipos de contrato: {df['Tipo de Contrato'].value_counts().to_dict()}
    
    Distribución por Empresa:
    {df['Nombre Empresa'].value_counts().to_dict()}
    
    Top 5 Áreas:
    {df['Nombre Área'].value_counts().head(5).to_dict()}
    """
    
    return context

def create_prompt(summary_type, context):
    """Crea el prompt específico para cada tipo de resumen"""
    
    prompts = {
        "📊 Resumen General de la Empresa": f"""
        Proporciona un resumen ejecutivo general de la situación de recursos humanos.
        Incluye insights sobre distribución, fortalezas y áreas de oportunidad.
        
        Contexto:
        {context}
        
        Formato: Resumen ejecutivo con bullet points.
        """,
        
        "📝 Análisis de Contratos y Estabilidad Laboral": f"""
        Analiza la estabilidad laboral y composición de contratos.
        Identifica riesgos y oportunidades de mejora.
        
        Contexto:
        {context}
        
        Enfócate en: porcentaje de contratos temporales vs indefinidos, recomendaciones.
        """,
        
        "📍 Distribución Geográfica y Logística": f"""
        Analiza la distribución geográfica del personal.
        Considera implicaciones logísticas y operativas.
        
        Contexto:
        {context}
        
        Incluye: recomendaciones para gestión descentralizada.
        """,
        
        "👥 Composición por Áreas y Gerencias": f"""
        Analiza la composición del personal por áreas y gerencias.
        Identifica desbalances o áreas sobrecargadas.
        
        Contexto:
        {context}
        
        Enfócate en: distribución óptima, oportunidades de reestructuración.
        """,
        
        "🔍 Detección de Patrones Emergentes": f"""
        Detecta patrones, tendencias emergentes y anomalías en los datos.
        
        Contexto:
        {context}
        
        Incluye: patrones inusuales, tendencias a monitorear.
        """,
        
        "📈 Recomendaciones Estratégicas RR.HH": f"""
        Proporciona recomendaciones estratégicas basadas en el análisis de datos.
        
        Contexto:
        {context}
        
        Formato: Recomendaciones accionables prioritizadas.
        """
    }
    
    return prompts.get(summary_type, prompts["📊 Resumen General de la Empresa"])

def generate_basic_summary(df, summary_type):
    """Genera un resumen básico cuando no hay acceso a OpenAI"""
    
    if df.empty:
        return "No hay datos disponibles para generar el análisis."
    
    basic_summaries = {
        "📊 Resumen General de la Empresa": f"""
        **Resumen General - Análisis Automático**
        
        • **Empleados totales:** {len(df)}
        • **Distribución por empresa:** 
          {chr(10).join([f'  - {empresa}: {count}' for empresa, count in df['Nombre Empresa'].value_counts().items()])}
        • **Áreas principales:** {', '.join(df['Nombre Área'].value_counts().head(3).index.tolist())}
        • **Ubicaciones activas:** {df['Lugar de Trabajo'].nunique()}
        
        **Recomendación básica:** Monitorear distribución entre empresas y áreas.
        """,
        
        "📝 Análisis de Contratos y Estabilidad Laboral": f"""
        **Análisis de Contratos - Resumen Básico**
        
        • **Contratos indefinidos:** {len(df[df['Tipo de Contrato'] == 'Indefinido'])} 
        • **Contratos plazo fijo:** {len(df[df['Tipo de Contrato'] == 'Plazo fijo'])}
        • **Otros tipos:** {len(df[~df['Tipo de Contrato'].isin(['Indefinido', 'Plazo fijo'])])}
        
        **Estabilidad:** {len(df[df['Tipo de Contrato'] == 'Indefinido'])/len(df)*100:.1f}% de empleados con contrato indefinido.
        """
    }
    
    return basic_summaries.get(summary_type, "Análisis básico no disponible para este tipo.")