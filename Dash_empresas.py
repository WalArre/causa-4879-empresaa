import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# 1. CONFIGURACIÓN E INSTITUCIONAL
st.set_page_config(page_title="PFA - Monitoreo Causa 4879", layout="wide")

# 2. CSS PARA CUADRADOS (GRID) Y BUSCADOR
st.markdown("""
    <style>
    .stApp { background-color: #0b131e; color: #e0e0e0; }
    /* Estilo de la tarjeta (cuadrado) */
    .investigado-card {
        background-color: #162636;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        height: 320px;
        border-top: 5px solid #3498db;
        box-shadow: 0 4px 8px rgba(0,0,0,0.5);
    }
    .card-verde { border-top: 5px solid #2ecc71; }
    .card-amarillo { border-top: 5px solid #f1c40f; }
    .card-rojo { border-top: 5px solid #e74c3c; }
    
    .card-title { font-size: 1.1rem; font-weight: bold; color: #ffffff; margin-bottom: 5px; }
    .card-sub { font-size: 0.85rem; color: #3498db; margin-bottom: 10px; font-weight: bold; }
    .card-info { font-size: 0.85rem; line-height: 1.3; margin-bottom: 8px; }
    .card-res { 
        background: rgba(0,0,0,0.2); 
        padding: 8px; 
        border-radius: 5px; 
        font-size: 0.8rem; 
        font-style: italic; 
        border-left: 2px solid #3498db;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CARGA DE DATOS
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv', sep=None, engine='python', encoding='utf-8')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    return df

try:
    df = load_data()
    
    # --- BUSCADOR Y FILTROS SUPERIORES ---
    st.markdown("<h1 style='text-align: center; color: white;'>🚔 Sala de Situación - Causa 4879</h1>", unsafe_allow_html=True)
    
    col_search, col_status = st.columns([2, 1])
    with col_search:
        query = st.text_input("🔍 Buscador de Objetivos (Nombre, CUIT, Empresa o DNI):", "").lower()
    with col_status:
        status_filtro = st.multiselect("Filtrar Semáforo:", ["Verde", "Amarillo", "Rojo"], default=["Verde", "Amarillo", "Rojo"])

    # Aplicar filtros
    mask = (
        (df['empresa'].str.lower().contains(query) | 
         df['sujeto'].str.lower().contains(query) | 
         df['cuit'].astype(str).str.contains(query)) &
        (df['status'].isin(status_filtro))
    )
    df_filtrado = df[mask]

    # --- MÉTRICAS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Objetivos en Vista", len(df_filtrado))
    m2.metric("Positivos", len(df_filtrado[df_filtrado['status'] == 'Verde']))
    m3.metric("Pendientes", len(df_filtrado[df_filtrado['status'] == 'Amarillo']))
    m4.metric("Sin Datos/Neg", len(df_filtrado[df_filtrado['status'] == 'Rojo']))

    # --- PESTAÑAS (TABS) ---
    tab_mapa, tab_cuadrados = st.tabs(["📍 MAPA OPERATIVO", "📇 ÍNDICE DE OBJETIVOS"])

    with tab_mapa:
        df_map = df_filtrado.dropna(subset=['latitude', 'longitude'])
        if not df_map.empty:
            m = folium.Map(location=[df_map['latitude'].mean(), df_map['longitude'].mean()], zoom_start=11, tiles="CartoDB dark_matter")
            for _, row in df_map.iterrows():
                color = {"Verde": "green", "Amarillo": "orange", "Rojo": "red"}.get(row['status'], "gray")
                folium.Marker([row['latitude'], row['longitude']], popup=row['sujeto'], icon=folium.Icon(color=color)).add_to(m)
            folium_static(m, width=1300, height=500)
        else:
            st.warning("No hay coordenadas para los filtros seleccionados.")

    with tab_cuadrados:
        # Generar Grilla de Cuadrados (Cards)
        columnas_grilla = st.columns(3) # 3 columnas para la TV de 55"
        
        for i, (idx, row) in enumerate(df_filtrado.iterrows()):
            with columnas_grilla[i % 3]:
                card_class = f"card-{row['status'].lower()}"
                st.markdown(f"""
                <div class="investigado-card {card_class}">
                    <div class="card-title">{row['sujeto'][:40]}</div>
                    <div class="card-sub">{row['empresa']}</div>
                    <div class="card-info">
                        <b>📍 Dom:</b> {row['domicilio'][:60]}...<br>
                        <b>📞 Tel:</b> {row['telefonos']}<br>
                        <b>🌐 Redes:</b> {row['redes_sociales']}
                    </div>
                    <div class="card-res">
                        <b>Informe:</b> {row['resultado'][:120]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error en la carga: {e}")
