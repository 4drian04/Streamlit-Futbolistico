import streamlit as st
import pandas as pd
from pathlib import Path
import joblib

# Configuración de página (debe ser el primer comando)
st.set_page_config(page_title="Scouting IA", layout="wide", page_icon="⚽")

# ── Cargar modelo (con cache) ──
@st.cache_resource
def cargar_modelo():
    ruta = Path("modelos/pipeline_futbolistico.pkl")
    if not ruta.exists():
        return None
    return joblib.load(ruta)

modelo = cargar_modelo()

# ── Cabecera de la App ─────────────────────────────────────────
st.title("⚽ Clasificador de Posiciones IA")
st.markdown("""
Descubre cuál es la posición ideal de un jugador basándote en su rendimiento en el campo. 
Introduce sus estadísticas de la temporada y nuestro modelo de Machine Learning hará el resto.
""")
st.divider() # Línea separadora visual

if modelo is None:
    st.error("⚠️ Modelo no encontrado. Asegúrate de que 'pipeline_futbolistico.pkl' está en la carpeta 'modelos'.")
    st.stop()

# ── Formulario Organizado ─────────────────────────────────────
with st.form("prediccion_form", border=True):
    
    # SECCIÓN 1: Datos Generales
    st.subheader("📋 Datos Generales")
    c1, c2 = st.columns(2)
    with c1:
        games = st.number_input("Partidos jugados", min_value=1, max_value=100, value=25, step=1)
    with c2:
        time = st.number_input("Minutos jugados", min_value=1, max_value=9000, value=1800, step=10, 
                               help="Total de minutos en toda la temporada.")
    
    st.write("") # Espacio en blanco

    # SECCIÓN 2: Ataque y Creación
    st.subheader("🎯 Ataque y Creación")
    c3, c4, c5 = st.columns(3)
    with c3:
        goals = st.number_input("Goles Totales", min_value=0, max_value=100, value=5, step=1)
        npg = st.number_input("Goles (Sin Penalti)", min_value=0, max_value=100, value=4, step=1,
                              help="Debe ser igual o menor a los Goles Totales.")
    with c4:
        assists = st.number_input("Asistencias", min_value=0, max_value=50, value=3, step=1)
        shots = st.number_input("Tiros Totales", min_value=0, max_value=500, value=30, step=1)
    with c5:
        key_passes = st.number_input("Pases Clave", min_value=0, max_value=300, value=15, step=1,
                                     help="Pases que terminan en un tiro de un compañero.")

    st.write("") # Espacio en blanco

    # SECCIÓN 3: Defensa y Disciplina
    st.subheader("🛡️ Defensa y Disciplina")
    c6, c7, c8 = st.columns(3)
    with c6:
        tackles = st.number_input("Entradas con éxito", min_value=0, max_value=500, value=25, step=1)
    with c7:
        yellow_cards = st.number_input("Tarjetas Amarillas", min_value=0, max_value=30, value=3, step=1)
    with c8:
        red_cards = st.number_input("Tarjetas Rojas", min_value=0, max_value=10, value=0, step=1)

    st.write("") # Espacio en blanco para separar el botón
    
    # Botón principal, ancho completo
    enviado = st.form_submit_button("🔍 Analizar Perfil del Jugador", use_container_width=True, type="primary")

# ── Procesamiento y Resultados ────────────────────────────────
if enviado:
    with st.spinner("Analizando estadísticas con Inteligencia Artificial..."):
        # 1. Cálculos de promedios
        tackles_per_game = tackles / games
        goals_per_game = goals / games
        assists_per_game = assists / games
        key_passes_per_game = key_passes / games
        partidos_completos = time / 90 if time > 0 else 0.1

        # 2. Estimación de métricas avanzadas (xG, xA, etc.)
        xG = shots * 0.10          
        xA = key_passes * 0.10      
        npxG = npg                  
        xGChain = xG + xA + (partidos_completos * 0.3) 
        xGBuildup = partidos_completos * 0.25          

        # 3. Creación del DataFrame
        columnas = [
            "games", "time", "goals", "xG", "assists", "xA", "shots", "key_passes", 
            "yellow_cards", "red_cards", "npg", "npxG", "xGChain", "xGBuildup", "tackles", "tackles_per_game", 
            "goals_per_game", "assists_per_game", "key_passes_per_game"]
        
        X = pd.DataFrame([[
            games, time, goals, xG, assists, xA, shots, key_passes, 
            yellow_cards, red_cards, npg, npxG, xGChain, xGBuildup, tackles, tackles_per_game, 
            goals_per_game, assists_per_game, key_passes_per_game]], columns=columnas)
        
        posiciones = [
        "Defensa",
        "Portero",
        "Delantero",
        "Centrocampista",
        "Segundo delantero"]

        # 4. Predicción
        posicion = modelo.predict(X)[0]
        proba = modelo.predict_proba(X)[0].max()

        # 5. UI de Resultados (Dashboard style)
        st.divider()
        st.subheader("📊 Resultado del Análisis")
        
        res1, res2 = st.columns(2)
        res1.metric(label="Posición Recomendada", value=str(posiciones[posicion]))
        res2.metric(label="Nivel de Confianza (IA)", value=f"{proba:.1%}")

        # Gráfico de barras más limpio
        st.markdown("**Distribución de probabilidad por posición:**")
        probas = modelo.predict_proba(X)[0]
        
        df_probas = pd.DataFrame({"Posición": posiciones, "Probabilidad": probas})
        st.bar_chart(df_probas.set_index("Posición"), color="#1f77b4") # Le damos un color azul elegante