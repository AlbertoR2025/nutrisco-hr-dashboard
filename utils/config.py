# utils/config.py → VERSIÓN BLINDADA FINAL (funciona sí o sí)
import os
from pathlib import Path

# Ruta absoluta que funciona en cualquier PC
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_FILE = BASE_DIR / "data" / "inventario_procesado_final.csv"

# === COLUMNAS EXACTAS DE TU CSV (con el espacio al final en Fecha) ===
COL_RUT = 'RUT_clean'
COL_FECHA = 'Fecha '                    # ← ¡¡OJO!! lleva espacio al final
COL_NOMBRE = 'Nombre Completo'
COL_AREA = 'Nombre Área'
COL_CATEGORIA = 'Categoria_Consulta'
COL_ESTADO_NORMALIZADO = 'Estado_Normalizado'
COL_TIPO_RESOLUCION = 'Tipo_Resolucion'
COL_CONSULTA_TEMA = 'Consulta'
COL_RESPUESTA = 'Respuesta'
COL_OBSERVACION = 'Observación'
COL_PUNTO_DOLOR = 'Es_Punto_Dolor'
COL_URGENCIA = 'Nivel_Urgencia'
COL_CONSULTAS_EMPLEADO = 'Consultas_Empleado'

# DEBUG FORZADO
print("\n" + "="*60)
print("CONFIG CARGADO CORRECTAMENTE")
print(f"Archivo esperado: {PROCESSED_FILE}")
print(f"¿Existe?: {'SÍ' if PROCESSED_FILE.exists() else 'NO'}")
print("="*60 + "\n")