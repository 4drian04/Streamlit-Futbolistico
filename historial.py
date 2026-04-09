"""
Módulo: historial.py
Descripción: Página de Streamlit que gestiona la visualización, filtrado y 
análisis del historial de predicciones realizadas por el modelo de Scouting IA.
Incluye paginación dinámica y renderizado de gráficos bajo demanda.
"""

import streamlit as st
import pandas as pd
import math

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Historial de Scouting", layout="wide", page_icon="📜")

st.title("📜 Historial de Análisis")
st.markdown("Consulta y filtra todas las predicciones realizadas durante esta sesión.")


# ==========================================
# 2. GESTIÓN DEL ESTADO DE SESIÓN (STATE)
# ==========================================
# Inicialización de variables para mantener el estado entre recargas de página
if "current_page" not in st.session_state:
    st.session_state.current_page = 1

if "confidence_slider" not in st.session_state:
    st.session_state.confidence_slider = 0.0

if "confidence_num" not in st.session_state:
    st.session_state.confidence_num = 0.0


# ==========================================
# 3. FUNCIONES CALLBACK (EVENTOS)
# ==========================================
def sync_from_slider():
    """Sincroniza el input numérico cuando se mueve el slider y resetea la paginación."""
    st.session_state.confidence_num = st.session_state.confidence_slider
    st.session_state.current_page = 1

def sync_from_num():
    """Sincroniza el slider cuando se modifica el input numérico y resetea la paginación."""
    st.session_state.confidence_slider = st.session_state.confidence_num
    st.session_state.current_page = 1

def reset_page():
    """Devuelve la vista a la primera página. Usado al cambiar cualquier filtro."""
    st.session_state.current_page = 1


