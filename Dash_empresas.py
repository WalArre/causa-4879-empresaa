import streamlit as st
import pandas as pd

# Configuración para TV y Celular
st.set_page_config(page_title="PFA - Causa 4879/2024", layout="wide")

# Estética Táctica (Dark Mode)
st.markdown("""
    <style>
    .main { background-color: #0d1b2a; color: #e0e0e0; }
    .stApp { background-color: #0d1b2a; }
    .company-card { 
        background-color: #1a3a5a; 
        padding: 15px; 
        border-radius: 10px; 
        margin-bottom: 15px;
        border-left: 5px solid #3498db;
    }
    .res-policial { 
        background-color: rgba(255,255,255,0.05); 
        padding: 10px; 
        border-radius: 5px; 
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# Datos extraídos de tu reporte
data = [
    {"empresa": "AGROZEP S.A.", "sujeto": "Sede Social", "status": "Rojo", "resultado": "Vecinos indican que no se emplaza empresa. Vivienda familiar."},
    {"empresa": "AGROZEP S.A.", "sujeto": "Cristian Eduardo Frechero", "status": "Verde", "resultado": "Domicilio confirmado por IDGE y Renaper. Perfil FB hallado."},
    {"empresa": "PLEGATS S.A.", "sujeto": "Lilian Zeni", "status": "Amarillo", "resultado": "Atendió nieto. Refiere que vive en el 4445. Resta entrevista."},
    {"empresa": "PLEGATS S.A.", "sujeto": "Alicia Raquel Andino", "status": "Rojo", "resultado": "Masculino refirió que la investigada se encuentra fallecida."},
    {"empresa": "LUISANVIAL S.A.", "sujeto": "Sede Social", "status": "Verde", "resultado": "Cartel 'Lemme-Nesterczuk Abogados'. Confirmaron firma Luisanvial."},
    {"empresa": "TELASINCIC S.A.", "sujeto": "Sede Social", "status": "Rojo", "resultado": "Empresa Fantasma. Sin registros en bases de datos."},
    {"empresa": "E-SCRAP OESTE S.A.", "sujeto": "Luis Pascual De Santis", "status": "Verde", "resultado": "Confirmado por femenino en el lugar. Reside allí."},
    {"empresa": "BARANOA S.A.", "sujeto": "Virgilio Mario Vivarelli", "status": "Verde", "resultado": "Atendió personalmente. Convive con Gastón Vivarelli."},
    {"empresa": "KASEGU S.A.", "sujeto": "Ángel Gerardo González", "status": "Verde", "resultado": "Esposa confirmó que registra domicilio en el lugar."},
    {"empresa": "LIGGO S.A.", "sujeto": "Marcos Daniel Santicchia", "status": "Verde", "resultado": "Resultado positivo en Lanús. Paradero constatado."},
] # Podes ir agregando las 22 aquí siguiendo el mismo formato

df = pd.DataFrame(data)

# Título
st.title("🚔 Monitor de Inteligencia - PFA")
st.subheader("Causa 4879/2024 - Relevamiento de Empresas")

# Filtros para el Jefe
status_filtro = st.multiselect("Filtrar por prioridad:", ["Verde", "Amarillo", "Rojo"], default=["Verde", "Amarillo", "Rojo"])

# Mostrar Tarjetas
for _, row in df[df['status'].isin(status_filtro)].iterrows():
    color_emoji = {"Verde": "🟢", "Amarillo": "🟡", "Rojo": "🔴"}[row['status']]
    with st.container():
        st.markdown(f"""
        <div class="company-card">
            <h4>{color_emoji} {row['empresa']}</h4>
            <p><b>Objetivo:</b> {row['sujeto']}</p>
            <div class="res-policial"><b>Informe de campo:</b> {row['resultado']}</div>
        </div>
        """, unsafe_allow_html=True)

st.sidebar.info(f"Total de objetivos visualizados: {len(df[df['status'].isin(status_filtro)])}")
