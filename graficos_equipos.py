import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

# Configuración inicial de la página
st.set_page_config(
    page_title="Análisis de Equipos",
    page_icon="📈",
    layout="wide"
)

# Carga de los distintos archivos HTML generados previamente
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
        # Leemos el archivo si existe, de lo contrario asignamos None
        html_content[key] = open(path, encoding="utf-8").read() if os.path.exists(path) else None

    return html_content


# Carga de los DataFrames necesarios para generar los insights de valor
@st.cache_data
def load_dataframes():
    return {
        "⚔️ Ataque vs Defensa": pd.read_csv("data_input/Ataques_vs_Defensas_Por_Equipo.csv"),
        "🚀 Equipos Eficientes": pd.read_csv("data_input/Equipos_Eficientes_GD_Puntos_Por_Partido.csv"),
        "👥 Media de Edad": pd.read_csv("data_input/Media_Edades_Equipos.csv"),
        "📦 Distribución de Edades": pd.read_csv("data_input/Media_Edades_Equipos.csv"),
    }


# Inicialización de datos
html_data = load_htmls()
df_data = load_dataframes()

# Diccionario descriptivo para el usuario
descriptions = {
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

# Función para generar insights dinámicos basados en la pestaña actual
def generate_insight(tab_name, df):
    if df is None or df.empty:
        return "No hay datos disponibles."

    try:
        # Lógica para la pestaña de Ataque vs Defensa
        if tab_name == "⚔️ Ataque vs Defensa":

            best_attack = df.loc[df["avg_goals_for"].idxmax()]
            best_defense = df.loc[df["avg_goals_against"].idxmin()]

            # Cálculo del equipo más equilibrado (diferencia entre ataque y defensa)
            df["balance"] = df["avg_goals_for"] - df["avg_goals_against"]
            balanced_team = df.loc[df["balance"].idxmax()]

            return f"""
            **Análisis de rendimiento**

            **Mejor ataque:** {best_attack['name']}  
            Promedio goles: **{round(best_attack['avg_goals_for'], 2)}**

            **Mejor defensa:** {best_defense['name']}  
            Goles encajados: **{round(best_defense['avg_goals_against'], 2)}**

            **Equipo más equilibrado:** {balanced_team['name']}  
            Balance: **{round(balanced_team['balance'], 2)}**
            """

        # Lógica para la pestaña de Equipos Eficientes
        elif tab_name == "🚀 Equipos Eficientes":

            best_team = df.loc[df["points_per_game"].idxmax()]
            best_gd = df.loc[df["goal_diff"].idxmax()]
            
            # Métrica de eficiencia: Puntos obtenidos vs Diferencia de Goles
            df["efficiency"] = df["points_per_game"] / (df["goal_diff"].replace(0, 0.1))

            overperformer = df.loc[df["efficiency"].idxmax()]
            underperformer = df.loc[df["efficiency"].idxmin()]

            return f"""
            **Análisis de eficiencia**

            **Mejor equipo en puntos:** {best_team['name']}  
            Puntos/partido: **{round(best_team['points_per_game'], 2)}**

            **Mayor diferencia de goles:** {best_gd['name']}  
            Goal Difference: **{best_gd['goal_diff']}**

            **Equipo que sobre-rinde:** {overperformer['name']}  
            → Consigue más puntos de lo esperado según su rendimiento

            **Equipo que infra-rinde:** {underperformer['name']}  
            → No convierte su rendimiento en puntos
            """

        # Lógica para la pestaña de Media de Edad
        elif tab_name == "👥 Media de Edad":
            # Filtro para mantener un registro único por equipo
            df_teams = df.drop_duplicates(subset=["team_name"])

            youngest = df_teams.loc[df_teams["avg_age"].idxmin()]
            oldest = df_teams.loc[df_teams["avg_age"].idxmax()]
            mean_age = df_teams["avg_age"].mean()

            young_teams = df_teams[df_teams["avg_age"] < mean_age - 1]
            old_teams = df_teams[df_teams["avg_age"] > mean_age + 1]

            return f"""
            **Análisis de edad de plantillas**

            **Equipo más joven:** {youngest['team_name']}  
            Edad media: **{round(youngest['avg_age'], 1)} años**

            **Equipo más veterano:** {oldest['team_name']}  
            Edad media: **{round(oldest['avg_age'], 1)} años**

            **Media global:** {round(mean_age, 1)} años

            **Equipos jóvenes:** {", ".join(young_teams['team_name'].tolist()) or "Ninguno claro"}

            **Equipos veteranos:** {", ".join(old_teams['team_name'].tolist()) or "Ninguno claro"}
            """

        # Lógica para la pestaña de Distribución de Edades
        elif tab_name == "📦 Distribución de Edades":
            age_col = [c for c in df.columns if "age" in c.lower()]

            if age_col:
                return f"""
                📊 Edad media global: **{round(df[age_col[0]].mean(),1)} años** 📉 Mínima: {round(df[age_col[0]].min(),1)}  
                📈 Máxima: {round(df[age_col[0]].max(),1)}
                """

    except Exception as e:
        return f"No se pudo generar insight ({e})"

    return "Insight no disponible."

# Interfaz de Usuario (UI) Principal
st.title("📊 Visualizaciones Interactivas de Equipos")
st.markdown("""
Esta herramienta te permite explorar datos sobre capacidad ofensiva, solidez defensiva, eficiencia en puntos y patrones de juego en diferentes ligas, facilitando la comparación entre equipos y competiciones.
""")

# Creación de pestañas iterando sobre las claves del diccionario html_data
ui_tabs = st.tabs(list(html_data.keys()))

for i, current_tab_name in enumerate(html_data.keys()):
    with ui_tabs[i]:

        st.subheader(current_tab_name)

        current_df = df_data.get(current_tab_name)
        current_html = html_data.get(current_tab_name)
        
        # Expansor explicativo
        if current_tab_name in descriptions:
            with st.expander("¿Qué estás viendo?", expanded=True):
                st.markdown(descriptions[current_tab_name])
                
        # Mostrar el insight generado
        st.success(generate_insight(current_tab_name, current_df))

        # Botón de descarga y renderizado del gráfico HTML
        if current_html:
            st.download_button(
                "📥 Descargar HTML",
                data=current_html,
                file_name=f"{current_tab_name}.html",
                mime="text/html",
                key=f"dl_{i}"
            )

            components.html(current_html, height=800, scrolling=True)
        else:
            st.warning("No hay gráfico disponible")

        st.caption("📌 Gráficos generados con plotly e insight obtenidos mediante los datos del csv")