# ==========================================
# 4. RENDERIZADO PRINCIPAL DE LA APP
# ==========================================
# Verificación de existencia de datos en el historial
if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.info("Aún no se han realizado predicciones en esta sesión. Ve a la pestaña de 'Predicción' para analizar a un jugador.")
else:
    # --- KPI General ---
    st.metric(label="Predicciones totales en esta sesión", value=len(st.session_state.history))
    st.divider()

    # --- Panel de Filtros ---
    st.subheader("⚙️ Filtros")
    
    # Distribución de columnas para los filtros
    f1, f2, f3 = st.columns([1, 1, 1.5]) 
    
    with f1:
        sort_order = st.selectbox("Ordenar por:", [
            "Más recientes primero", 
            "Más antiguos primero", 
            "Mayor confianza", 
            "Menor confianza"
        ], on_change=reset_page)
    
    with f2:
        unique_positions = ["Todas"] + ["Defensa", "Portero", "Delantero", "Centrocampista", "Segundo delantero"]
        pos_filter = st.selectbox("Filtrar por Posición:", unique_positions, on_change=reset_page)
        
    with f3:
        st.markdown("**Confianza mínima requerida (%)**")
        col_slider, col_num = st.columns([3, 1])
        
        with col_slider:
            st.slider("Confianza", min_value=0.0, max_value=100.0, step=0.1, 
                      key="confidence_slider", label_visibility="collapsed", on_change=sync_from_slider)
        
        with col_num:
            st.number_input("Confianza num", min_value=0.0, max_value=100.0, step=0.1, format="%.1f", 
                            key="confidence_num", label_visibility="collapsed", on_change=sync_from_num)

    # ==========================================
    # 5. PROCESAMIENTO DE DATOS (FILTRADO Y ORDEN)
    # ==========================================
    # Clonamos la lista original para no mutar el estado global
    data_to_show = list(st.session_state.history)
    
    # Aplicar filtro por posición categórica
    if pos_filter != "Todas":
        data_to_show = [d for d in data_to_show if d["position"] == pos_filter]
        
    # Aplicar filtro por umbral de confianza (ambas variables de sesión son idénticas aquí)
    confidence_limit = st.session_state.confidence_slider / 100.0
    data_to_show = [d for d in data_to_show if d["confidence_num"] >= confidence_limit]
    
    # Aplicar criterio de ordenación seleccionado
    if sort_order == "Más recientes primero":
        data_to_show.sort(key=lambda x: x["id"], reverse=True)
    elif sort_order == "Más antiguos primero":
        data_to_show.sort(key=lambda x: x["id"], reverse=False)
    elif sort_order == "Mayor confianza":
        data_to_show.sort(key=lambda x: x["confidence_num"], reverse=True)
    elif sort_order == "Menor confianza":
        data_to_show.sort(key=lambda x: x["confidence_num"], reverse=False)

    # ==========================================
    # 6. MOTOR DE PAGINACIÓN MATEMÁTICA
    # ==========================================
    ITEMS_PER_PAGE = 10
    total_items = len(data_to_show)
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE) if total_items > 0 else 1

    # Control de seguridad: Si los filtros reducen las páginas por debajo de la actual
    if st.session_state.current_page > total_pages:
        st.session_state.current_page = total_pages

    # Extracción del subset de datos correspondiente a la página actual
    start_idx = (st.session_state.current_page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_data = data_to_show[start_idx:end_idx]

    # --- Resumen de resultados ---
    st.write("") 
    if total_items > 0:
        st.markdown(f"**Mostrando resultados {start_idx + 1} al {min(end_idx, total_items)} de {total_items}**")
    else:
        st.markdown("**No hay resultados que coincidan con los filtros.**")

    # ==========================================
    # 7. INTERFAZ DE TABLA DE RESULTADOS
    # ==========================================
    # Encabezados de la tabla pseudo-nativa
    h1, h2, h3, h4, h5 = st.columns([1, 2, 2, 2, 2])
    h1.markdown("**ID**")
    h2.markdown("**Posición Predicha**")
    h3.markdown("**Confianza**")
    h4.markdown("**Partidos Jugados**")
    h5.markdown("**Acción**")
    
    # Generación iterativa de las filas
    for record in page_data:
        c1, c2, c3, c4, c5 = st.columns([1, 2, 2, 2, 2])
        
        c1.write(f"#{record['id']}")
        c2.write(record["position"])
        c3.write(record["confidence_str"])
        c4.write(record["matches"])
        
        # Botón para inyectar el ID seleccionado en la sesión y renderizar el detalle
        if c5.button("📊 Ver detalles", key=f"btn_graph_{record['id']}"):
            st.session_state.selected_graph_id = record["id"]

    st.divider()

    # ==========================================
    # 8. COMPONENTES VISUALES DE PAGINACIÓN
    # ==========================================
    if total_pages > 1:
        
        def generate_page_list(current, total):
            """Genera la estructura de visualización de botones numéricos con elipsis ('...')."""
            if total <= 4:
                return list(range(1, total + 1))

            start = min(current, total - 3)
            if start < 1:
                start = 1
                
            end = start + 3
            res = []
            
            if start >= 3:
                res.extend([1, '...'])
            
            for i in range(start, end + 1):
                res.append(i)

            if end < total - 1:
                res.extend(['...', total])
            elif end == total - 1:
                res.append(total)

            return res

        pages_to_show = generate_page_list(st.session_state.current_page, total_pages)
        
        # Configuración de espaciados relativos para centrar la botonera
        proportions = [3, 1.2] + [0.7] * len(pages_to_show) + [1.2, 3]
        pagination_columns = st.columns(proportions)
        
        # Botón "Anterior"
        with pagination_columns[1]:
            if st.button("⬅️", use_container_width=True, disabled=(st.session_state.current_page == 1)):
                st.session_state.current_page -= 1
                st.rerun()
                
        # Iteración de botones numéricos y elipsis
        for i, pag in enumerate(pages_to_show):
            with pagination_columns[i + 2]:
                if pag == '...':
                    st.markdown("<div style='text-align: center; padding-top: 5px; font-weight: bold; color: gray;'>...</div>", unsafe_allow_html=True)
                else:
                    # Resalta el botón de la página actual
                    btn_type = "primary" if pag == st.session_state.current_page else "secondary"
                    if st.button(str(pag), key=f"btn_page_{pag}", type=btn_type, use_container_width=True):
                        st.session_state.current_page = pag
                        st.rerun()
                        
        # Botón "Siguiente"
        with pagination_columns[-2]:
            if st.button("➡️", use_container_width=True, disabled=(st.session_state.current_page == total_pages)):
                st.session_state.current_page += 1
                st.rerun()
                
    st.divider()

    # ==========================================
    # 9. VISTA DE DETALLE Y GRÁFICO (MODAL SIMULADO)
    # ==========================================
    if "selected_graph_id" in st.session_state:
        # Búsqueda O(N) del registro exacto por su ID único
        target_id = st.session_state.selected_graph_id
        selected_record = next((item for item in st.session_state.history if item["id"] == target_id), None)
        
        if selected_record:
            stats = selected_record["stats"] 
            
            st.subheader(f"🔍 Detalle de la Predicción #{selected_record['id']}")
            
            # --- KPIs Específicos del Jugador ---
            st.markdown("**Estadísticas analizadas:**")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Partidos", selected_record["matches"])
            m2.metric("Minutos", stats["minutes"])
            m3.metric("Goles Totales", selected_record["goals"])
            m4.metric("Goles (Sin Penalti)", stats["npg"])
            
            m5, m6, m7, m8 = st.columns(4)
            m5.metric("Asistencias", stats["assists"])
            m6.metric("Tiros Totales", stats["shots"])
            m7.metric("Pases Clave", stats["key_passes"])
            m8.metric("Entradas", stats["tackles"])
            
            # --- Visualización del Gráfico de Probabilidades ---
            st.write("") 
            st.markdown(f"**Resultado:** {selected_record['position']} ({selected_record['confidence_str']})")
            
            target_positions = ["Defensa", "Portero", "Delantero", "Centrocampista", "Segundo delantero"]
            df_probs = pd.DataFrame({
                "Posición": target_positions, 
                "Probabilidad": selected_record["raw_probs"]
            })
            
            st.bar_chart(df_probs.set_index("Posición"), color="#1f77b4")
            
            # Botón para cerrar el detalle y limpiar el estado
            if st.button("❌ Cerrar detalle"):
                del st.session_state.selected_graph_id
                st.rerun()

    # ==========================================
    # 10. ZONA DE PELIGRO (LIMPIEZA DE DATOS)
    # ==========================================
    st.write("")
    if st.button("🗑️ Borrar todo el historial", type="primary"):
        # Reseteo completo del estado global del historial y variables de interfaz
        st.session_state.history = []
        st.session_state.current_page = 1
        st.session_state.confidence_slider = 0.0
        st.session_state.confidence_num = 0.0
        if "selected_graph_id" in st.session_state:
            del st.session_state.selected_graph_id
        st.rerun()