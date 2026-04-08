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
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = 1

if "confianza_slider" not in st.session_state:
    st.session_state.confianza_slider = 0.0

if "confianza_num" not in st.session_state:
    st.session_state.confianza_num = 0.0


# ==========================================
# 3. FUNCIONES CALLBACK (EVENTOS)
# ==========================================
def sync_from_slider():
    """Sincroniza el input numérico cuando se mueve el slider y resetea la paginación."""
    st.session_state.confianza_num = st.session_state.confianza_slider
    st.session_state.pagina_actual = 1

def sync_from_num():
    """Sincroniza el slider cuando se modifica el input numérico y resetea la paginación."""
    st.session_state.confianza_slider = st.session_state.confianza_num
    st.session_state.pagina_actual = 1

def reset_pagina():
    """Devuelve la vista a la primera página. Usado al cambiar cualquier filtro."""
    st.session_state.pagina_actual = 1


# ==========================================
# 4. RENDERIZADO PRINCIPAL DE LA APP
# ==========================================
# Verificación de existencia de datos en el historial
if "historial" not in st.session_state or len(st.session_state.historial) == 0:
    st.info("Aún no se han realizado predicciones en esta sesión. Ve a la pestaña de 'Predicción' para analizar a un jugador.")
else:
    # --- KPI General ---
    st.metric(label="Predicciones totales en esta sesión", value=len(st.session_state.historial))
    st.divider()

    # --- Panel de Filtros ---
    st.subheader("⚙️ Filtros")
    
    # Distribución de columnas para los filtros
    f1, f2, f3 = st.columns([1, 1, 1.5]) 
    
    with f1:
        orden = st.selectbox("Ordenar por:", [
            "Más recientes primero", 
            "Más antiguos primero", 
            "Mayor confianza", 
            "Menor confianza"
        ], on_change=reset_pagina)
    
    with f2:
        posiciones_unicas = ["Todas"] + ["Defensa", "Portero", "Delantero", "Centrocampista", "Segundo delantero"]
        filtro_pos = st.selectbox("Filtrar por Posición:", posiciones_unicas, on_change=reset_pagina)
        
    with f3:
        st.markdown("**Confianza mínima requerida (%)**")
        col_slider, col_num = st.columns([3, 1])
        
        with col_slider:
            st.slider("Confianza", min_value=0.0, max_value=100.0, step=0.1, 
                      key="confianza_slider", label_visibility="collapsed", on_change=sync_from_slider)
        
        with col_num:
            st.number_input("Confianza num", min_value=0.0, max_value=100.0, step=0.1, format="%.1f", 
                            key="confianza_num", label_visibility="collapsed", on_change=sync_from_num)

    # ==========================================
    # 5. PROCESAMIENTO DE DATOS (FILTRADO Y ORDEN)
    # ==========================================
    # Clonamos la lista original para no mutar el estado global
    datos_mostrar = list(st.session_state.historial)
    
    # Aplicar filtro por posición categórica
    if filtro_pos != "Todas":
        datos_mostrar = [d for d in datos_mostrar if d["Posición"] == filtro_pos]
        
    # Aplicar filtro por umbral de confianza (ambas variables de sesión son idénticas aquí)
    limite_confianza = st.session_state.confianza_slider / 100.0
    datos_mostrar = [d for d in datos_mostrar if d["Confianza_num"] >= limite_confianza]
    
    # Aplicar criterio de ordenación seleccionado
    if orden == "Más recientes primero":
        datos_mostrar.sort(key=lambda x: x["ID"], reverse=True)
    elif orden == "Más antiguos primero":
        datos_mostrar.sort(key=lambda x: x["ID"], reverse=False)
    elif orden == "Mayor confianza":
        datos_mostrar.sort(key=lambda x: x["Confianza_num"], reverse=True)
    elif orden == "Menor confianza":
        datos_mostrar.sort(key=lambda x: x["Confianza_num"], reverse=False)

    # ==========================================
    # 6. MOTOR DE PAGINACIÓN MATEMÁTICA
    # ==========================================
    ITEMS_POR_PAGINA = 10
    total_items = len(datos_mostrar)
    total_paginas = math.ceil(total_items / ITEMS_POR_PAGINA) if total_items > 0 else 1

    # Control de seguridad: Si los filtros reducen las páginas por debajo de la actual
    if st.session_state.pagina_actual > total_paginas:
        st.session_state.pagina_actual = total_paginas

    # Extracción del subset de datos correspondiente a la página actual
    inicio = (st.session_state.pagina_actual - 1) * ITEMS_POR_PAGINA
    fin = inicio + ITEMS_POR_PAGINA
    datos_pagina = datos_mostrar[inicio:fin]

    # --- Resumen de resultados ---
    st.write("") 
    if total_items > 0:
        st.markdown(f"**Mostrando resultados {inicio + 1} al {min(fin, total_items)} de {total_items}**")
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
    for registro in datos_pagina:
        c1, c2, c3, c4, c5 = st.columns([1, 2, 2, 2, 2])
        
        c1.write(f"#{registro['ID']}")
        c2.write(registro["Posición"])
        c3.write(registro["Confianza_str"])
        c4.write(registro["Partidos"])
        
        # Botón para inyectar el ID seleccionado en la sesión y renderizar el detalle
        if c5.button("📊 Ver detalles", key=f"btn_grafico_{registro['ID']}"):
            st.session_state.grafico_seleccionado_id = registro["ID"]

    st.divider()

    # ==========================================
    # 8. COMPONENTES VISUALES DE PAGINACIÓN
    # ==========================================
    if total_paginas > 1:
        
        def generar_lista_paginas(actual, total):
            """Genera la estructura de visualización de botones numéricos con elipsis ('...')."""
            if total <= 4:
                return list(range(1, total + 1))

            start = min(actual, total - 3)
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

        paginas_a_mostrar = generar_lista_paginas(st.session_state.pagina_actual, total_paginas)
        
        # Configuración de espaciados relativos para centrar la botonera
        proporciones = [3, 1.2] + [0.7] * len(paginas_a_mostrar) + [1.2, 3]
        columnas_paginacion = st.columns(proporciones)
        
        # Botón "Anterior"
        with columnas_paginacion[1]:
            if st.button("⬅️", use_container_width=True, disabled=(st.session_state.pagina_actual == 1)):
                st.session_state.pagina_actual -= 1
                st.rerun()
                
        # Iteración de botones numéricos y elipsis
        for i, pag in enumerate(paginas_a_mostrar):
            with columnas_paginacion[i + 2]:
                if pag == '...':
                    st.markdown("<div style='text-align: center; padding-top: 5px; font-weight: bold; color: gray;'>...</div>", unsafe_allow_html=True)
                else:
                    # Resalta el botón de la página actual
                    tipo_btn = "primary" if pag == st.session_state.pagina_actual else "secondary"
                    if st.button(str(pag), key=f"btn_pag_{pag}", type=tipo_btn, use_container_width=True):
                        st.session_state.pagina_actual = pag
                        st.rerun()
                        
        # Botón "Siguiente"
        with columnas_paginacion[-2]:
            if st.button("➡️", use_container_width=True, disabled=(st.session_state.pagina_actual == total_paginas)):
                st.session_state.pagina_actual += 1
                st.rerun()
                
    st.divider()

    # ==========================================
    # 9. VISTA DE DETALLE Y GRÁFICO (MODAL SIMULADO)
    # ==========================================
    if "grafico_seleccionado_id" in st.session_state:
        # Búsqueda O(N) del registro exacto por su ID único
        id_buscado = st.session_state.grafico_seleccionado_id
        registro_sel = next((item for item in st.session_state.historial if item["ID"] == id_buscado), None)
        
        if registro_sel:
            stats = registro_sel["Estadísticas"] 
            
            st.subheader(f"🔍 Detalle de la Predicción #{registro_sel['ID']}")
            
            # --- KPIs Específicos del Jugador ---
            st.markdown("**Estadísticas analizadas:**")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Partidos", registro_sel["Partidos"])
            m2.metric("Minutos", stats["Minutos"])
            m3.metric("Goles Totales", registro_sel["Goles"])
            m4.metric("Goles (Sin Penalti)", stats["Goles (Sin Penalti)"])
            
            m5, m6, m7, m8 = st.columns(4)
            m5.metric("Asistencias", stats["Asistencias"])
            m6.metric("Tiros Totales", stats["Tiros Totales"])
            m7.metric("Pases Clave", stats["Pases Clave"])
            m8.metric("Entradas", stats["Entradas"])
            
            # --- Visualización del Gráfico de Probabilidades ---
            st.write("") 
            st.markdown(f"**Resultado:** {registro_sel['Posición']} ({registro_sel['Confianza_str']})")
            
            posiciones = ["Defensa", "Portero", "Delantero", "Centrocampista", "Segundo delantero"]
            df_probas = pd.DataFrame({
                "Posición": posiciones, 
                "Probabilidad": registro_sel["Probas_crudas"]
            })
            
            st.bar_chart(df_probas.set_index("Posición"), color="#1f77b4")
            
            # Botón para cerrar el detalle y limpiar el estado
            if st.button("❌ Cerrar detalle"):
                del st.session_state.grafico_seleccionado_id
                st.rerun()

    # ==========================================
    # 10. ZONA DE PELIGRO (LIMPIEZA DE DATOS)
    # ==========================================
    st.write("")
    if st.button("🗑️ Borrar todo el historial", type="primary"):
        # Reseteo completo del estado global del historial y variables de interfaz
        st.session_state.historial = []
        st.session_state.pagina_actual = 1
        st.session_state.confianza_slider = 0.0
        st.session_state.confianza_num = 0.0
        if "grafico_seleccionado_id" in st.session_state:
            del st.session_state.grafico_seleccionado_id
        st.rerun()