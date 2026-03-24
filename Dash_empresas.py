import streamlit as st
import pandas as pd

# 1. Configuración de pantalla para TV QLED y S25 Ultra
st.set_page_config(
    page_title="Monitor Causa 4879/2024",
    page_icon="🚔",
    layout="wide"
)

# 2. Estética "Dark Mode" Táctica
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
        background-color: rgba(52, 152, 219, 0.1);
        border-left: 4px solid #3498db;
        padding: 12px;
        margin-top: 10px;
        font-style: italic;
        border-radius: 4px;
    }
    .status-badge { font-weight: bold; padding: 5px 10px; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Base de Datos Completa (22 Empresas)
data = [
    # 1. AGROZEP S.A.
    {"id": "1", "empresa": "AGROZEP S.A.", "cuit": "30-71761370-4", "sujeto": "Sede Social", "status": "Rojo", "resultado": "Vecinos indican que no se emplaza empresa. Piso 4-9 familia, 4-10 femenino."},
    {"id": "1", "empresa": "AGROZEP S.A.", "cuit": "30-71761370-4", "sujeto": "Cristian Eduardo Frechero (Presidente)", "status": "Verde", "resultado": "Domicilio confirmado en Valentín Alsina. Perfil FB 'Cristian Pitu' con alta similitud."},
    {"id": "1", "empresa": "AGROZEP S.A.", "cuit": "30-71761370-4", "sujeto": "Matías Ezequiel Leguiza (Dir. Suplente)", "status": "Amarillo", "resultado": "Domicilio constatado en Berazategui. Redes verificadas. Restan tareas de campo."},
    # 2. PLEGATS S.A.
    {"id": "2", "empresa": "PLEGATS S.A.", "cuit": "33-70983954-9", "sujeto": "Lilian Zeni (Presidente)", "status": "Amarillo", "resultado": "Nieto indicó que reside en Monte 4445. No se encontraba al momento de la entrevista."},
    {"id": "2", "empresa": "PLEGATS S.A.", "cuit": "33-70983954-9", "sujeto": "Alicia Raquel Andino (Ex Presidente)", "status": "Rojo", "resultado": "Masculino en domicilio refirió que la investigada se encuentra fallecida."},
    {"id": "2", "empresa": "PLEGATS S.A.", "cuit": "33-70983954-9", "sujeto": "Ricardo Federico Konig (Dir. Suplente)", "status": "Rojo", "resultado": "Sin respuesta. Vecino manifestó no conocerlo y que no reside allí."},
    # 3. LFC PRODUCCIONES S.A.
    {"id": "3", "empresa": "LFC PRODUCCIONES S.A.", "cuit": "30-71153127-7", "sujeto": "Sede Social", "status": "Rojo", "resultado": "Encargado contestó que no existe empresa. Vivienda familiar."},
    {"id": "3", "empresa": "LFC PRODUCCIONES S.A.", "cuit": "30-71153127-7", "sujeto": "Nahuel Darío Núñez Guevara", "status": "Amarillo", "resultado": "Timbres averiados. Tío refirió que reside allí pero trabaja de día."},
    {"id": "3", "empresa": "LFC PRODUCCIONES S.A.", "cuit": "30-71153127-7", "sujeto": "Andrés Escudero", "status": "Amarillo", "resultado": "Madre refirió que reside allí pero se encontraba haciendo diligencias."},
    {"id": "3", "empresa": "LFC PRODUCCIONES S.A.", "cuit": "30-71153127-7", "sujeto": "Yurdren Shahar Diaz Mejía", "status": "Rojo", "resultado": "En domicilio San Pedrito 83 indicaron no conocerlo."},
    # 4. LUISANVIAL S.A.
    {"id": "4", "empresa": "LUISANVIAL S.A.", "cuit": "30-71779037-1", "sujeto": "Sede Social", "status": "Verde", "resultado": "Cartel 'Lemme-Nesterczuk Abogados'. Secretaria confirmó que allí tienen Luisanvial."},
    # 5. RIV CONSULTING S.A.
    {"id": "5", "empresa": "RIV CONSULTING S.A.", "cuit": "30-71756733-8", "sujeto": "Sede Social", "status": "Rojo", "resultado": "Encargado indicó vivienda familiar y alquiler temporario AIRBNB."},
    {"id": "5", "empresa": "RIV CONSULTING S.A.", "cuit": "30-71756733-8", "sujeto": "Gabriela Anahí Rivero", "status": "Rojo", "resultado": "En Alberdi la desconocen. En Lanús la numeración Lituania 815 no existe."},
    # 6. HCL HEALT S.A.
    {"id": "6", "empresa": "HCL HEALT S.A.", "cuit": "30-71761735-1", "sujeto": "Sede Social", "status": "Rojo", "resultado": "Masculino contestó que reside él y no existe la empresa."},
    {"id": "6", "empresa": "HCL HEALT S.A.", "cuit": "30-71761735-1", "sujeto": "Diego Fabián Carrasco", "status": "Rojo", "resultado": "Desconocido en el lugar. Timbre pertenece a otra persona."},
    # 7. BARANOA S.A.
    {"id": "7", "empresa": "BARANOA S.A.", "cuit": "Pendiente", "sujeto": "Virgilio Mario Vivarelli", "status": "Verde", "resultado": "Atendió personalmente. Convive con Gastón Vivarelli."},
    # 8. HOPKINS PRODUCCIONES S.A.
    {"id": "8", "empresa": "HOPKINS PRODUCCIONES S.A.", "cuit": "Pendiente", "sujeto": "Juan Luis Samudio Bareiro", "status": "Rojo", "resultado": "En Madero no existe ese nombre. En Caaguazú vecinos indicaron hallarlo después de 18hs."},
    # 9. VSP CONSULTING S.A.
    {"id": "9", "empresa": "VSP CONSULTING S.A.", "cuit": "30-71696932-7", "sujeto": "Sede Social", "status": "Rojo", "resultado": "Vecina desconoce la firma. Allí vive una pareja."},
    {"id": "9", "empresa": "VSP CONSULTING S.A.", "cuit": "30-71696932-7", "sujeto": "Luis Alexander Pichuaga", "status": "Amarillo", "resultado": "Timbre averiado con cartel manuscrito. Sin respuesta al teléfono indicado."},
    # 10. CIRIACO SHOES S.R.L.
    {"id": "10", "empresa": "CIRIACO SHOES S.R.L.", "cuit": "30-71679167-6", "sujeto": "Sede Social", "status": "Amarillo", "resultado": "Ingreso cerrado con cadenas. Ventana tapada con bolsa negra."},
    # 11. COXTEX S.A.
    {"id": "11", "empresa": "COXTEX S.A.", "cuit": "33-71697567-9", "sujeto": "Sede Social", "status": "Amarillo", "resultado": "Tres timbres sin especificar. Sin respuesta."},
    # 12. RECINSUR S.A.
    {"id": "12", "empresa": "RECINSUR S.A.", "cuit": "Pendiente", "sujeto": "Vinculada a Elpidio Ludueña", "status": "Amarillo", "resultado": "Mencionada en Grupo Vega. Sin domicilios directos relevados."},
    # 13. E-SCRAP OESTE S.A.
    {"id": "13", "empresa": "E-SCRAP OESTE S.A.", "cuit": "30-71645010-0", "sujeto": "Sede Social / Luis De Santis", "status": "Verde", "resultado": "Femenino manifestó conocer a De Santis y que reside allí."},
    {"id": "13", "empresa": "E-SCRAP OESTE S.A.", "cuit": "30-71645010-0", "sujeto": "Walter Gustavo Mozas", "status": "Amarillo", "resultado": "Datos confirmados en sistemas. Restan tareas de campo."},
    # 14. HEDEZA S.A.
    {"id": "14", "empresa": "HEDEZA S.A.", "cuit": "30-71601428-9", "sujeto": "Sede Social", "status": "Amarillo", "resultado": "Domicilio fijado en asambleas. Restan tareas de campo."},
    {"id": "14", "empresa": "HEDEZA S.A.", "cuit": "30-71601428-9", "sujeto": "Liliana Cosentino", "status": "Verde", "resultado": "Atendió personalmente por portero eléctrico."},
    {"id": "14", "empresa": "HEDEZA S.A.", "cuit": "30-71601428-9", "sujeto": "Elpidio Héctor Ludueña", "status": "Amarillo", "resultado": "Relación con Plegats y Recinsur. Domicilios obtenidos por bases."},
    # 15. KASEGU S.A.
    {"id": "15", "empresa": "KASEGU S.A.", "cuit": "30-71479846-0", "sujeto": "Sede Social", "status": "Amarillo", "resultado": "Domicilios históricos detectados en bases comerciales."},
    {"id": "15", "empresa": "KASEGU S.A.", "cuit": "30-71479846-0", "sujeto": "Ángel Gerardo González", "status": "Verde", "resultado": "Esposa confirmó domicilio."},
    {"id": "15", "empresa": "KASEGU S.A.", "cuit": "30-71479846-0", "sujeto": "Enrique Leonardo Chamorro", "status": "Rojo", "resultado": "Vecinos de Honorio Pueyrredón 468 manifestaron no conocerlo."},
    # 16. MDL GROUP S.A.
    {"id": "16", "empresa": "MDL GROUP S.A.", "cuit": "30-71761340-2", "sujeto": "Sede Social", "status": "Amarillo", "resultado": "Alerta de facturación apócrifa (2023). Restan tareas."},
    {"id": "16", "empresa": "MDL GROUP S.A.", "cuit": "30-71761340-2", "sujeto": "Carlos Miguel Ángel Ibañez", "status": "Verde", "resultado": "Familiar refirió que Ibañez reside allí pero no se encontraba."},
    # 17. LIGGO S.A.
    {"id": "17", "empresa": "LIGGO S.A.", "cuit": "30-71761750-5", "sujeto": "Sede Social", "status": "Amarillo", "resultado": "Pendiente confirmación de campo."},
    {"id": "17", "empresa": "LIGGO S.A.", "cuit": "30-71761750-5", "sujeto": "Marcos Daniel Santicchia", "status": "Verde", "resultado": "Positivo en Lanús. Paradero constatado por Aux. Pellegrino."},
    # 18. TECNOFRESH S.A.
    {"id": "18", "empresa": "TECNOFRESH S.A.", "cuit": "30-71759371-1", "sujeto": "Sede Social", "status": "Rojo", "resultado": "Negativo en el domicilio. Registra cheques rechazados."},
    {"id": "18", "empresa": "TECNOFRESH S.A.", "cuit": "30-71759371-1", "sujeto": "Pablo Emanuel Valverde", "status": "Amarillo", "resultado": "Confirmado en Renaper. Pendiente verificación física."},
    # 19. TELASINCIC S.A.
    {"id": "19", "empresa": "TELASINCIC S.A.", "cuit": "Sin Registros", "sujeto": "Sede Social (Empresa Fantasma)", "status": "Rojo", "resultado": "ÚNICA que NO aparece en ninguna base consultada (NOSIS, etc)."},
    # 20. GALRAZ S.A.
    {"id": "20", "empresa": "GALRAZ S.A.", "cuit": "30-71759481-5", "sujeto": "Sede Social", "status": "Amarillo", "resultado": "Pendiente de verificación en terreno."},
    {"id": "20", "empresa": "GALRAZ S.A.", "cuit": "30-71759481-5", "sujeto": "Axel Kevin Galván", "status": "Amarillo", "resultado": "Múltiples teléfonos a su nombre. Pendiente de inspección."},
    # 21. METALGE S.A.
    {"id": "21", "empresa": "METALGE S.A.", "cuit": "30-71759416-5", "sujeto": "Sede Social", "status": "Amarillo", "resultado": "Empresa activa en NOSIS. Sin tareas de campo volcadas."},
    {"id": "21", "empresa": "METALGE S.A.", "cuit": "30-71759416-5", "sujeto": "Nazareno Benítez Antolín", "status": "Amarillo", "resultado": "Dirección constatada en RENAPER."},
    # 22. KAFE S.A.
    {"id": "22", "empresa": "KAFE S.A.", "cuit": "30-71686304-9", "sujeto": "Sede Social", "status": "Amarillo", "resultado": "Firma presenta deudas bancarias y cheques rechazados."},
    {"id": "22", "empresa": "KAFE S.A.", "cuit": "30-71686304-9", "sujeto": "Ariel Klempnow", "status": "Amarillo", "resultado": "6 vehículos detectados. Falta tarea en Zarate."},
]

df = pd.DataFrame(data)

# 4. Cabecera del Dashboard
st.markdown("<h1 style='text-align: center; color: white;'>🚨 Monitor de Inteligencia PFA</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #3498db;'>Causa 4879/2024 - Relevamiento de Empresas</h3>", unsafe_allow_html=True)
st.markdown("---")

# 5. Sidebar de Control (Briefing)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/2c/Logo_de_la_Polic%C3%ADa_Federal_Argentina.png", width=150)
    st.header("Briefing Táctico")
    status_filtro = st.multiselect(
        "Filtrar Semáforo:", 
        ["Verde", "Amarillo", "Rojo"], 
        default=["Verde", "Amarillo", "Rojo"]
    )
    st.info(f"Objetivos Cargados: {len(df)}")

# 6. Lógica de Visualización
empresas = df['empresa'].unique()

for emp in empresas:
    sub_df = df[(df['empresa'] == emp) & (df['status'].isin(status_filtro))]
    
    if not sub_df.empty:
        cuit = sub_df['cuit'].iloc[0]
        st.markdown(f'<div class="company-header">{emp} <span style="float:right; font-size:0.9rem;">CUIT: {cuit}</span></div>', unsafe_allow_html=True)
        
        for _, row in sub_df.iterrows():
            with st.container():
                st.markdown('<div class="card-body">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    emoji = {"Verde": "🟢 Positivo", "Amarillo": "🟡 Pendiente", "Rojo": "🔴 Negativo"}[row['status']]
                    st.markdown(f"**{row['sujeto']}**")
                    st.write(emoji)
                
                with col2:
                    st.markdown(f'<div class="res-policial">{row["resultado"]}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

# 7. Resumen Final
st.markdown("---")
st.caption(f"Visualización generada para Briefing - Total en vista: {len(df[df['status'].isin(status_filtro)])}")
