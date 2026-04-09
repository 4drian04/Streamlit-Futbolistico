import streamlit as st
import pandas as pd

# Configuración inicial de la vista de tabla
st.set_page_config(page_title="Tabla de equipos", layout="wide", page_icon="👥")

# Función para cargar los diferentes DataFrames desde los archivos CSV
@st.cache_data
def load_data():
    return {
        "⚔️ Ataque vs Defensa": pd.read_csv("data_input/Ataques_vs_Defensas_Por_Equipo.csv"),
        "🚀 Equipos Eficientes": pd.read_csv("data_input/Equipos_Eficientes_GD_Puntos_Por_Partido.csv"),
        "🛡️ Ligas Defensivas": pd.read_csv("data_input/Ligas_Mas_Defensivas.csv"),
        "⚽ Goles por Liga": pd.read_csv("data_input/Media_Goles_Partido_Ligas.csv"),
        "🏆 Puntos por Liga": pd.read_csv("data_input/Media_Puntos_Partidos_Ligas.csv"),
        "🤝 Victorias y Empates": pd.read_csv("data_input/Victorias_Empates_Por_Liga.csv"),
    }

csv_data = load_data()

# Diccionario de descripciones explicativas de cada tabla
descriptions = {
    "⚔️ Ataque vs Defensa": """
    Este análisis compara la capacidad ofensiva y defensiva de los equipos.  
    Permite identificar conjuntos equilibrados, dominantes o con carencias en alguna fase del juego.
    """,

    "🚀 Equipos Eficientes": """
    Visualiza qué equipos maximizan su rendimiento en función de sus resultados y diferencia de goles.  
    Ideal para detectar conjuntos que obtienen más puntos de lo esperado respecto a su desempeño.
    """,

    "🛡️ Ligas Defensivas": """
    Muestra las ligas más sólidas defensivamente, con menor promedio de goles en contra.  
    Útil para analizar tendencias defensivas por competición.
    """,

    "⚽ Goles por Liga": """
    Representa la media de goles por partido en cada liga.  
    Permite comparar qué ligas son más ofensivas y qué equipos destacan en anotación.
    """,

    "🏆 Puntos por Liga": """
    Analiza el promedio de puntos obtenidos por partido en cada liga.  
    Ayuda a evaluar la eficiencia de los equipos y la competitividad de la competición.
    """,

    "🤝 Victorias y Empates": """
    Muestra el ratio de victorias y empates por liga.  
    Permite identificar ligas más equilibradas o dominadas por ciertos equipos.
    """
}

# Títulos de la interfaz
st.title("📊 Análisis de Equipos y Ligas")
st.markdown("""
Sumérgete en un análisis detallado del rendimiento futbolístico.  
Esta herramienta te permite explorar datos sobre capacidad ofensiva, solidez defensiva, eficiencia en puntos y patrones de juego en diferentes ligas, facilitando la comparación entre equipos y competiciones.
""")

# Definición e iteración de pestañas para las tablas
tab_names = list(csv_data.keys())
ui_tabs = st.tabs(tab_names)

# Identificadores de las pestañas que requerirán filtros adicionales
tabs_with_filter = ["⚔️ Ataque vs Defensa", "🚀 Equipos Eficientes"]

# Renderizado del contenido de cada pestaña
for i, current_tab_name in enumerate(tab_names):
    with ui_tabs[i]:
        # Copia local del DataFrame para aplicar filtros sin alterar el original
        current_df = csv_data[current_tab_name].copy()

        st.subheader(current_tab_name)

        if current_tab_name in descriptions:
            with st.expander("¿Qué estás viendo?", expanded=True):
                st.markdown(descriptions[current_tab_name])
                
        # Creación y aplicación de filtros si corresponden a la pestaña
        if current_tab_name in tabs_with_filter and "name_league" in current_df.columns:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown("### 🎛️ Filtros")

                with col2:
                    unique_leagues = sorted(current_df["name_league"].dropna().unique())
                    selected_league = st.selectbox(
                        "Selecciona liga",
                        options=["Todas"] + list(unique_leagues),
                        key=f"league_{i}"
                    )

                    if selected_league != "Todas":
                        current_df = current_df[current_df["name_league"] == selected_league]
                        
        # Renderizado interactivo de la tabla de datos
        st.dataframe(
            current_df,
            use_container_width=True
        )

        # Información metadatos extra
        st.caption(f"📌 Total de registros: {len(current_df)}")