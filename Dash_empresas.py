import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# 1. LOGIN DE ACCESO
def login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False
    if not st.session_state["autenticado"]:
        st.markdown("<h2 style='text-align: center; color: white;'>🚔 Sistema de Inteligencia PFA</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            clave = st.text_input("Clave de la Causa 4879:", type="password")
            if st.button("Acceder"):
                if clave == "Dicco1272":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("⚠️ Clave incorrecta")
        return False
    return True

if login():
    st.set_page_config(page_title="PFA - Causa 4879", layout="wide")

    # 2. ESTÉTICA TÁCTICA PARA 55"
    st.markdown("""
        <style>
        .stApp { background-color: #0b131e; color: #e0e0e0; }
        .company-card {
            background-color: #162636; border-radius: 12px; padding: 18px;
            margin-bottom: 25px; border: 1px solid #1a3a5a;
            box-shadow: 0 8px 16px rgba(0,0,0,0.6);
        }
        .company-header-box { border-bottom: 2px solid #3498db; margin-bottom: 15px; padding-bottom: 8px; }
        .company-title { color: #3498db; font-size: 1.2rem; font-weight: bold; text-transform: uppercase; }
        .subject-block {
            background: rgba(0,0,0,0.25); border-radius: 8px; padding: 12px;
            margin-bottom: 12px; border-left: 5px solid #7f8c8d;
        }
        .border-verde { border-left-color: #2ecc71 !important; }
        .border-amarillo { border-left-color: #f1c40f !important; }
        .border-rojo { border-left-color: #e74c3c !important; }
        .subject-name { font-size: 0.95rem; font-weight: bold; color: #ffffff; }
        .subject-data { font-size: 0.8rem; line-height: 1.4; color: #adb5bd; margin-top: 5px; }
        .subject-report { 
            font-size: 0.78rem; font-style: italic; color: #3498db; 
            margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1);
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
        st.markdown("<h1 style='text-align: center;'>🚨 Monitoreo de Redes Societarias - Causa 4879</h1>", unsafe_allow_html=True)

        # 3. FILTROS Y BÚSQUEDA
        col_search, col_status = st.columns([2, 1])
        with col_search:
            query = st.text_input("🔍 Buscar por Empresa, Nombre o CUIT:", "").lower()
        with col_status:
            status_filtro = st.multiselect("Filtrar estados:", ["Verde", "Amarillo", "Rojo"], default=["Verde", "Amarillo", "Rojo"])

        df_base = df[df['status'].isin(status_filtro)]
        if query:
            match_empresas = df_base[
                df_base['empresa'].str.contains(query, case=False, na=False) | 
                df_base['sujeto'].str.contains(query, case=False, na=False) |
                df_base['cuit'].astype(str).str.contains(query, na=False)
            ]['empresa'].unique()
            df_final = df_base[df_base['empresa'].isin(match_empresas)]
        else:
            df_final = df_base

        tab1, tab2 = st.tabs(["📍 MAPA OPERATIVO", "🏢 ÍNDICE DE EMPRESAS (22)"])

        with tab1:
            df_map = df_final.dropna(subset=['latitude', 'longitude'])
            if not df_map.empty:
                m = folium.Map(location=[df_map['latitude'].mean(), df_map['longitude'].mean()], zoom_start=11, tiles="CartoDB dark_matter")
                for _, row in df_map.iterrows():
                    color = {"Verde": "green", "Amarillo": "orange", "Rojo": "red"}.get(row['status'], "gray")
                    folium.Marker([row['latitude'], row['longitude']], 
                                  popup=f"<b>{row['empresa']}</b><br>{row['sujeto']}", 
                                  icon=folium.Icon(color=color)).add_to(m)
                folium_static(m, width=1300)

        with tab2:
            empresas_unicas = df_final['empresa'].unique()
            n_cols = 3 
            cols = st.columns(n_cols)
            
            for i, emp in enumerate(empresas_unicas):
                with cols[i % n_cols]:
                    data_emp = df_final[df_final['empresa'] == emp]
                    cuit_val = data_emp['cuit'].iloc[0]
                    
                    # CONSTRUCCIÓN DEL CUADRO DE EMPRESA
                    html_card = f'<div class="company-card">'
                    html_card += f'<div class="company-header-box"><div class="company-title">{emp}</div>'
                    html_card += f'<div style="color:#7f8c8d; font-size:0.8rem;">CUIT: {cuit_val}</div></div>'
                    
                    for _, row in data_emp.iterrows():
                        c_border = f"border-{row['status'].lower()}"
                        html_card += f"""
                        <div class="subject-block {c_border}">
                            <div class="subject-name">👤 {row['sujeto']}</div>
                            <div class="subject-data">
                                📍 {row['domicilio']}<br>
                                📞 {row['telefonos']} | 🌐 {row['redes_sociales']}
                            </div>
                            <div class="subject-report">{row['resultado']}</div>
                        </div>
                        """
                    html_card += "</div>"
                    st.markdown(html_card, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Falla crítica: {e}")
