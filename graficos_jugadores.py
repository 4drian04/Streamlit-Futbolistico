import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

# Configuración inicial de la página
st.set_page_config(
    page_title="Visualizaciones de jugadores",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# CARGA DE HTML
# -----------------------------
@st.cache_data
def load_htmls():
    base_path = "graphics"

    html_files = {
        "Faltas recibidas por extremos": "Faltas_Recibidas_Extremos.html",
        "Gol/Asistencias extremos": "Goles_Asistencias_Extremos.html",
        "Media de goles por nacionalidad": "Media_Goles_Nacionalidad.html"
    }

    html_content = {}
    for key, file_name in html_files.items():
        path = os.path.join(base_path, file_name)
        html_content[key] = open(path, encoding="utf-8").read() if os.path.exists(path) else None

    return html_content

# -----------------------------
# CARGA DE DATAFRAMES PARA INSIGHTS
# -----------------------------
@st.cache_data
def load_dataframes():
    return {
        "Faltas recibidas por extremos": pd.read_csv("data_input/Faltas_Recibidas_Extremos.csv"),
        "Gol/Asistencias extremos": pd.read_csv("data_input/Goles_Asistencias_Extremos.csv"),
        "Media de goles por nacionalidad": pd.read_csv("data_input/Media_Goles_Nacionalidad.csv")
    }

html_data = load_htmls()
df_data = load_dataframes()

# -----------------------------
# GENERADOR DE INSIGHTS
# -----------------------------
def generate_insight(tab_name, df):
    if df is None or df.empty:
        return "No hay datos disponibles."

    try:
        if tab_name == "Faltas recibidas por extremos":
            
            top_total_fouls = df.loc[df["fouls_received"].idxmax()]
            top_per_game = df.loc[df["fouls_per_game"].idxmax()]

            # Extremos jóvenes (menores de 23 años) que reciben más faltas
            young_players = df[df["age"] < 23]
            if not young_players.empty:
                top_young = young_players.loc[young_players["fouls_received"].idxmax()]
                young_text = f"{top_young['player_name']} ({top_young['team_id']}) → {top_young['fouls_received']} faltas"
            else:
                young_text = "No hay extremos jóvenes destacados"

            return f"""
            **Análisis de faltas a extremos**

            **Extremo más faltado (total):** {top_total_fouls['player_name']}  → {top_total_fouls['fouls_received']} faltas

            **Extremo más faltado por partido:** {top_per_game['player_name']} → {round(top_per_game['fouls_per_game'],2)} faltas/partido

            **Extremo joven más faltado:** {young_text}
            """

        elif tab_name == "Gol/Asistencias extremos":
            
            top_contribution = df.loc[df["total_contribution"].idxmax()]

            return f"""
            **Análisis de contribución ofensiva de extremos**

            **Extremo con mayor contribución:** {top_contribution['player_name']} ({top_contribution['player_team_id']})  
            Total de goles+asistencias: **{top_contribution['total_contribution']}**
            """

        elif tab_name == "Media de goles por nacionalidad":
            
            top_avg_goals = df.loc[df["avg_goals"].idxmax()]
            top_total_goals = df.loc[df["total_goals"].idxmax()]

            return f"""
            **Análisis de goles por nacionalidad**

            **Mayor promedio de goles por jugador:** {top_avg_goals['nationality']} → {round(top_avg_goals['avg_goals'],2)} goles por jugador

            **Nacionalidad con más goles totales:** {top_total_goals['nationality']} → {top_total_goals['total_goals']} goles
            """

    except Exception as e:
        return f"No se pudo generar insight ({e})"

    return "Insight no disponible."

# Interfaz de Usuario (UI) Principal
st.title("📊 Visualizaciones interactivas de jugadores")
st.markdown("Análisis de los diferentes extremos, en cuanto a contribuciones de gol (g/a) y faltas recibidas. Además, se muestra los goles por las diferentes nacionalidades")

ui_tabs = st.tabs(list(html_data.keys()))

for i, current_tab_name in enumerate(html_data.keys()):
    with ui_tabs[i]:

        st.subheader(current_tab_name)

        current_df = df_data.get(current_tab_name)
        current_html = html_data.get(current_tab_name)

        # Mostrar insight generado
        st.success(generate_insight(current_tab_name, current_df))

        # Descarga e integración del archivo HTML
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
            st.warning("No se encontró el archivo HTML")

        st.caption("📌 Gráficos generados con plotly e insight obtenidos mediante los datos del csv")