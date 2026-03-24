import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# 1. Configuración de Pantalla (Optimizado para TV de 55" y S25 Ultra)
st.set_page_config(
    page_title="PFA - Causa 4879/2024",
    page_icon="🚔",
    layout="wide"
)

# 2. Estética Táctica (Dark Mode Oficial PFA)
st.markdown("""
    <style>
    .stApp { background-color: #0d1b2a; color: #e0e0e0; }
    .company-header {
        background: linear-gradient(90deg, #1a3a5a 0%, #0d1b2a 100%);
        color: #3498db;
        padding: 15px;
        border-radius: 8px 8px 0 0;
        font-weight: bold;
        font-size: 1.2rem;
        border-bottom: 2px solid #3498db;
        margin-top: 25px;
    }
    .card-body {
        background-color: #162636;
        padding: 20px;
        border-radius: 0 0 8px 8px;
        border: 1px solid #1a3a5a;
        margin-bottom: 10px;
    }
    .res-policial {
        background-color: rgba(52, 152, 219, 0.05);
        border-left: 4px solid #3498db;
        padding: 12px;
        font-style: italic;
        border-radius: 4px;
        margin-top: 10px;
    }
    .status-verde { color: #2ecc71; font-weight: bold; }
    .status-amarillo { color: #f1c40f; font-weight: bold; }
    .status-rojo { color: #e74c3c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. Carga de Datos (Con auto-detección de formato)
@st.cache_data
def load_data():
    # El motor 'python' y sep=None detectan si usaste coma o punto y coma
    df = pd.read_csv('data.csv', sep=None, engine='python', encoding='utf-8')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    return df

try:
    df = load_data()
    
    if df.empty:
        st.error("🚨 El archivo 'data.csv' está vacío. Cargá los datos en GitHub.")
        st.stop()

    # --- ENCABEZADO ---
    st.markdown("<h1 style='text-align: center;'>🚨 Inteligencia PFA - Monitor Táctico</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #3498db;'>Causa 4879/2024 - Relevamiento de Campo</h3>", unsafe_allow_html=True)

    # --- RESUMEN DE CANTIDADES ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Empresas Investigadas", len(df['empresa'].unique()))
    with col2:
        st.metric("Objetivos Totales", len(df))
    with col3:
        st.metric("Resultados Positivos (Verde)", len(df[df['status'] == 'Verde']))

    # --- MAPA INTERACTIVO ---
    st.markdown("---")
    st.subheader("📍 Despliegue Geográfico de Objetivos")
    df_map = df.dropna(subset=['latitude', 'longitude'])
    
    if not df_map.empty:
        m = folium.Map(location=[df_map['latitude'].mean(), df_map['longitude'].mean()], zoom_start=11, tiles="CartoDB dark_matter")
        for _, row in df_map.iterrows():
            color = {"Verde": "green", "Amarillo": "orange", "Rojo": "red"}.get(row['status'], "gray")
            folium.Marker(
                [row['latitude'], row['longitude']], 
                popup=f"<b>{row['empresa']}</b><br>{row['sujeto']}", 
                icon=folium.Icon(color=color, icon="info-sign")
            ).add_to(m)
        folium_static(m, width=1100)
    else:
        st.warning("No se detectaron coordenadas válidas para mostrar el mapa.")

    # --- SIDEBAR (Filtros) ---
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/2/2c/Logo_de_la_Polic%C3%ADa_Federal_Argentina.png", width=120)
        st.header("Filtros")
        status_filtro = st.multiselect("Ver por estado:", ["Verde", "Amarillo", "Rojo"], default=["Verde", "Amarillo", "Rojo"])

    # --- TARJETAS DETALLADAS ---
    st.markdown("---")
    st.subheader("🏢 Detalle por Empresa e Investigados")
    
    for emp in df['empresa'].unique():
        sub_df = df[(df['empresa'] == emp) & (df['status'].isin(status_filtro))]
        
        if not sub_df.empty:
            st.markdown(f'<div class="company-header">🏢 {emp} | CUIT: {sub_df["cuit"].iloc[0]}</div>', unsafe_allow_html=True)
            for _, row in sub_df.iterrows():
                status_color = {"Verde": "status-verde", "Amarillo": "status-amarillo", "Rojo": "status-rojo"}.get(row['status'], "")
                with st.container():
                    st.markdown(f"""
                    <div class="card-body">
                        <div style="display: flex; justify-content: space-between;">
                            <b>👤 {row['sujeto']}</b>
                            <span class="{status_color}">{row['status'].upper()}</span>
                        </div>
                        <div style="margin-top:10px; font-size: 0.9rem;">
                            📍 <b>Domicilio:</b> {row['domicilio']}<br>
                            📞 <b>Teléfonos:</b> {row['telefonos']} | 🌐 <b>Redes:</b> {row['redes_sociales']}
                        </div>
                        <div class="res-policial">
                            <b>Informe Policial:</b> {row['resultado']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error técnico al procesar el dashboard: {e}")
