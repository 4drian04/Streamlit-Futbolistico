# tabla_html.py
import streamlit as st
import streamlit.components.v1 as components
import os

# ----------------------------
# CARGA DE HTMLs
# ----------------------------
@st.cache_data
def load_htmls():
    base_path = "graphics"  # Carpeta donde están los HTML

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
# FUNCION PARA GENERAR INSIGHT AUTOMÁTICO
# ----------------------------
def generar_insight(tab_name):
    """
    Insights rápidos para cada visualización de ligas.
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
# CARGAR HTMLs
# ----------------------------
data = load_htmls()

# ----------------------------
# CABECERA DEL DASHBOARD
# ----------------------------
st.title("📊 Visualizaciones gráficas de ligas")
st.markdown("""
Explora las principales métricas de rendimiento de las ligas: defensa, goles, puntos y ratios de victoria/empate.  
Cada visualización incluye un insight automático y la opción de descargar el gráfico en HTML.
""")

# ----------------------------
# CREAR TABS
# ----------------------------
tab_names = list(data.keys())
tabs = st.tabs(tab_names)

for i, tab_name in enumerate(tab_names):
    with tabs[i]:
        st.subheader(tab_name)

        # Insight dinámico
        st.info(generar_insight(tab_name))

        html = data[tab_name]

        if html is not None:
            # Mostrar HTML
            components.html(html, height=800, scrolling=True)

            # Botón para descargar
            st.download_button(
                label="💾 Descargar gráfico HTML",
                data=html,
                file_name=f"{tab_name.replace(' ', '_')}.html",
                mime="text/html"
            )
        else:
            st.warning("No se encontró el archivo HTML")