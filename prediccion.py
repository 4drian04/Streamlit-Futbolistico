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
if "historial" not in st.session_state:
    st.session_state.historial = []

# ==========================================
# 2. CARGA DEL MODELO PREDICTIVO
# ==========================================
@st.cache_resource
def cargar_modelo():
    """
    Carga el modelo de Machine Learning desde el sistema de archivos local.
    Usa el decorador @st.cache_resource para evitar cargar el archivo .pkl 
    repetidamente con cada interacción del usuario, mejorando el rendimiento.
    """
    ruta = Path("modelos/pipeline_futbolistico.pkl")
    if not ruta.exists():
        return None
    return joblib.load(ruta)

modelo = cargar_modelo()

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
if modelo is None:
    st.error("⚠️ Modelo no encontrado. Asegúrate de que 'pipeline_futbolistico.pkl' está en la carpeta 'modelos'.")
    st.stop()

# ==========================================
# 4. INTERFAZ DE ENTRADA DE DATOS (FORMULARIO)
# ==========================================
# El uso de st.form asegura que la página no se recargue constantemente;
# agrupa todas las entradas y las envía juntas al pulsar el botón.
with st.form("prediccion_form", border=True):
    
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
    enviado = st.form_submit_button("🔍 Analizar Perfil del Jugador", use_container_width=True, type="primary")


# ==========================================
# 5. PROCESAMIENTO E INFERENCIA (MACHINE LEARNING)
# ==========================================
if enviado:
    with st.spinner("Analizando estadísticas con Inteligencia Artificial..."):
        
        # --- 5.1. Ingeniería de Características (Feature Engineering) ---
        # Normalización de estadísticas base dividiendo por el volumen de partidos
        tackles_per_game = tackles / games
        goals_per_game = goals / games
        assists_per_game = assists / games
        key_passes_per_game = key_passes / games
        
        # Estimación de partidos completos jugados (basado en bloques de 90 mins)
        partidos_completos = time / 90 if time > 0 else 0.1

        # Estimación algorítmica de métricas subyacentes avanzadas (Expected Goals/Assists)
        xG = shots * 0.10          
        xA = key_passes * 0.10      
        npxG = npg                  
        xGChain = xG + xA + (partidos_completos * 0.3) 
        xGBuildup = partidos_completos * 0.25          

        # --- 5.2. Preparación del Vector de Entrada ---
        # El orden y nombre de las columnas debe coincidir exactamente con el dataset de entrenamiento del pipeline
        columnas = [
            "games", "time", "goals", "xG", "assists", "xA", "shots", "key_passes", 
            "yellow_cards", "red_cards", "npg", "npxG", "xGChain", "xGBuildup", "tackles", "tackles_per_game", 
            "goals_per_game", "assists_per_game", "key_passes_per_game"
        ]
        
        X = pd.DataFrame([[
            games, time, goals, xG, assists, xA, shots, key_passes, 
            yellow_cards, red_cards, npg, npxG, xGChain, xGBuildup, tackles, tackles_per_game, 
            goals_per_game, assists_per_game, key_passes_per_game
        ]], columns=columnas)
        
        # Mapeo posicional del output numérico del modelo a etiquetas legibles
        posiciones = ["Defensa", "Portero", "Delantero", "Centrocampista", "Segundo delantero"]

        # --- 5.3. Predicción ---
        # .predict() devuelve la clase ganadora, .predict_proba() el array de probabilidades de todas las clases
        posicion_idx = modelo.predict(X)[0]
        posicion_predicha = posiciones[posicion_idx]
        
        probas = modelo.predict_proba(X)[0]
        proba_maxima = float(probas.max())

        # ==========================================
        # 6. VISUALIZACIÓN DE RESULTADOS Y REGISTRO GLOBAL
        # ==========================================
        st.divider()
        st.subheader("📊 Resultado del Análisis")
        
        # Mostrar KPIs de la inferencia
        res1, res2 = st.columns(2)
        res1.metric(label="Posición Recomendada", value=str(posicion_predicha))
        res2.metric(label="Nivel de Confianza (IA)", value=f"{proba_maxima:.1%}")

        # --- Construcción y almacenamiento del payload en la memoria de sesión ---
        registro_analisis = {
            "ID": len(st.session_state.historial) + 1,
            "Posición": posicion_predicha,
            "Confianza_str": f"{proba_maxima:.1%}",
            "Confianza_num": proba_maxima, # Almacenado de forma numérica para permitir el filtrado matemático posterior
            "Partidos": games,
            "Goles": goals,
            "Estadísticas": {
                "Minutos": time,
                "Goles (Sin Penalti)": npg,
                "Asistencias": assists,
                "Tiros Totales": shots,
                "Pases Clave": key_passes,
                "Entradas": tackles,
                "Amarillas": yellow_cards,
                "Rojas": red_cards
            },
            "Probas_crudas": probas.tolist() # Se convierte el array numpy a lista estándar para evitar problemas de serialización
        }
        
        st.session_state.historial.append(registro_analisis)

        # Renderizado visual del gráfico de distribución
        st.markdown("**Distribución de probabilidad por posición:**")
        df_probas = pd.DataFrame({
            "Posición": posiciones, 
            "Probabilidad": probas
        })
        st.bar_chart(df_probas.set_index("Posición"), color="#1f77b4")