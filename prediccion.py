"""
Módulo: prediccion.py
Descripción: Interfaz de usuario y lógica predictiva para el Scouting IA.
Recopila estadísticas de jugadores, procesa métricas avanzadas (xG, xA, etc.)
y utiliza un modelo de Machine Learning pre-entrenado para clasificar 
su posición ideal en el campo.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import joblib

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
# Configuración de la página (obligatorio como primer comando de Streamlit)
st.set_page_config(page_title="Scouting IA", layout="wide", page_icon="⚽")

# Inicialización del historial en el estado de la sesión (Session State)
# Esto permite que los datos de predicción persistan al navegar a la página de historial.
if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================
# 2. CARGA DEL MODELO PREDICTIVO
# ==========================================
@st.cache_resource
def load_model():
    """
    Carga el modelo de Machine Learning desde el sistema de archivos local.
    Usa el decorador @st.cache_resource para evitar cargar el archivo .pkl 
    repetidamente con cada interacción del usuario, mejorando el rendimiento.
    """
    model_path = Path("modelos/pipeline_futbolistico.pkl")
    if not model_path.exists():
        return None
    return joblib.load(model_path)

ml_model = load_model()

# ==========================================
# 3. CABECERA DE LA APLICACIÓN
# ==========================================
st.title("⚽ Clasificador de Posiciones IA")
st.markdown("""
Descubre cuál es la posición ideal de un jugador basándote en su rendimiento en el campo. 
Introduce sus estadísticas de la temporada y nuestro modelo de Machine Learning hará el resto.
""")
st.divider()

# Control de errores: Detener la ejecución limpiamente si no hay modelo disponible
if ml_model is None:
    st.error("⚠️ Modelo no encontrado. Asegúrate de que 'pipeline_futbolistico.pkl' está en la carpeta 'modelos'.")
    st.stop()

# ==========================================
# 4. INTERFAZ DE ENTRADA DE DATOS (FORMULARIO)
# ==========================================
# El uso de st.form asegura que la página no se recargue constantemente;
# agrupa todas las entradas y las envía juntas al pulsar el botón.
with st.form("prediction_form", border=True):
    
    # --- Sección 1: Datos de Participación ---
    st.subheader("📋 Datos Generales")
    c1, c2 = st.columns(2)
    with c1:
        games = st.number_input("Partidos jugados", min_value=1, max_value=100, value=25, step=1)
    with c2:
        time = st.number_input("Minutos jugados", min_value=1, max_value=9000, value=1800, step=10, 
                               help="Total de minutos en toda la temporada.")
    
    st.write("") # Espaciador visual

    # --- Sección 2: Métricas Ofensivas ---
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

    st.write("") 

    # --- Sección 3: Métricas Defensivas y Disciplinarias ---
    st.subheader("🛡️ Defensa y Disciplina")
    c6, c7, c8 = st.columns(3)
    with c6:
        tackles = st.number_input("Entradas con éxito", min_value=0, max_value=500, value=25, step=1)
    with c7:
        yellow_cards = st.number_input("Tarjetas Amarillas", min_value=0, max_value=30, value=3, step=1)
    with c8:
        red_cards = st.number_input("Tarjetas Rojas", min_value=0, max_value=10, value=0, step=1)

    st.write("")
    
    # Botón de envío que activa el procesamiento del bloque de formulario
    is_submitted = st.form_submit_button("🔍 Analizar Perfil del Jugador", use_container_width=True, type="primary")


# ==========================================
# 5. PROCESAMIENTO E INFERENCIA (MACHINE LEARNING)
# ==========================================
if is_submitted:
    with st.spinner("Analizando estadísticas con Inteligencia Artificial..."):
        
        # --- 5.1. Ingeniería de Características (Feature Engineering) ---
        # Normalización de estadísticas base dividiendo por el volumen de partidos
        tackles_per_game = tackles / games
        goals_per_game = goals / games
        assists_per_game = assists / games
        key_passes_per_game = key_passes / games
        
        # Estimación de partidos completos jugados (basado en bloques de 90 mins)
        full_matches = time / 90 if time > 0 else 0.1

        # Estimación algorítmica de métricas subyacentes avanzadas (Expected Goals/Assists)
        xG = shots * 0.10          
        xA = key_passes * 0.10      
        npxG = npg                  
        xGChain = xG + xA + (full_matches * 0.3) 
        xGBuildup = full_matches * 0.25          

        # --- 5.2. Preparación del Vector de Entrada ---
        # El orden y nombre de las columnas debe coincidir exactamente con el dataset de entrenamiento del pipeline
        feature_columns = [
            "games", "time", "goals", "xG", "assists", "xA", "shots", "key_passes", 
            "yellow_cards", "red_cards", "npg", "npxG", "xGChain", "xGBuildup", "tackles", "tackles_per_game", 
            "goals_per_game", "assists_per_game", "key_passes_per_game"
        ]
        
        input_data = pd.DataFrame([[
            games, time, goals, xG, assists, xA, shots, key_passes, 
            yellow_cards, red_cards, npg, npxG, xGChain, xGBuildup, tackles, tackles_per_game, 
            goals_per_game, assists_per_game, key_passes_per_game
        ]], columns=feature_columns)
        
        # Mapeo posicional del output numérico del modelo a etiquetas legibles
        target_positions = ["Defensa", "Portero", "Delantero", "Centrocampista", "Segundo delantero"]

        # --- 5.3. Predicción ---
        # .predict() devuelve la clase ganadora, .predict_proba() el array de probabilidades de todas las clases
        predicted_position_idx = ml_model.predict(input_data)[0]
        predicted_position = target_positions[predicted_position_idx]
        
        probs = ml_model.predict_proba(input_data)[0]
        max_prob = float(probs.max())

        # ==========================================
        # 6. VISUALIZACIÓN DE RESULTADOS Y REGISTRO GLOBAL
        # ==========================================
        st.divider()
        st.subheader("📊 Resultado del Análisis")
        
        # Mostrar KPIs de la inferencia
        res1, res2 = st.columns(2)
        res1.metric(label="Posición Recomendada", value=str(predicted_position))
        res2.metric(label="Nivel de Confianza (IA)", value=f"{max_prob:.1%}")

        # --- Construcción y almacenamiento del payload en la memoria de sesión ---
        analysis_record = {
            "id": len(st.session_state.history) + 1,
            "position": predicted_position,
            "confidence_str": f"{max_prob:.1%}",
            "confidence_num": max_prob, # Almacenado de forma numérica para permitir el filtrado matemático posterior
            "matches": games,
            "goals": goals,
            "stats": {
                "minutes": time,
                "npg": npg,
                "assists": assists,
                "shots": shots,
                "key_passes": key_passes,
                "tackles": tackles,
                "yellow_cards": yellow_cards,
                "red_cards": red_cards
            },
            "raw_probs": probs.tolist() # Se convierte el array numpy a lista estándar para evitar problemas de serialización
        }
        
        st.session_state.history.append(analysis_record)

        # Renderizado visual del gráfico de distribución
        st.markdown("**Distribución de probabilidad por posición:**")
        df_probs = pd.DataFrame({
            "Posición": target_positions, 
            "Probabilidad": probs
        })
        st.bar_chart(df_probs.set_index("Posición"), color="#1f77b4")