# utils/chatbot_engine.py → VERSIÓN MEJORADA (RAG + FAQ + Puntos de dolor)

import pandas as pd
from datetime import datetime

# FAQs predefinidas (esto lo vamos a extraer automáticamente después)
FAQS = {
    "finiquito": "El finiquito se paga máximo 10 días hábiles después de firmado...",
    "buk": "Para ingresar a BUK usa tu RUT y la clave que te llegó al correo...",
    "vacaciones": "Tienes derecho a 15 días hábiles de vacaciones al año...",
    # ... aquí vamos a cargar automáticamente las 20 más frecuentes
}

class ChatbotHR:
    def __init__(self, df_knowledge_base):
        self.df = df_knowledge_base.copy()
        self.df['text_combined'] = self.df['Consulta'].fillna('') + " " + self.df['Respuesta'].fillna('') + " " + self.df['Observación'].fillna('')
        
    def find_similar_case(self, query, top_k=1):
        query_lower = query.lower()
        self.df['score'] = self.df['text_combined'].str.lower().str.count('|'.join(query_lower.split()))
        results = self.df[self.df['score'] > 0].sort_values('score', ascending=False)
        return results.head(top_k)
    
    def generate_response(self, user_query):
        similar = self.find_similar_case(user_query)
        
        if len(similar) > 0:
            caso = similar.iloc[0]
            nombre = caso['Nombre Completo']
            fecha = caso['Fecha '].strftime('%d/%m/%Y') if pd.notna(caso['Fecha ']) else 'reciente'
            respuesta = caso['Respuesta'] if pd.notna(caso['Respuesta']) else "Se derivó al área correspondiente."
            
            # Detectar punto de dolor
            es_punto_dolor = "⚠️ **Este es un tema recurrente (punto de dolor)**" if caso['Es_Punto_Dolor'] else ""
            
            return f"""
**Respuesta encontrada en caso similar**

**Empleado:** {nombre}  
**Fecha:** {fecha}  
{es_punto_dolor}

**Pregunta original:** {caso['Consulta']}

**Respuesta dada anteriormente:**
> {respuesta}

Si necesitas más detalles o tu caso es diferente, por favor escríbelo con más detalle o contacta directamente a RR.HH.
            """.strip()
        
        # Si no encuentra nada → FAQ o mensaje genérico
        query_lower = user_query.lower()
        for key, answer in FAQS.items():
            if key in query_lower:
                return f"**Respuesta automática (FAQ):** {answer}"
                
        return """
Lo siento, no encontré un caso exactamente igual en el historial.

Puedes intentar:
• Ser más específico con tu consulta
• Preguntar por temas como: finiquito, BUK, vacaciones, licencias, etc.
• O escribir directamente a rrhh@nutrisco.cl

¡Estamos trabajando para mejorar las respuestas día a día! 🤖
        """