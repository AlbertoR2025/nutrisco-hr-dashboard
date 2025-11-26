# utils/data_loader.py
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
FILE = BASE_DIR / "data" / "Consultas-Atencion-Personas-Enriquecido.xlsx"

def load_data():
    if not FILE.exists():
        print("Archivo no encontrado")
        return None
    df = pd.read_excel(FILE, sheet_name="Atención_Completa")
    if 'Fecha ' in df.columns:
        df['Fecha '] = pd.to_datetime(df['Fecha '], errors='coerce')
    print(f"Cargadas {len(df)} filas")
    return df