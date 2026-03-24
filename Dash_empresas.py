import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import json

# 1. CONFIGURACIÓN DE PANTALLA (Para TV y S25 Ultra)
st.set_page_config(
    page_title="PFA - Causa 4879/2024",
    page_icon="🚔",
    layout="wide"
)

# 2. CARGA DE DATOS (Fase 2)
# Esta función lee el archivo CSV. Si no existe, muestra un mensaje.
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data.csv')
        # Limpieza básica para asegurar que lat/lon sean números
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        return df
    except FileNotFoundError:
        return pd.DataFrame() # Devuelve DF vacío si no encuentra el archivo

df = load_data()

# --- ESTÉTICA TÁCTICA (Dark Mode) ---
st.markdown("""
    <style>
    .main { background-color: #0d1b2a; color: #e0e0e0; }
    .stApp { background-color: #0d1b2a; }
    .company-header {
        background: linear-gradient(90deg, #1a3a5a 0%, #0d1b2a 100%);
        color: #3498db;
        padding: 15px;
        border-radius: 8px 8px 0 0;
        font-weight: bold;
        font-size: 1.2rem;
        border-bottom: 2px solid #3498db;
        margin-top: 30px;
    }
    .card-body {
        background-color: #162636;
        padding: 20px;
        border-radius: 0 0 8px 8px;
        border: 1px solid #1a3a5a;
        margin-bottom: 15px;
    }
    .res-policial {
        background-color: rgba(52, 152, 219, 0.05);
        border-left: 4px solid #3498db;
        padding: 12px;
        font-style: italic;
        border-radius: 4px;
        margin-top: 10px;
    }
    .data-label { color: #adb5bd; font-size: 0.85rem; text-transform: uppercase; font-weight: bold; margin-top: 10px;}
    .data-value { font-weight: 500; margin-bottom: 5px; color: #ffffff;}
    .status-verde { color: #2ecc71; font-weight: bold; }
    .status-amarillo { color: #f1c40f; font-weight: bold; }
    .status-rojo { color: #e74c3c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. CABECERA INSTITUCIONAL
st.markdown("<h1 style='text-align: center; color: white;'>🚨 Inteligencia PFA - Sala de Situación</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #3498db; margin-bottom: 30px;'>Causa 4879/2024 - Relevamiento Integral</h3>", unsafe_allow_html=True)

if df.empty:
    st.warning("⚠️ El archivo 'data.csv' no fue encontrado o está vacío. Por favor, complete la Fase 2 (Crear data.csv) para visualizar los datos.")
    st.stop()

# --- FASE 1: MAPA INTERACTIVO DE PINPOINTS ---
st.markdown("---")
st.header("📍 Geocalización de Objetivos")

# Filtrar solo los datos con coordenadas válidas para el mapa
df_map = df.dropna(subset=['latitude', 'longitude'])

if not df_map.empty:
    # Crear Mapa base centrado en CABA/GBA
    m = folium.Map(location=[-34.6037, -58.3816], zoom_start=11, tiles="CartoDB dark_matter")

    # Agregar Marcadores
    for _, row in df_map.iterrows():
        # Color del Pin según Semáforo
        color = {"Verde": "green", "Amarillo": "orange", "Rojo": "red"}.get(row['status'], "gray")
        icon_type = {"Verde": "ok-sign", "Amarillo": "warning-sign", "Rojo": "remove-sign"}.get(row['status'], "info-sign")

        popup_text = f"""
        <b>Empresa:</b> {row['empresa']}<br>
        <b>Objetivo:</b> {row['sujeto']}<br>
        <b>Domicilio:</b> {row['domicilio']}<br>
        <b>Teléfono:</b> {row['telefonos']}<br>
        <b>Redes:</b> {row['redes_sociales']}<br>
        <b>Estado:</b> {row['status']}
        """

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_text, max_width=300),
            tooltip=f"{row['empresa']} - {row['sujeto']}",
            icon=folium.Icon(color=color, icon=icon_type)
        ).add_to(m)

    # Mostrar Mapa en Streamlit
    folium_static(m, width=1200, height=600)
else:
    st.info("No hay datos geolocalizados disponibles para mostrar en el mapa (faltan Latitud/Longitud en el CSV).")

# --- RESUMEN DE LA CAUSA (CANTIDADES) ---
st.markdown("---")
st.header("📊 Resumen Numérico de la Causa")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Empresas Investigadas", len(df['empresa'].unique()))
with col2:
    st.metric("Total Objetivos (Gente/Sedes)", len(df))
with col3:
    # Este campo 'novedades' debe estar en el CSV para mostrar algo
    try:
        st.metric("Novedades de Campo Registradas", len(df[df['resultado'].notna()]))
    except:
        st.metric("Novedades de Campo Registradas", "Pendiente CSV")

st.markdown("---")

# 7. SIDEBAR (Filtros Tácticos)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/2c/Logo_de_la_Polic%C3%ADa_Federal_Argentina.png", width=120)
    st.header("Panel de Control")
    st.write("Seleccione el estado de los objetivos para filtrar la vista:")
    status_filtro = st.multiselect(
        "Filtro de Semáforo:",
        ["Verde", "Amarillo", "Rojo"],
        default=["Verde", "Amarillo", "Rojo"]
    )
    st.info(f"Mostrando {len(df[df['status'].isin(status_filtro)])} de {len(df)} objetivos totales.")

# --- FASE 2: CARTAS DE EMPRESAS Y GENTE ---
st.header("🏢 Detalle por Empresa y Objetivos")

empresas = df['empresa'].unique()

for emp in empresas:
    sub_df = df[(df['empresa'] == emp) & (df['status'].isin(status_filtro))]

    if not sub_df.empty:
        cuit = sub_df['cuit'].iloc[0]
        # Título de la Empresa (Header)
        st.markdown(f"""
        <div class="company-header">
            🏢 {emp} <span style="float:right; font-size:1rem; color:#adb5bd;">CUIT: {cuit}</span>
        </div>
        """, unsafe_allow_html=True)

        # Tarjetas de Objetivos
        for _, row in sub_df.iterrows():
            with st.container():
                # Color del semáforo en texto
                status_class = {"Verde": "status-verde", "Amarillo": "status-amarillo", "Rojo": "status-rojo"}.get(row['status'], "")
                
                st.markdown(f"""
                <div class="card-body">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <span style="font-size: 1.1rem; font-weight: bold;">👤 {row['sujeto']}</span>
                        <span class="{status_class}">{row['status'].upper()}</span>
                    </div>
                    
                    <div class="row" style="display: flex; flex-wrap: wrap;">
                        <div class="col" style="flex: 1; min-width: 250px; margin-right: 20px;">
                            <div class="data-label">📍 Domicilio Relevado</div>
                            <div class="data-value">{row['domicilio']}</div>
                            <div class="data-label">📞 Teléfonos Detectados</div>
                            <div class="data-value">{row['telefonos']}</div>
                        </div>
                        <div class="col" style="flex: 1; min-width: 250px;">
                            <div class="data-label">🌐 Redes Sociales Completas</div>
                            <div class="data-value">{row['redes_sociales']}</div>
                        </div>
                    </div>

                    <div class="data-label">📝 Columna de Resultados Policiales</div>
                    <div class="res-policial">{row['resultado']}</div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<br><hr><p style='text-align: center; color: #adb5bd; font-size: 0.8rem;'>Generado para Briefing de Comando - PFA Inteligencia</p>", unsafe_allow_html=True)
