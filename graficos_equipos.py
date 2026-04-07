# tabla_html.py
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

# Configuración inicial
st.set_page_config(
    page_title="Análisis de Equipos",
    page_icon="📈",
    layout="wide"
)

# Cargamos los distintos HTML
@st.cache_data
def load_htmls():
    base_path = "graphics"

    html_files = {
        "⚔️ Ataque vs Defensa": "Ataques_vs_Defensas_Por_Equipo.html",
        "🚀 Equipos Eficientes": "Equipos_Eficientes_GD_Puntos_Por_Partido.html",
        "👥 Media de Edad": "Media_Edades_Equipos.html",
        "📦 Distribución de Edades": "Boxplot_Edades_Equipos.html"
    }

    html_content = {}
    for key, file_name in html_files.items():
        path = os.path.join(base_path, file_name)
        html_content[key] = open(path, encoding="utf-8").read() if os.path.exists(path) else None

    return html_content


# Cargamos los dataframes para hacer los insights importantes
@st.cache_data
def load_dataframes():
    return {
        "⚔️ Ataque vs Defensa": pd.read_csv("data_output/Ataques_vs_Defensas_Por_Equipo.csv"),
        "🚀 Equipos Eficientes": pd.read_csv("data_output/Equipos_Eficientes_GD_Puntos_Por_Partido.csv"),
        "👥 Media de Edad": pd.read_csv("data_output/Media_Edades_Equipos.csv"),
        "📦 Distribución de Edades": pd.read_csv("data_output/Media_Edades_Equipos.csv"),
    }


html_data = load_htmls()
df_data = load_dataframes()

descripciones = {
    "⚔️ Ataque vs Defensa": """
    Este gráfico compara la capacidad ofensiva y defensiva de los equipos.  
    Permite identificar conjuntos equilibrados, dominantes o con carencias en alguna fase del juego.
    """,

    "🚀 Equipos Eficientes": """
    Visualiza qué equipos maximizan su rendimiento en función de sus resultados.  
    Ideal para detectar equipos que obtienen más puntos de lo esperado.
    """,

    "👥 Media de Edad": """
    Muestra la edad promedio de las plantillas.  
    Ayuda a identificar equipos jóvenes, en desarrollo, o veteranos con experiencia.
    """,

    "📦 Distribución de Edades": """
    Representa la distribución de edades dentro de los equipos.  
    Permite analizar la estructura generacional de cada plantilla.
    """
}

# Generar insight
def generar_insight(tab_name, df):
    if df is None or df.empty:
        return "No hay datos disponibles."

    try:
        # Ataque vs Defensa
        if tab_name == "⚔️ Ataque vs Defensa":

            # Mejor ataque
            mejor_ataque = df.loc[df["avg_goals_for"].idxmax()]

            # Mejor defensa (menos goles encajados)
            mejor_defensa = df.loc[df["avg_goals_against"].idxmin()]

            # Equipo más equilibrado (ataque - defensa)
            df["balance"] = df["avg_goals_for"] - df["avg_goals_against"]
            equilibrado = df.loc[df["balance"].idxmax()]

            return f"""
            **Análisis de rendimiento**

            **Mejor ataque:** {mejor_ataque['name']}  
            Promedio goles: **{round(mejor_ataque['avg_goals_for'], 2)}**

            **Mejor defensa:** {mejor_defensa['name']}  
            Goles encajados: **{round(mejor_defensa['avg_goals_against'], 2)}**

            **Equipo más equilibrado:** {equilibrado['name']}  
            Balance: **{round(equilibrado['balance'], 2)}**
            """

        # Equipos eficientes
        elif tab_name == "🚀 Equipos Eficientes":

            # Mejor equipo en puntos por partido
            mejor = df.loc[df["points_per_game"].idxmax()]

            # Mejor diferencia de goles
            mejor_gd = df.loc[df["goal_diff"].idxmax()]
            # Qué equipos sacan más puntos de lo que "deberían"
            df["eficiencia"] = df["points_per_game"] / (df["goal_diff"].replace(0, 0.1))

            overperformer = df.loc[df["eficiencia"].idxmax()]
            underperformer = df.loc[df["eficiencia"].idxmin()]

            return f"""
            **Análisis de eficiencia**

            **Mejor equipo en puntos:** {mejor['name']}  
            Puntos/partido: **{round(mejor['points_per_game'], 2)}**

            **Mayor diferencia de goles:** {mejor_gd['name']}  
            Goal Difference: **{mejor_gd['goal_diff']}**

            **Equipo que sobre-rinde:** {overperformer['name']}  
            → Consigue más puntos de lo esperado según su rendimiento

            **Equipo que infra-rinde:** {underperformer['name']}  
            → No convierte su rendimiento en puntos
            """

        # Edad media
        elif tab_name == "👥 Media de Edad":
            # Nos quedamos con un registro por equipo
            df_equipos = df.drop_duplicates(subset=["team_name"])

            # Equipo más joven
            joven = df_equipos.loc[df_equipos["avg_age"].idxmin()]

            # Equipo más veterano
            veterano = df_equipos.loc[df_equipos["avg_age"].idxmax()]

            # Media global
            media = df_equipos["avg_age"].mean()

            jovenes = df_equipos[df_equipos["avg_age"] < media - 1]
            veteranos = df_equipos[df_equipos["avg_age"] > media + 1]

            return f"""
            **Análisis de edad de plantillas**

            **Equipo más joven:** {joven['team_name']}  
            Edad media: **{round(joven['avg_age'], 1)} años**

            **Equipo más veterano:** {veterano['team_name']}  
            Edad media: **{round(veterano['avg_age'], 1)} años**

            **Media global:** {round(media, 1)} años

            **Equipos jóvenes:** {", ".join(jovenes['team_name'].tolist()) or "Ninguno claro"}

            **Equipos veteranos:** {", ".join(veteranos['team_name'].tolist()) or "Ninguno claro"}
            """

        # Distribución edades
        elif tab_name == "📦 Distribución de Edades":
            col_edad = [c for c in df.columns if "age" in c.lower()]

            if col_edad:
                return f"""
                📊 Edad media global: **{round(df[col_edad[0]].mean(),1)} años**  
                📉 Mínima: {round(df[col_edad[0]].min(),1)}  
                📈 Máxima: {round(df[col_edad[0]].max(),1)}
                """

    except Exception as e:
        return f"No se pudo generar insight ({e})"

    return "Insight no disponible."

st.title("📊 Visualizaciones Interactivas de Equipos")
st.markdown("""
Esta herramienta te permite explorar datos sobre capacidad ofensiva, solidez defensiva, eficiencia en puntos y patrones de juego en diferentes ligas, facilitando la comparación entre equipos y competiciones.
""")

tabs = st.tabs(list(html_data.keys()))

for i, tab_name in enumerate(html_data.keys()):
    with tabs[i]:

        st.subheader(tab_name)

        df = df_data.get(tab_name)
        html = html_data.get(tab_name)
        if tab_name in descripciones:
            with st.expander("¿Qué estás viendo?", expanded=True):
                st.markdown(descripciones[tab_name])
        # Insight
        st.success(generar_insight(tab_name, df))

        # Descarga del HTML
        if html:
            st.download_button(
                "📥 Descargar HTML",
                data=html,
                file_name=f"{tab_name}.html",
                mime="text/html",
                key=f"dl_{i}"
            )

            components.html(html, height=800, scrolling=True)
        else:
            st.warning("No hay gráfico disponible")

        st.caption("📌 Gráficos generados con plotly e insight obtenidos mediante los datos del csv")