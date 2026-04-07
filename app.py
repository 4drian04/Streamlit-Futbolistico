import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(page_title="App Fútbol", layout="wide", page_icon="⚽")

# =========================
# MENU SUPERIOR
# =========================

menu = st.navigation({
    "Tablas": [st.Page("tabla_equipos.py", title="Equipos"), st.Page("tabla_jugadores.py", title="Jugadores")],
    "Gráficos": [st.Page("graficos_equipos.py", title="Equipos"), st.Page("graficos_ligas.py", title="Ligas"), st.Page("graficos_jugadores.py", title="Jugadores")],
    "Dashboard": [st.Page("tableau_dashboard.py", title="Dashboard")],
    "Predicción": [st.Page("prediccion.py", title="🤖 Predicción")]
},
position='top')

page = menu.run()
