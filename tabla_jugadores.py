import streamlit as st
import pandas as pd

# Configuración general de la página
st.set_page_config(
    page_title="Análisis de Jugadores",
    page_icon="👤",
    layout="wide"
)

# Carga en caché de los conjuntos de datos
@st.cache_data
def load_data():
    return {
        "🎯 Faltas a Extremos": pd.read_csv("data_input/Faltas_Recibidas_Extremos.csv"),
        "⚽ Goles y Asistencias": pd.read_csv("data_input/Goles_Asistencias_Extremos.csv"),
        "🌍 Goles por Nacionalidad": pd.read_csv("data_input/Media_Goles_Nacionalidad.csv"),
    }

csv_data = load_data()

# Títulos de la interfaz
st.title("📊 Análisis de Jugadores")
st.markdown("""
Explora el rendimiento individual de los jugadores a través de métricas clave.  
Analiza la generación de peligro de los extremos, la contribución ofensiva y goles según nacionalidad para descubrir perfiles destacados y patrones de juego.
""")

# Configuración de pestañas
tab_names = list(csv_data.keys())
ui_tabs = st.tabs(tab_names)

# Renderizado de cada DataFrame por pestaña
for i, current_tab_name in enumerate(tab_names):
    with ui_tabs[i]:
        # Clonamos el DataFrame para no mutar el estado en caché
        current_df = csv_data[current_tab_name].copy()

        st.subheader(current_tab_name)

        # Creación de filtros de edad interactivos si la columna está presente
        if "age" in current_df.columns:
            with st.container():
                col1, col2 = st.columns([1, 3])

                with col1:
                    st.markdown("### 🎛️ Filtros")

                with col2:
                    min_age = int(current_df["age"].min())
                    max_age = int(current_df["age"].max())

                    age_range = st.slider(
                        "Rango de edad",
                        min_value=min_age,
                        max_value=max_age,
                        value=(min_age, max_age),
                        key=f"age_{i}"
                    )

                    # Filtrado de los datos basado en los inputs del usuario
                    current_df = current_df[
                        (current_df["age"] >= age_range[0]) &
                        (current_df["age"] <= age_range[1])
                    ]

        # Renderizado interactivo del DataFrame filtrado
        st.dataframe(
            current_df,
            use_container_width=True
        )

        # Estadísticas de registro
        st.caption(f"📌 Total de jugadores: {len(current_df)}")