import streamlit as st
import pandas as pd

# Configuración general
st.set_page_config(
    page_title="Análisis de Jugadores",
    page_icon="👤",
    layout="wide"
)

@st.cache_data
def load_data():
    return {
        "🎯 Faltas a Extremos": pd.read_csv("data_output/Faltas_Recibidas_Extremos.csv"),
        "⚽ Goles y Asistencias": pd.read_csv("data_output/Goles_Asistencias_Extremos.csv"),
        "🌍 Goles por Nacionalidad": pd.read_csv("data_output/Media_Goles_Nacionalidad.csv"),
    }

data = load_data()

# Cabecera de la página
st.title("📊 Análisis de Jugadores")
st.markdown("""
Explora el rendimiento individual de los jugadores a través de métricas clave.  
Analiza la generación de peligro de los extremos, la contribución ofensiva y goles según nacionalidad para descubrir perfiles destacados y patrones de juego.
""")

# Pestañas
tab_names = list(data.keys())
tabs = st.tabs(tab_names)

# Contenido de cada pestaña
for i, tab_name in enumerate(tab_names):
    with tabs[i]:
        df = data[tab_name].copy()

        st.subheader(tab_name)

        # Filtros
        if "age" in df.columns:
            with st.container():
                col1, col2 = st.columns([1, 3])

                with col1:
                    st.markdown("### 🎛️ Filtros")

                with col2:
                    edad_min = int(df["age"].min())
                    edad_max = int(df["age"].max())

                    edad = st.slider(
                        "Rango de edad",
                        min_value=edad_min,
                        max_value=edad_max,
                        value=(edad_min, edad_max),
                        key=f"edad_{i}"
                    )

                    df = df[
                        (df["age"] >= edad[0]) &
                        (df["age"] <= edad[1])
                    ]

        # Tabla
        st.dataframe(
            df,
            use_container_width=True
        )

        # Información extra
        st.caption(f"📌 Total de jugadores: {len(df)}")