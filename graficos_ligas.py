import streamlit as st
import streamlit.components.v1 as components
import os

# ----------------------------
# CARGA DE ARCHIVOS HTML
# ----------------------------
@st.cache_data
def load_htmls():
    base_path = "graphics"  # Carpeta contenedora de los gráficos HTML

    html_files = {
        "🛡️ Ligas más defensivas": "Ligas_Mas_Defensivas.html",
        "⚽ Media de goles por partido según liga": "Media_Goles_Partido_Ligas.html",
        "🏆 Media de puntos por partido según liga": "Media_Puntos_Partidos_Ligas.html",
        "📊 Ratio de victorias/empates por liga": "Victorias_Empates_Por_Liga.html"
    }

    html_content = {}
    for key, file_name in html_files.items():
        file_path = os.path.join(base_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                html_content[key] = f.read()
        else:
            html_content[key] = None

    return html_content

# ----------------------------
# FUNCIÓN PARA GENERAR INSIGHTS AUTOMÁTICOS
# ----------------------------
def generate_insight(tab_name):
    """
    Retorna insights descriptivos rápidos para cada visualización de ligas.
    """
    if tab_name == "🛡️ Ligas más defensivas":
        return "Muestra cuáles ligas conceden menos goles por partido, destacando su solidez defensiva."
    elif tab_name == "⚽ Media de goles por partido según liga":
        return "Permite comparar qué ligas tienen partidos más ofensivos, con mayor promedio de goles."
    elif tab_name == "🏆 Media de puntos por partido según liga":
        return "Resalta la eficiencia de los equipos en cada liga en términos de puntos obtenidos por partido."
    elif tab_name == "📊 Ratio de victorias/empates por liga":
        return "Analiza el equilibrio entre victorias y empates en cada liga para detectar competitividad."
    return "Insight no disponible."

# ----------------------------
# INICIALIZACIÓN DE DATOS
# ----------------------------
html_data = load_htmls()

# ----------------------------
# INTERFAZ PRINCIPAL
# ----------------------------
st.title("📊 Visualizaciones gráficas de ligas")
st.markdown("""
Explora las principales métricas de rendimiento de las ligas: defensa, goles, puntos y ratios de victoria/empate.  
Cada visualización incluye un insight automático y la opción de descargar el gráfico en HTML.
""")

# ----------------------------
# GESTIÓN DE PESTAÑAS (TABS)
# ----------------------------
tab_names = list(html_data.keys())
ui_tabs = st.tabs(tab_names)

for i, current_tab_name in enumerate(tab_names):
    with ui_tabs[i]:
        st.subheader(current_tab_name)

        # Insight descriptivo dinámico
        st.info(generate_insight(current_tab_name))

        current_html = html_data[current_tab_name]

        if current_html is not None:
            # Renderizar el gráfico HTML incrustado
            components.html(current_html, height=800, scrolling=True)

            # Botón de descarga para el usuario
            st.download_button(
                label="💾 Descargar gráfico HTML",
                data=current_html,
                file_name=f"{current_tab_name.replace(' ', '_')}.html",
                mime="text/html"
            )
        else:
            st.warning("No se encontró el archivo HTML")