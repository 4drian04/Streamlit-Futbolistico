# ⚽ Football Scouting IA & Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E.svg)
![Tableau](https://img.shields.io/badge/Tableau-Dashboards-E97627.svg)

Una aplicación web interactiva desarrollada en **Streamlit** diseñada para el análisis avanzado de datos futbolísticos y el *scouting* inteligente. Esta herramienta permite explorar estadísticas de equipos y jugadores, visualizar métricas clave en gráficos y dashboards de Tableau, y utilizar **Machine Learning** para predecir la posición ideal de un jugador basándose en su rendimiento en el campo.

## 📝 Descripción

El proyecto se divide en dos grandes bloques:
1. **Analítica Descriptiva (Business Intelligence):** Tablas filtrables, gráficos HTML generados (vía Plotly u otras librerías) e integración directa con dashboards de Tableau para evaluar el rendimiento de ligas, equipos y jugadores extremos.
2. **Analítica Predictiva (Inteligencia Artificial):** Un pipeline de Machine Learning (Random Forest) que toma estadísticas avanzadas (xG, xA, entradas, etc.) e infiere la posición natural de un jugador, guardando un historial de sesión interactivo para comparar distintos perfiles.

## ✨ Características Principales

* **📊 Explorador de Tablas:** Consulta de datos brutos y filtrados de equipos (ataque/defensa, ligas) y jugadores (edad, nacionalidad, rendimiento).
* **📈 Visualizaciones Nativas:** Gráficos pre-renderizados en HTML interactivo con capacidad de descarga e *insights* (conclusiones) generados automáticamente.
* **🖥️ Dashboards de Tableau:** Integración de paneles de Tableau Public embebidos directamente en la aplicación para una experiencia de Business Intelligence completa.
* **🤖 Scouting IA:** Formulario de entrada de estadísticas que procesa métricas avanzadas y utiliza un modelo de IA pre-entrenado para clasificar posiciones (Defensa, Portero, Delantero, Centrocampista, Segundo delantero).
* **📜 Historial Inteligente:** Sistema de paginación, ordenación y filtrado (por posición y confianza de la IA) del historial de predicciones realizadas durante la sesión.

## 🛠️ Tecnologías Utilizadas

* **Frontend/Backend:** [Streamlit](https://streamlit.io/) (Python)
* **Manipulación de Datos:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn (`RandomForestClassifier`, `PolynomialFeatures`, `Pipeline`)
* **Visualización:** Plotly (HTML renderizado), Streamlit Components, Tableau Public

## 📁 Estructura del Proyecto

[AQUÍ VA LA ESTRUCTURA DEL PROYECTO]
football-scouting-ia
 |— data_input/           # Datasets CSV con estadísticas (equipos, jugadores, ligas)
 |— graphics/             # Gráficos exportados en formato HTML
 |— modelos/              # Modelos de Machine Learning serializados
 |   |— pipeline_futbolistico.pkl
 |— app.py                # Archivo principal y menú de navegación
 |— tabla_equipos.py      # Vista de datos tabulares de equipos
 |— tabla_jugadores.py    # Vista de datos tabulares de jugadores
 |— graficos_equipos.py   # Visualización e insights de equipos
 |— graficos_ligas.py     # Visualización e insights de ligas
 |— graficos_jugadores.py # Visualización e insights de jugadores
 |— tableau_dashboard.py  # Integración de Dashboards de Tableau
 |— prediccion.py         # Interfaz de IA y motor de predicción
 |— historial.py          # Gestión y vista del historial de predicciones
 |— train.py              # Script de entrenamiento del modelo de ML

## 🚀 Instalación y Uso

1. **Clona el repositorio:**
   git clone https://github.com/TU_USUARIO/football-scouting-ia.git
   cd football-scouting-ia

2. **Crea un entorno virtual (Recomendado):**
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate

3. **Instala las dependencias:**
   (Asegúrate de tener un archivo `requirements.txt` o instala manualmente las librerías base)
   pip install streamlit pandas numpy scikit-learn joblib

4. **Entrena el modelo (Opcional, si no tienes el archivo `.pkl`):**
   Si necesitas generar el archivo del modelo desde cero usando tus datos en `data_input/`:
   python train.py

5. **Ejecuta la aplicación:**
   streamlit run app.py

## 🤖 Sobre el Modelo de Machine Learning

El archivo `train.py` contiene el flujo de trabajo de entrenamiento. Utiliza un `Pipeline` de Scikit-Learn que combina:
1. **PolynomialFeatures (degree=2):** Para capturar relaciones no lineales y sinergias entre las distintas estadísticas del jugador.
2. **RandomForestClassifier:** Configurado con pesos balanceados (`class_weight="balanced"`), profundidad máxima ajustada y regularización para prevenir el sobreajuste (*overfitting*).

Se ha aplicado ingeniería de características (*Feature Engineering*) para normalizar métricas a base "por partido" (ej. *tackles_per_game*, *goals_per_game*), mejorando la precisión del clasificador sin importar si el jugador ha disputado 10 o 35 partidos.