# tabla_html_insight.py
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

# Configuración inicial
st.set_page_config(
    page_title="Visualizaciones de jugadores",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# CARGA HTML
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
# CARGA DATAFRAMES PARA INSIGHT
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
def generar_insight(tab_name, df):
    if df is None or df.empty:
        return "No hay datos disponibles."

    try:
        if tab_name == "Faltas recibidas por extremos":
            # Top extremo más faltado
            top_total = df.loc[df["fouls_received"].idxmax()]

            # Top extremo más faltado por partido
            top_por_partido = df.loc[df["fouls_per_game"].idxmax()]

            # Extremos jóvenes (edad < 23) más faltados
            jovenes = df[df["age"] < 23]
            if not jovenes.empty:
                top_joven = jovenes.loc[jovenes["fouls_received"].idxmax()]
                joven_text = f"{top_joven['player_name']} ({top_joven['team_id']}) → {top_joven['fouls_received']} faltas"
            else:
                joven_text = "No hay extremos jóvenes destacados"

            return f"""
            **Análisis de faltas a extremos**

            **Extremo más faltado (total):** {top_total['player_name']}  → {top_total['fouls_received']} faltas

            **Extremo más faltado por partido:** {top_por_partido['player_name']} → {round(top_por_partido['fouls_per_game'],2)} faltas/partido

            **Extremo joven más faltado:** {joven_text}
            """

        elif tab_name == "Gol/Asistencias extremos":
            # Extremo con mayor contribución ofensiva
            top_total = df.loc[df["total_contribution"].idxmax()]

            return f"""
            **Análisis de contribución ofensiva de extremos**

            **Extremo con mayor contribución:** {top_total['player_name']} ({top_total['player_team_id']})  
            Total de goles+asistencias: **{top_total['total_contribution']}**
            """

        elif tab_name == "Media de goles por nacionalidad":
            top_avg = df.loc[df["avg_goals"].idxmax()]
            top_total_goals = df.loc[df["total_goals"].idxmax()]

            return f"""
            **Análisis de goles por nacionalidad**

            **Mayor promedio de goles por jugador:** {top_avg['nationality']} → {round(top_avg['avg_goals'],2)} goles por jugador

            **Nacionalidad con más goles totales:** {top_total_goals['nationality']} → {top_total_goals['total_goals']} goles
            """

    except Exception as e:
        return f"No se pudo generar insight ({e})"

    return "Insight no disponible."

st.title("📊 Visualizaciones interactivas de jugadores")
st.markdown("Análisis de los diferentes extremos, en cuanto a contribuciones de gol (g/a) y faltas recibidas. Además, se muestra los goles por las diferentes nacionalidades")

tabs = st.tabs(list(html_data.keys()))

for i, tab_name in enumerate(html_data.keys()):
    with tabs[i]:

        st.subheader(tab_name)

        df = df_data.get(tab_name)
        html = html_data.get(tab_name)

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
            st.warning("No se encontró el archivo HTML")

        st.caption("📌 Gráficos generados con plotly e insight obtenidos mediante los datos del csv")