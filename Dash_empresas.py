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
            clave = st.text_input("Ingrese Clave Operativa:", type="password")
            if st.button("Acceder"):
                if clave == "Dicco1272": # CLAVE FIJADA
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("⚠️ Acceso Denegado")
        return False
    return True

if login():
    st.set_page_config(page_title="PFA - Causa 4879", layout="wide")

    # 2. CSS - ESTÉTICA DE TARJETAS EMPRESARIALES (Sin espacios que rompan markdown)
    st.markdown("""
<style>
.stApp { background-color: #0b131e; color: #e0e0e0; }
.company-card { background-color: #162636; border-radius: 12px; padding: 20px; margin-bottom: 25px; border: 1px solid #1a3a5a; box-shadow: 0 8px 16px rgba(0,0,0,0.6); min-height: 480px; }
.header-box { border-bottom: 2px solid #3498db; margin-bottom: 15px; padding-bottom: 10px; }
.company-title { color: #3498db; font-size: 1.1rem; font-weight: bold; text-transform: uppercase; }
.subject-block { background: rgba(0,0,0,0.3); border-radius: 8px; padding: 12px; margin-bottom: 12px; border-left: 5px solid #7f8c8d; }
.border-verde { border-left-color: #2ecc71 !important; }
.border-amarillo { border-left-color: #f1c40f !important; }
.border-rojo { border-left-color: #e74c3c !important; }
.subject-name { font-size: 0.95rem; font-weight: bold; color: #ffffff; }
.subject-data { font-size: 0.8rem; line-height: 1.4; color: #adb5bd; margin-top: 5px; }
.subject-report { font-size: 0.75rem; font-style: italic; color: #3498db; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1); }
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

        # 3. FILTROS
        q_col, s_col = st.columns([3, 1])
        with q_col:
            query = st.text_input("🔍 Buscador de Empresa, Sujeto o CUIT:", "").lower()
        with s_col:
            status_f = st.multiselect("Semáforo:", ["Verde", "Amarillo", "Rojo"], default=["Verde", "Amarillo", "Rojo"])

        df_base = df[df['status'].isin(status_f)]
        if query:
            match_list = df_base[
                df_base['empresa'].str.contains(query, case=False, na=False) | 
                df_base['sujeto'].str.contains(query, case=False, na=False) |
                df_base['cuit'].astype(str).str.contains(query, na=False)
            ]['empresa'].unique()
            df_final = df_base[df_base['empresa'].isin(match_list)]
        else:
            df_final = df_base

        tab_m, tab_g = st.tabs(["📍 MAPA OPERATIVO", "🏢 ÍNDICE DE EMPRESAS (22)"])

        with tab_m:
            df_map = df_final.dropna(subset=['latitude', 'longitude'])
            if not df_map.empty:
                m = folium.Map(location=[df_map['latitude'].mean(), df_map['longitude'].mean()], zoom_start=11, tiles="CartoDB dark_matter")
                for _, row in df_map.iterrows():
                    color = {"Verde": "green", "Amarillo": "orange", "Rojo": "red"}.get(row['status'], "gray")
                    folium.Marker([row['latitude'], row['longitude']], popup=f"<b>{row['empresa']}</b><br>{row['sujeto']}", icon=folium.Icon(color=color)).add_to(m)
                folium_static(m, width=1300)

        with tab_g:
            empresas = df_final['empresa'].unique()
            cols = st.columns(3) 
            
            for i, emp in enumerate(empresas):
                with cols[i % 3]:
                    data_emp = df_final[df_final['empresa'] == emp]
                    cuit_label = data_emp['cuit'].iloc[0]
                    
                    # CONSTRUCCIÓN LINEAL DEL HTML (Sin espacios en blanco para evitar errores)
                    html_content = f"<div class='company-card'>"
                    html_content += f"<div class='header-box'>"
                    html_content += f"<div class='company-title'>{emp}</div>"
                    html_content += f"<div style='color:#7f8c8d; font-size:0.85rem;'>CUIT: {cuit_label}</div>"
                    html_content += f"</div>"
                    
                    for _, row in data_emp.iterrows():
                        border = f"border-{row['status'].lower()}"
                        html_content += f"<div class='subject-block {border}'>"
                        html_content += f"<div class='subject-name'>👤 {row['sujeto']}</div>"
                        html_content += f"<div class='subject-data'>📍 {row['domicilio']}<br>📞 {row['telefonos']} | 🌐 {row['redes_sociales']}</div>"
                        html_content += f"<div class='subject-report'>{row['resultado']}</div>"
                        html_content += f"</div>"
                        
                    html_content += "</div>"
                    
                    st.markdown(html_content, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Falla crítica: {e}")
