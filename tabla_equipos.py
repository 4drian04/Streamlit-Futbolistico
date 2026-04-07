# tabla.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tabla de equipos", layout="wide", page_icon="👥")

# Carga de datos
@st.cache_data
def load_data():
    return {
        "⚔️ Ataque vs Defensa": pd.read_csv("data_output/Ataques_vs_Defensas_Por_Equipo.csv"),
        "🚀 Equipos Eficientes": pd.read_csv("data_output/Equipos_Eficientes_GD_Puntos_Por_Partido.csv"),
        "🛡️ Ligas Defensivas": pd.read_csv("data_output/Ligas_Mas_Defensivas.csv"),
        "⚽ Goles por Liga": pd.read_csv("data_output/Media_Goles_Partido_Ligas.csv"),
        "🏆 Puntos por Liga": pd.read_csv("data_output/Media_Puntos_Partidos_Ligas.csv"),
        "🤝 Victorias y Empates": pd.read_csv("data_output/Victorias_Empates_Por_Liga.csv"),
    }

data = load_data()

descripciones = {
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
# Cabecera
st.title("📊 Análisis de Equipos y Ligas")
st.markdown("""
Sumérgete en un análisis detallado del rendimiento futbolístico.  
Esta herramienta te permite explorar datos sobre capacidad ofensiva, solidez defensiva, eficiencia en puntos y patrones de juego en diferentes ligas, facilitando la comparación entre equipos y competiciones.
""")

# Pestañas
tab_names = list(data.keys())
tabs = st.tabs(tab_names)

# Tabs con filtros disponibles
tabs_con_filtro = ["⚔️ Ataque vs Defensa", "🚀 Equipos Eficientes"]

# Contenido de cada pestaña
for i, tab_name in enumerate(tab_names):
    with tabs[i]:
        df = data[tab_name].copy()

        st.subheader(tab_name)

        if tab_name in descripciones:
                    with st.expander("¿Qué estás viendo?", expanded=True):
                        st.markdown(descripciones[tab_name])
        # Filtros
        if tab_name in tabs_con_filtro and "name_league" in df.columns:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown("### 🎛️ Filtros")

                with col2:
                    ligas = sorted(df["name_league"].dropna().unique())
                    liga = st.selectbox(
                        "Selecciona liga",
                        options=["Todas"] + list(ligas),
                        key=f"liga_{i}"
                    )

                    if liga != "Todas":
                        df = df[df["name_league"] == liga]
        # Tabla
        st.dataframe(
            df,
            use_container_width=True
        )

        # Información extra
        st.caption(f"📌 Total de registros: {len(df)}")