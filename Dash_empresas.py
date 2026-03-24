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
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            clave = st.text_input("Clive de la Causa 4879:", type="password")
            if st.button("Acceder"):
                if clave == "Dicco1272": # CLAVE ACTUALIZADA
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("⚠️ Clave incorrecta")
        return False
    return True

if login():
    st.set_page_config(page_title="PFA - Causa 4879", layout="wide")

    # 2. ESTÉTICA TÁCTICA (CSS)
    st.markdown("""
        <style>
        .stApp { background-color: #0b131e; color: #e0e0e0; }
        .company-card {
            background-color: #162636; border-radius: 12px; padding: 18px;
            margin-bottom: 25px; border: 1px solid #1a3a5a;
            box-shadow: 0 8px 16px rgba(0,0,0,0.6);
        }
        .header-box { border-bottom: 2px solid #3498db; margin-bottom: 15px; padding-bottom: 8px; }
        .company-title { color: #3498db; font-size: 1.1rem; font-weight: bold; text-transform: uppercase; }
        .subject-block {
            background: rgba(0,0,0,0.3); border-radius: 8px; padding: 10px;
            margin-bottom: 10px; border-left: 5px solid #7f8c8d;
        }
        .border-verde { border-left-color: #2ecc71 !important; }
        .border-amarillo { border-left-color: #f1c40f !important; }
        .border-rojo { border-left-color: #e74c3c !important; }
        .subject-name { font-size: 0.9rem; font-weight: bold; color: #ffffff; }
        .subject-data { font-size: 0.75rem; line-height: 1.3; color: #adb5bd; margin-top: 5px; }
        .subject-report { 
            font-size: 0.72rem; font-style: italic; color: #3498db; 
            margin-top: 8px; padding-top: 6px; border-top: 1px solid rgba(255,255,255,0.1);
        }
        </style>
        """, unsafe_allow_html=True)

    @st.cache_data
    def load_data():
        # Carga el CSV que ya tenés completo en GitHub
        df = pd.read_csv('data.csv', sep=None, engine='python', encoding='utf-8')
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        return df

    try:
        df = load_data()
        st.markdown("<h1 style='text-align: center;'>🚨 Monitoreo de Redes Societarias - Causa 4879</h1>", unsafe_allow_html=True)

        # 3. BUSCADOR Y FILTROS
        col_s, col_f = st.columns([3, 1])
        with col_s:
            query = st.text_input("🔍 Buscador de Empresa, Sujeto, CUIT o DNI:", "").lower()
        with col_f:
            status_f = st.multiselect("Semáforo:", ["Verde", "Amarillo", "Rojo"], default=["Verde", "Amarillo", "Rojo"])

        # Lógica de filtrado
        df_base = df[df['status'].isin(status_f)]
        if query:
            match_emp = df_base[
                df_base['empresa'].str.contains(query, case=False, na=False) | 
                df_base['sujeto'].str.contains(query, case=False, na=False) |
                df_base['cuit'].astype(str).str.contains(query, na=False)
            ]['empresa'].unique()
            df_final = df_base[df_base['empresa'].isin(match_emp)]
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
                folium_static(m, width=1200)

        with tab2:
            empresas = df_final['empresa'].unique()
            cols = st.columns(3) # 3 Columnas para la TV de 55"
            
            for i, emp in enumerate(empresas):
                with cols[i % 3]:
                    data_emp = df_final[df_final['empresa'] == emp]
                    cuit_label = data_emp['cuit'].iloc[0]
                    
                    # ARMAMOS TODO EL HTML EN UNA SOLA VARIABLE PARA QUE NO DE ERROR
                    html_card = f"""
                    <div class="company-card">
                        <div class="header-box">
                            <div class="company-title">{emp}</div>
                            <div style="color:#7f8c8d; font-size:0.8rem;">CUIT: {cuit_label}</div>
                        </div>
                    """
                    
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
                    
                    html_card += "</div>" # Cerramos el cuadro de la empresa
                    
                    # MANDAMOS EL BLOQUE COMPLETO A LA PANTALLA
                    st.markdown(html_card, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Falla crítica: {e}")
