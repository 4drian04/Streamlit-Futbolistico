import streamlit as st
import streamlit.components.v1 as components

# Configuración de la vista del dashboard
st.set_page_config(page_title="Dashboards", layout="wide", page_icon="🖥️")

# URLs optimizadas para la incrustación desde Tableau Public
tableau_dashboards = {
    "Estadísticas equipos I": "https://public.tableau.com/views/3_2_GarciaGarcia_CaraballoBulnes/Dashboard1?:embed=y&:showVizHome=no",
    "Estadísticas Extremos": "https://public.tableau.com/views/3_2_GarciaGarcia_CaraballoBulnes/Dashboard2?:embed=y&:showVizHome=no",
    "Estadísticas equipos II": "https://public.tableau.com/views/3_2_GarciaGarcia_CaraballoBulnes/Dashboard3?:embed=y&:showVizHome=no"
}

# Tamaños verticales dinámicos según el dashboard requerido
iframe_heights = {
    "Estadísticas equipos I": 800,
    "Estadísticas Extremos": 800,
    "Estadísticas equipos II": 1800  # Formato más extendido
}

# Bloques de texto descriptivos
descriptions = {
    "Estadísticas equipos I": """
    Este panel muestra un análisis comparativo del rendimiento de equipos y ligas de fútbol a partir de métricas ofensivas, defensivas y de eficiencia.

    1. Goles de diferencia por partido
    Se observa cuánto supera (o queda por debajo) cada equipo a sus rivales en promedio por partido.

    - Valores positivos indican equipos dominantes.
    - Valores negativos reflejan equipos con más goles en contra que a favor.

    2. Equipos eficientes (goles vs puntos)
    Este gráfico relaciona la diferencia de goles con los puntos obtenidos por partido.

    - La línea indica la tendencia general: a mayor diferencia de goles, más puntos.
    - Equipos por encima de la línea son más eficientes (consiguen más puntos con menor diferencia).
    - Equipos por debajo rinden menos de lo esperado.

    3. Equipos: ataque vs defensa
    Cada punto representa un equipo según:

    - Ataque: goles a favor por partido (eje X).
    - Defensa: goles en contra por partido (eje Y).
    Las líneas marcan el promedio general:
    - Abajo a la derecha → equipos fuertes (buen ataque y buena defensa).
    - Arriba a la izquierda → equipos con debilidades en ambas áreas.

    4. Ligas más defensivas
    Comparación entre ligas según el promedio de goles concedidos.

    - Valores más bajos indican ligas más defensivas.
    - Permite identificar estilos de juego predominantes por competición.
    """,
    "Estadísticas Extremos": """
    Este panel destaca a jugadores con valores extremos en métricas ofensivas y de comportamiento en el juego, permitiendo identificar perfiles muy productivos o intensos.

    1. Goles y asistencias (extremos)
    Se comparan jugadores con cifras destacadas en contribución ofensiva:

    - Las barras muestran el número de goles y asistencias de cada jugador.
    - Permite distinguir perfiles:
        - Jugadores finalizadores (más goles que asistencias).
        - Jugadores creadores (más asistencias que goles).
        - Jugadores completos (equilibrio en ambas métricas).

    2. Faltas por partido (extremos)
    Este gráfico muestra los jugadores que más faltas cometen por partido:

    - Valores más altos indican un estilo de juego más físico o agresivo.
    - También puede reflejar roles tácticos (presión alta, recuperación de balón).

    3. Tabla completa
    Por último, se muestra una tabla que reune todos los datos anteriores de forma resumida
    """,
    "Estadísticas equipos II": """
    Este panel ofrece una visión comparativa del estilo de juego entre ligas y del rendimiento ofensivo según la nacionalidad de los jugadores.

    1. Media de goles por partido por liga

    Este gráfico muestra cuántos goles se anotan en promedio en cada liga:

    - Valores más altos indican competiciones más ofensivas y abiertas.
    - Valores más bajos reflejan ligas más tácticas o defensivas.

    2. Porcentaje de empates por liga

    Se representa la proporción de partidos que terminan en empate:

    - Un porcentaje alto sugiere ligas más equilibradas o con menor diferencia entre equipos.
    - Un porcentaje bajo indica mayor presencia de resultados definidos (victorias/derrotas).

    3. Media de goles por nacionalidad

    El mapa muestra el promedio de goles anotados por jugadores según su país de origen:

    - Permite identificar qué nacionalidades destacan más en producción ofensiva.
    - También refleja posibles tendencias formativas o estilos de juego por región.

    4. Media de puntos por partido (gráfico circular)

    Muestra el promedio de puntos que obtienen los equipos en cada liga. Permite comparar rápidamente qué ligas son más competitivas o tienen mayor rendimiento promedio.

    5. Porcentaje de victorias por liga (gráfico circular)

    Representa la proporción de partidos ganados en cada liga. Es útil para identificar diferencias en el equilibrio competitivo o la frecuencia de empates.

    6. Edad media de las plantillas por equipo (gráfico de cajas)

    Este gráfico detalla la distribución de edades de los jugadores en cada equipo:

    - La línea central indica la mediana de edad.
    - La caja muestra el rango intercuartílico (la mayoría de jugadores).
    - Los extremos reflejan edades mínimas y máximas.
    """
}

# Título de la sección
st.title("Dashboards de Tableau")

# Crear y estructurar pestañas
dashboard_names = list(tableau_dashboards.keys())
ui_tabs = st.tabs(dashboard_names)

# Incrustar el iFrame correspondiente dentro de cada pestaña
for i, current_tab_name in enumerate(dashboard_names):
    with ui_tabs[i]:
        st.subheader(current_tab_name)
        if current_tab_name in descriptions:
            with st.expander("¿Qué estás viendo?", expanded=False):
                st.markdown(descriptions[current_tab_name])

        target_url = tableau_dashboards[current_tab_name]
        
        # Renderizado del componente iFrame de Tableau
        components.iframe(target_url, height=iframe_heights[current_tab_name])