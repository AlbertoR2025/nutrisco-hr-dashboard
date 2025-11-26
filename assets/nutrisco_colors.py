"""
Paleta de colores oficial de Nutrisco para el dashboard
"""

# Colores principales de Nutrisco
PRIMARY_BLUE = "#1E3A8A"      # Azul corporativo
SECONDARY_GREEN = "#10B981"   # Verde corporativo
ACCENT_ORANGE = "#F59E0B"     # Naranja corporativo

# Colores neutrales
NEUTRAL_WHITE = "#FFFFFF"
NEUTRAL_LIGHT = "#F8FAFC"
NEUTRAL_GRAY = "#64748B"
NEUTRAL_DARK = "#1E293B"

# Colores para estados y alertas
SUCCESS_GREEN = "#10B981"
WARNING_ORANGE = "#F59E0B"
ERROR_RED = "#EF4444"
INFO_BLUE = "#3B82F6"

# Colores para gráficos (paleta extendida)
CHART_COLORS = [
    PRIMARY_BLUE, 
    SECONDARY_GREEN, 
    ACCENT_ORANGE,
    "#8B5CF6",  # Violeta
    "#EF4444",  # Rojo
    "#06B6D4",  # Cian
    "#84CC16",  # Verde lima
    "#F97316",  # Naranja intenso
    "#6366F1",  # Índigo
    "#EC4899"   # Rosa
]

# Gradientes para visualizaciones
GRADIENTS = {
    "blue_gradient": ["#1E3A8A", "#3B82F6", "#60A5FA"],
    "green_gradient": ["#10B981", "#34D399", "#6EE7B7"],
    "orange_gradient": ["#F59E0B", "#FBBF24", "#FCD34D"]
}

def get_company_color(company_name):
    """Devuelve el color corporativo basado en el nombre de la empresa"""
    company_colors = {
        "Nutrisco S.A.": PRIMARY_BLUE,
        "Orizon S.A.": SECONDARY_GREEN
    }
    return company_colors.get(company_name, NEUTRAL_GRAY)