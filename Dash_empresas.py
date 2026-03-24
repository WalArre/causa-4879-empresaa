import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# 1. CONFIGURACIÓN DE SEGURIDAD (Clave manual)
def check_password():
    """Devuelve True si el usuario ingresó la clave correcta."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        # Pantalla de Login
        st.markdown("<h2 style='text-align: center; color: white;'>🚔 Sistema de Inteligencia PFA</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Ingrese la clave de acceso de la Causa 4879</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            password = st.text_input("Contraseña:", type="password")
            if st.button("Acceder"):
                # DEFINÍ TU CLAVE ACÁ (Cambiá 'brigada4879' por lo que quieras)
                if password == "Dicco1272": 
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("⚠️ Clave incorrecta. Acceso denegado.")
        return False
    return True

# Solo si la clave es correcta, se ejecuta el resto
if check_password():
    
    # 2. CONFIGURACIÓN E INSTITUCIONAL
    st.set_page_config(page_title="PFA - Monitoreo Causa 4879", layout="wide")

    # 3. CSS PARA CUADRADOS Y ESTÉTICA
    st.markdown("""
        <style>
        .stApp { background-color: #0b131e; color: #e0e0e0; }
        .investigado-card {
            background-color: #162636;
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 15px;
            height: 300px;
            border-top: 5px solid #3498db;
            box-shadow: 0 4px 8px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .card-verde { border-top: 5px solid #2ecc71; }
        .card-amarillo { border-top: 5px solid #f1c40f; }
        .card-rojo { border-top: 5px solid #e74c3c; }
        .card-title { font-size: 1rem; font-weight: bold; color: #ffffff; }
        .card-sub { font-size: 0.8rem; color: #3498db; font-weight: bold; text-transform: uppercase; }
        .card-info { font-size: 0.8rem; line-height: 1.2; margin-top: 5px; }
        .card-res { 
            background: rgba(0,0,0,0.3); 
            padding: 8px; border-radius: 5px; font-size: 0.75rem; 
            font-style: italic; border-left: 2px solid #3498db;
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
        
        # --- BUSCADOR Y FILTROS ---
        st.markdown("<h1 style='text-align: center;'>🚨 Monitor Táctico - Causa 4879</h1>", unsafe_allow_html=True)
        
        query = st.text_input("🔍 Buscador (Nombre, CUIT, Empresa o DNI):", "").lower()
        status_filtro = st.multiselect("Filtrar Semáforo:", ["Verde", "Amarillo", "Rojo"], default=["Verde", "Amarillo", "Rojo"])

        mask = (
            (df['empresa'].str.contains(query, case=False, na=False) | 
             df['sujeto'].str.contains(query, case=False, na=False) | 
             df['cuit'].astype(str).str.contains(query, na=False)) &
            (df['status'].isin(status_filtro))
        )
        df_filtrado = df[mask]

        # --- PESTAÑAS ---
        tab_mapa, tab_cuadrados = st.tabs(["📍 MAPA OPERATIVO", "📇 ÍNDICE EN CUADRADOS"])

        with tab_mapa:
            df_map = df_filtrado.dropna(subset=['latitude', 'longitude'])
            if not df_map.empty:
                m = folium.Map(location=[df_map['latitude'].mean(), df_map['longitude'].mean()], zoom_start=11, tiles="CartoDB dark_matter")
                for _, row in df_map.iterrows():
                    color = {"Verde": "green", "Amarillo": "orange", "Rojo": "red"}.get(row['status'], "gray")
                    folium.Marker([row['latitude'], row['longitude']], popup=row['sujeto'], icon=folium.Icon(color=color)).add_to(m)
                folium_static(m, width=1200, height=500)

        with tab_cuadrados:
            n_cols = 4
            columnas_grilla = st.columns(n_cols)
            for i, (idx, row) in enumerate(df_filtrado.iterrows()):
                with columnas_grilla[i % n_cols]:
                    card_class = f"card-{row['status'].lower()}"
                    st.markdown(f"""
                    <div class="investigado-card {card_class}">
                        <div>
                            <div class="card-title">{row['sujeto'][:45]}</div>
                            <div class="card-sub">{row['empresa'][:30]}</div>
                            <div class="card-info">
                                <b>📍 Dom:</b> {row['domicilio'][:50]}...<br>
                                <b>📞 Tel:</b> {row['telefonos']}<br>
                                <b>🌐 Redes:</b> {row['redes_sociales']}
                            </div>
                        </div>
                        <div class="card-res">
                            <b>Informe:</b> {row['resultado'][:100]}...
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")
