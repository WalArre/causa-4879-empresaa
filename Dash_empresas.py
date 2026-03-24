import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# 1. SEGURIDAD DE ACCESO
def login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False
    if not st.session_state["autenticado"]:
        st.markdown("<h2 style='text-align: center; color: white;'>🚔 Sistema de Inteligencia PFA</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            clave = st.text_input("Clave de la Causa 4879:", type="password")
            if st.button("Acceder"):
                if clave == "Dicco1272": # CLAVE MANUAL
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("⚠️ Clave incorrecta")
        return False
    return True

if login():
    st.set_page_config(page_title="PFA - Causa 4879", layout="wide")

    # 2. CSS PARA CUADROS POR EMPRESA (Contenedores)
    st.markdown("""
        <style>
        .stApp { background-color: #0b131e; color: #e0e0e0; }
        
        /* Contenedor Principal de la Empresa */
        .company-card {
            background-color: #162636;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid #1a3a5a;
            box-shadow: 0 6px 12px rgba(0,0,0,0.5);
            min-height: 400px;
        }
        .company-title { 
            color: #3498db; 
            font-size: 1.1rem; 
            font-weight: bold; 
            border-bottom: 2px solid #3498db;
            margin-bottom: 12px;
            padding-bottom: 5px;
            text-transform: uppercase;
        }
        
        /* Bloque de Persona/Sujeto dentro de la empresa */
        .subject-block {
            background: rgba(0,0,0,0.2);
            border-radius: 6px;
            padding: 10px;
            margin-bottom: 10px;
            border-left: 4px solid #7f8c8d;
        }
        .border-verde { border-left-color: #2ecc71 !important; }
        .border-amarillo { border-left-color: #f1c40f !important; }
        .border-rojo { border-left-color: #e74c3c !important; }
        
        .subject-name { font-size: 0.9rem; font-weight: bold; color: #ffffff; }
        .subject-data { font-size: 0.8rem; line-height: 1.2; color: #adb5bd; margin-top: 4px; }
        .subject-report { 
            font-size: 0.75rem; 
            font-style: italic; 
            color: #3498db; 
            margin-top: 6px; 
            border-top: 1px solid #2c3e50;
            padding-top: 4px;
        }
        </style>
        """, unsafe_allow_html=True)

    @st.cache_data
    def load_data():
        df = pd.read_csv('data.csv', sep=None, engine='python', encoding='utf-8')
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        return df

    try:
        df = load_data()
        st.markdown("<h1 style='text-align: center;'>🚨 Monitor de Empresas - Causa 4879</h1>", unsafe_allow_html=True)

        # 3. FILTROS
        col_a, col_b = st.columns([3, 1])
        with col_a:
            query = st.text_input("🔍 Buscar por Empresa o Nombre de Investigado:", "").lower()
        with col_b:
            status_filtro = st.multiselect("Filtrar por Estado:", ["Verde", "Amarillo", "Rojo"], default=["Verde", "Amarillo", "Rojo"])

        # Lógica de búsqueda: Si el nombre de la empresa O alguno de sus integrantes coincide
        df_filtrado = df[df['status'].isin(status_filtro)]
        if query:
            # Encontramos todas las empresas que tienen al menos un match
            empresas_con_match = df_filtrado[
                df_filtrado['empresa'].str.contains(query, case=False, na=False) | 
                df_filtrado['sujeto'].str.contains(query, case=False, na=False)
            ]['empresa'].unique()
            df_display = df_filtrado[df_filtrado['empresa'].isin(empresas_con_match)]
        else:
            df_display = df_filtrado

        tab_map, tab_grid = st.tabs(["📍 MAPA DE OBJETIVOS", "🏢 ESTRUCTURA POR EMPRESA"])

        with tab_map:
            df_map = df_display.dropna(subset=['latitude', 'longitude'])
            if not df_map.empty:
                m = folium.Map(location=[df_map['latitude'].mean(), df_map['longitude'].mean()], zoom_start=11, tiles="CartoDB dark_matter")
                for _, row in df_map.iterrows():
                    color = {"Verde": "green", "Amarillo": "orange", "Rojo": "red"}.get(row['status'], "gray")
                    folium.Marker([row['latitude'], row['longitude']], popup=f"{row['empresa']}: {row['sujeto']}", icon=folium.Icon(color=color)).add_to(m)
                folium_static(m, width=1200)

        with tab_grid:
            # Agrupamos por Empresa para generar un recuadro por cada una
            lista_empresas = df_display['empresa'].unique()
            
            # Grilla de 3 columnas (mejor para ver contenido interno de cada cuadro)
            n_cols = 3
            cols = st.columns(n_cols)
            
            for i, nombre_empresa in enumerate(lista_empresas):
                with cols[i % n_cols]:
                    # Datos de la empresa actual
                    emp_data = df_display[df_display['empresa'] == nombre_empresa]
                    cuit_emp = emp_data['cuit'].iloc[0]
                    
                    # Iniciamos el cuadro de empresa
                    card_html = f"""
                    <div class="company-card">
                        <div class="company-title">{nombre_empresa}</div>
                        <div style="font-size:0.8rem; color:#7f8c8d; margin-top:-10px; margin-bottom:15px;">CUIT: {cuit_emp}</div>
                    """
                    
                    # Agregamos a cada persona dentro de esta empresa
                    for _, row in emp_data.iterrows():
                        color_class = f"border-{row['status'].lower()}"
                        card_html += f"""
                        <div class="subject-block {color_class}">
                            <div class="subject-name">👤 {row['sujeto']}</div>
                            <div class="subject-data">
                                📍 {row['domicilio']}<br>
                                📞 {row['telefonos']} | 🌐 {row['redes_sociales']}
                            </div>
                            <div class="subject-report">
                                {row['resultado']}
                            </div>
                        </div>
                        """
                    
                    card_html += "</div>"
                    st.markdown(card_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error en carga de datos: {e}")
