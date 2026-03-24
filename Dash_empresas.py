import streamlit as st
import pandas as pd

# 1. Configuración de Pantalla (Modo TV y Celular)
st.set_page_config(
    page_title="PFA - Causa 4879/2024",
    page_icon="🚔",
    layout="wide"
)

# 2. Estética Táctica (Dark Mode Oficial)
st.markdown("""
    <style>
    .main { background-color: #0d1b2a; color: #e0e0e0; }
    .stApp { background-color: #0d1b2a; }
    .metric-card {
        background-color: #162636;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #1a3a5a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-value { font-size: 2.5rem; font-weight: bold; }
    .val-verde { color: #2ecc71; }
    .val-amarillo { color: #f1c40f; }
    .val-rojo { color: #e74c3c; }
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
        border-top: none;
        margin-bottom: 15px;
    }
    .res-policial {
        background-color: rgba(52, 152, 219, 0.05);
        border-left: 4px solid #3498db;
        padding: 12px;
        font-style: italic;
        border-radius: 4px;
        margin-top: 5px;
    }
    .data-label { color: #adb5bd; font-size: 0.85rem; text-transform: uppercase; }
    .data-value { font-weight: 500; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Base de Datos Completa (Extraída de HTML)
data = [
    {"empresa": "AGROZEP S.A.", "cuit": "30-71761370-4", "sujeto": "Sede Social", "status": "Rojo", "domicilio": "Av. Martin García 551 Piso 4, CABA", "resultado": "Vecinos respondieron que según sus conocimientos no se emplaza una empresa. En el piso '4° 9' viviría una familia y en el '4° 10' vive un femenino."},
    {"empresa": "AGROZEP S.A.", "cuit": "30-71761370-4", "sujeto": "Cristian Eduardo Frechero", "status": "Verde", "domicilio": "Coronel Delia 2862 PB Dpto 4, Valentín Alsina, PBA", "resultado": "Base IDGE y Renaper confirman domicilio. Perfil de Facebook activo hallado con rasgos de extrema similitud."},
    {"empresa": "AGROZEP S.A.", "cuit": "30-71761370-4", "sujeto": "Matías Ezequiel Leguiza", "status": "Amarillo", "domicilio": "Calle 1320 e/ 21 y 22 N° 2121, Berazategui, PBA", "resultado": "Domicilio constatado en bases de datos. Redes sociales verificadas. Restan tareas de campo en el lugar."},
    {"empresa": "PLEGATS S.A.", "cuit": "33-70983954-9", "sujeto": "Lilian Zeni", "status": "Amarillo", "domicilio": "Monte 4448 / Monte 4450, CABA", "resultado": "Se tocó timbre en Monte 4448. Atendió un nieto e indicó que la investigada (su abuela) reside en el domicilio de numeración 4445, pero que no se encontraba al momento de la entrevista."},
    {"empresa": "PLEGATS S.A.", "cuit": "33-70983954-9", "sujeto": "Alicia Raquel Andino", "status": "Rojo", "domicilio": "Monte 4450, CABA", "resultado": "Al constituirse en Monte 4450, un masculino de 25 años refirió que la señora Alicia Andino se encuentra fallecida."},
    {"empresa": "PLEGATS S.A.", "cuit": "33-70983954-9", "sujeto": "Ricardo Federico Konig", "status": "Rojo", "domicilio": "Monte 4561, CABA", "resultado": "Sin respuesta al timbre. Vecino consultado manifestó no conocerlo y que no reside allí."},
    {"empresa": "LFC PRODUCCIONES S.A.", "cuit": "30-71153127-7", "sujeto": "Sede Social", "status": "Rojo", "domicilio": "Esmeralda 570 Piso 1 Of 'D', CABA", "resultado": "Encargado del edificio contestó que no se emplaza una empresa en el lugar y que se trata de una vivienda familiar."},
    {"empresa": "LFC PRODUCCIONES S.A.", "cuit": "30-71153127-7", "sujeto": "Nahuel Darío Núñez Guevara", "status": "Amarillo", "domicilio": "L. Beláustegui 4535 Piso 2, CABA", "resultado": "Timbres averiados. Un masculino en las cercanías indicó ser su tío, refiriendo que el investigado reside en el departamento 2, pero que trabaja de día y no se encontraba."},
    {"empresa": "LFC PRODUCCIONES S.A.", "cuit": "30-71153127-7", "sujeto": "Andrés Ricardo Horacio Escudero", "status": "Amarillo", "domicilio": "Balbastro 1775, CABA", "resultado": "Atendido por femenino (su madre) quien refirió que el encartado reside en el lugar pero se había retirado a hacer diligencias."},
    {"empresa": "LFC PRODUCCIONES S.A.", "cuit": "30-71153127-7", "sujeto": "Yurdren Shahar Diaz Mejía", "status": "Rojo", "domicilio": "San Pedrito 83 / La Paz 1218 B, Ramos Mejía", "resultado": "En San Pedrito 83 atendió un masculino indicando no conocerlo y que no reside allí."},
    {"empresa": "LUISANVIAL S.A.", "cuit": "30-71779037-1", "sujeto": "Sede Social", "status": "Verde", "domicilio": "Lavalle 1447 Piso 2 Dpto E, CABA", "resultado": "Cartel reza 'Lemme-Nesterczuk Abogados'. Secretaria consultó en grupo interno y le confirmaron que allí 'tienen Luisanvial'."},
    {"empresa": "RIV CONSULTING S.A.", "cuit": "30-71756733-8", "sujeto": "Sede Social", "status": "Rojo", "domicilio": "Esmeralda 570 Piso 3 Of 7, CABA", "resultado": "Encargado indicó que existen dos departamentos en esa ubicación: una vivienda familiar y otro destinado a alquiler temporario tipo AIRBNB."},
    {"empresa": "RIV CONSULTING S.A.", "cuit": "30-71756733-8", "sujeto": "Gabriela Anahí Rivero", "status": "Rojo", "domicilio": "Av. J. B. Alberdi 4054 PB 4, CABA", "resultado": "En Alberdi vecinos manifiestan desconocerla. En Lanús la numeración Lituania 815 no existe y vecinos la desconocen."},
    {"empresa": "HCL HEALT S.A.", "cuit": "30-71761735-1", "sujeto": "Sede Social", "status": "Rojo", "domicilio": "Aristóbulo Del Valle 1357 Piso 3 A, CABA", "resultado": "Atendido por un masculino quien contestó que en el lugar reside él y no existe tal empresa."},
    {"empresa": "HCL HEALT S.A.", "cuit": "30-71761735-1", "sujeto": "Diego Fabián Carrasco", "status": "Rojo", "domicilio": "Formosa 1035, Lanús Oeste, PBA", "resultado": "Inquilino del edificio constató que el investigado es desconocido en el lugar. Timbre 1035 lateral pertenece a un hombre con distinto nombre."},
    {"empresa": "BARANOA S.A.", "cuit": "Pendiente", "sujeto": "Virgilio Mario Vivarelli", "status": "Verde", "domicilio": "Av. Avellaneda 4050 Piso 8 Dpto D, CABA", "resultado": "Atendió personalmente en el domicilio y refirió que convive allí con Gastón Martín Vivarelli."},
    {"empresa": "HOPKINS PRODUCCIONES S.A.", "cuit": "Pendiente", "sujeto": "Juan Luis Samudio Bareiro", "status": "Rojo", "domicilio": "Madero 712, CABA / Caaguazú 6735 Dpto A", "resultado": "En Madero vecina indicó que no posee ese nombre. En J.A. García 1868 sin respuestas. En Caaguazú vecinos indicaron que se lo encuentra luego de las 18 hs (Pendiente confirmación visual)."},
    {"empresa": "VSP CONSULTING S.A.", "cuit": "30-71696932-7", "sujeto": "Sede Social", "status": "Rojo", "domicilio": "Guardia Nacional 1221, CABA", "resultado": "Timbre averiado. Vecina lindante manifiesta que desconoce la firma, que allí vive una pareja y que ya varias veces le habían consultado por la firma."},
    {"empresa": "VSP CONSULTING S.A.", "cuit": "30-71696932-7", "sujeto": "Luis Alexander Pichuaga", "status": "Amarillo", "domicilio": "Camarones 4383, CABA", "resultado": "Inmueble posee dos ingresos (A y B). Timbre averiado con cartel manuscrito 'TIMBRE NO ANDA LLAMAR AL 1133796680'. Se llamó a dicho número sin obtener respuesta."},
    {"empresa": "CIRIACO SHOES S.R.L.", "cuit": "30-71679167-6", "sujeto": "Sede Social", "status": "Amarillo", "domicilio": "Chascomús 5349, CABA", "resultado": "Ingreso vehicular cerrado con candado y cadenas. Ventana tapada con bolsa de plástico negro. Sin respuestas."},
    {"empresa": "COXTEX S.A.", "cuit": "33-71697567-9", "sujeto": "Sede Social", "status": "Amarillo", "domicilio": "Av. Montes de Oca 242, CABA", "resultado": "Tres timbres sin especificar. Se presionaron todos sin obtener respuesta alguna."},
    {"empresa": "RECINSUR S.A.", "cuit": "Pendiente", "sujeto": "Vinculada a Elpidio Ludueña", "status": "Amarillo", "domicilio": "Sin Datos", "resultado": "Mencionada dentro del Grupo Vega / Vinculaciones directivas. Sin domicilios directos relevados en los reportes de campo."},
    {"empresa": "E-SCRAP OESTE S.A.", "cuit": "30-71645010-0", "sujeto": "Sede Social / Luis Pascual De Santis", "status": "Verde", "domicilio": "Lacarra 1675, CABA", "resultado": "El domicilio de la empresa coincide con el del presidente. Atendió un femenino quien manifestó conocer a Luis Pascual De Santis y que el nombrado reside efectivamente en dicho domicilio."},
    {"empresa": "E-SCRAP OESTE S.A.", "cuit": "30-71645010-0", "sujeto": "Walter Gustavo Mozas", "status": "Amarillo", "domicilio": "Famaillá 685 PB B, Lomas del Mirador, PBA", "resultado": "Datos confirmados por Renaper e IDGE. Restan tareas de campo."},
    {"empresa": "HEDEZA S.A.", "cuit": "30-71601428-9", "sujeto": "Sede Social", "status": "Amarillo", "domicilio": "Aristóbulo Fernández 1432, CABA", "resultado": "Domicilio fijado en asambleas societarias. Restan tareas de campo."},
    {"empresa": "HEDEZA S.A.", "cuit": "30-71601428-9", "sujeto": "Liliana Cosentino", "status": "Verde", "domicilio": "José Bonifacio 2456 Piso 2 Dpto 202, Flores, CABA", "resultado": "Mediante contacto a través del portero eléctrico en José Bonifacio 2456, atendió un femenino manifestando ser efectivamente la Sra. Liliana Cosentino."},
    {"empresa": "HEDEZA S.A.", "cuit": "30-71601428-9", "sujeto": "Elpidio Héctor Ludueña", "status": "Amarillo", "domicilio": "Gdor. Castro 50, San Isidro, PBA", "resultado": "Posee relación también con Plegats S.A. y Recinsur S.A. Domicilios obtenidos por bases de datos."},
    {"empresa": "KASEGU S.A.", "cuit": "30-71479846-0", "sujeto": "Sede Social", "status": "Amarillo", "domicilio": "Armenia 2121 Piso 6 Dpto B, CABA", "resultado": "Domicilios fiscales y reales históricos detectados en bases comerciales."},
    {"empresa": "KASEGU S.A.", "cuit": "30-71479846-0", "sujeto": "Ángel Gerardo González", "status": "Verde", "domicilio": "Av. Benedetti 2100 Torre 3B Piso 11 Dpto F, Dock Sud, PBA", "resultado": "Al concurrir al domicilio aportado, el personal fue atendido por una mujer que manifestó ser su esposa, confirmando que el investigado registra domicilio allí."},
    {"empresa": "KASEGU S.A.", "cuit": "30-71479846-0", "sujeto": "Enrique Leonardo Chamorro", "status": "Rojo", "domicilio": "Dr. Honorio Pueyrredón 468, CABA", "resultado": "En el domicilio de CABA, Honorio Pueyrredón 468, se entrevistó a vecinos del inmueble, quienes manifestaron no conocerlo."},
    {"empresa": "MDL GROUP S.A.", "cuit": "30-71761340-2", "sujeto": "Sede Social", "status": "Amarillo", "domicilio": "Santo Domingo 2486 Piso 3 Dpto A, CABA", "resultado": "Registra alerta de facturación apócrifa (2023). Restan tareas sobre la sede social."},
    {"empresa": "MDL GROUP S.A.", "cuit": "30-71761340-2", "sujeto": "Carlos Miguel Ángel Ibañez", "status": "Verde", "domicilio": "Calle 54 N° 4860, Hudson, Berazategui, PBA", "resultado": "En el lugar, personal se entrevistó con un masculino familiar del investigado, quien refirió que Ibañez reside en el domicilio, aunque no se encontraba al momento."},
    {"empresa": "LIGGO S.A.", "cuit": "30-71761750-5", "sujeto": "Sede Social", "status": "Amarillo", "domicilio": "Bolívar 1856, CABA", "resultado": "Domicilio fiscal detectado en Nosis. Pendiente confirmación de campo."},
    {"empresa": "LIGGO S.A.", "cuit": "30-71761750-5", "sujeto": "Marcos Daniel Santicchia", "status": "Verde", "domicilio": "Av. Pdte. Bernardino Rivadavia 1448 Piso 1, Lanús, PBA", "resultado": "Resultado positivo de campo en la dirección de Lanús (Reporte de Aux. 5° Pellegrino). Se constató el paradero del investigado."},
    {"empresa": "TECNOFRESH S.A.", "cuit": "30-71759371-1", "sujeto": "Sede Social", "status": "Rojo", "domicilio": "Ruy Díaz De Guzmán 300 Piso 1, CABA", "resultado": "Resultado de tareas de campo negativo/inexistente en el domicilio Ruy Díaz De Guzmán. Empresa registra cheques rechazados por BCRA."},
    {"empresa": "TECNOFRESH S.A.", "cuit": "30-71759371-1", "sujeto": "Pablo Emanuel Valverde", "status": "Amarillo", "domicilio": "Calle 159 N° 2221 (e/ 22 y 23), Berazategui, PBA", "resultado": "Domicilio confirmado en sistemas Renaper/Workmanagement. Pendiente verificación física."},
    {"empresa": "TELASINCIC S.A.", "cuit": "Sin Registros", "sujeto": "Sede Social (Empresa Fantasma)", "status": "Rojo", "domicilio": "Desconocido", "resultado": "De la totalidad de las empresas de la causa, es la ÚNICA que NO aparece registrada en ninguna de las bases de datos consultadas (NOSIS, NORISK, etc)."},
    {"empresa": "GALRAZ S.A.", "cuit": "30-71759481-5", "sujeto": "Sede Social", "status": "Amarillo", "domicilio": "Herrera 1500, CABA", "resultado": "Domicilio obtenido de compulsa. Pendiente de verificación en terreno."},
    {"empresa": "GALRAZ S.A.", "cuit": "30-71759481-5", "sujeto": "Axel Kevin Galván", "status": "Amarillo", "domicilio": "San Lorenzo 1821, Lanús Este, PBA", "resultado": "Múltiples teléfonos a su nombre. Pendiente de inspección de campo."},
    {"empresa": "METALGE S.A.", "cuit": "30-71759416-5", "sujeto": "Sede Social", "status": "Amarillo", "domicilio": "Osvaldo Cruz 2600, CABA", "resultado": "Empresa activa en NOSIS. Sin tareas de campo volcadas aún."},
    {"empresa": "METALGE S.A.", "cuit": "30-71759416-5", "sujeto": "Nazareno Benítez Antolín", "status": "Amarillo", "domicilio": "Yatay 309, Valentín Alsina, PBA", "resultado": "Dirección constatada en RENAPER y Workmanagement."},
    {"empresa": "KAFE S.A.", "cuit": "30-71686304-9", "sujeto": "Sede Social", "status": "Amarillo", "domicilio": "Ruta 9 Km 78.7, Campana", "resultado": "Firma presenta deudas en bancos y cheques rechazados."},
    {"empresa": "KAFE S.A.", "cuit": "30-71686304-9", "sujeto": "Ariel Klempnow", "status": "Amarillo", "domicilio": "Gallesio 250 Piso 1 / Belgrano 660, Zarate, PBA", "resultado": "Datos arrojados por las bases consultadas. Falta tarea en Zarate."}
]

df = pd.DataFrame(data)

# 4. Cabecera Institucional
st.markdown("<h1 style='text-align: center;'>🚨 Inteligencia PFA - Sala de Situación</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #3498db; margin-bottom: 30px;'>Causa 4879/2024 - Despliegue Operativo</h3>", unsafe_allow_html=True)

# 5. Resumen de Mando (Métricas Rápidas)
total_verde = len(df[df['status'] == 'Verde'])
total_amarillo = len(df[df['status'] == 'Amarillo'])
total_rojo = len(df[df['status'] == 'Rojo'])

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 1.2rem; font-weight: bold; color: #e0e0e0;">Positivos (Confirmados)</div>
        <div class="metric-value val-verde">{total_verde}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 1.2rem; font-weight: bold; color: #e0e0e0;">Pendientes (Tareas Restantes)</div>
        <div class="metric-value val-amarillo">{total_amarillo}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 1.2rem; font-weight: bold; color: #e0e0e0;">Negativos (Falsos/Inexistentes)</div>
        <div class="metric-value val-rojo">{total_rojo}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 6. Sidebar (Filtros Tácticos)
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

# 7. Motor de Visualización (Tarjetas de Empresas)
empresas = df['empresa'].unique()

for emp in empresas:
    sub_df = df[(df['empresa'] == emp) & (df['status'].isin(status_filtro))]
    
    if not sub_df.empty:
        cuit = sub_df['cuit'].iloc[0]
        # Título de la Empresa
        st.markdown(f"""
        <div class="company-header">
            🏢 {emp} <span style="float:right; font-size:1rem; color:#adb5bd;">CUIT: {cuit}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Tarjetas de Objetivos
        for _, row in sub_df.iterrows():
            with st.container():
                emoji = {"Verde": "🟢", "Amarillo": "🟡", "Rojo": "🔴"}[row['status']]
                st.markdown(f"""
                <div class="card-body">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <span style="font-size: 1.1rem; font-weight: bold;">{emoji} {row['sujeto']}</span>
                    </div>
                    <div class="data-label">📍 Domicilio Relevado</div>
                    <div class="data-value">{row['domicilio']}</div>
                    <div class="data-label">📝 Reporte de Campo</div>
                    <div class="res-policial">{row['resultado']}</div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<br><hr><p style='text-align: center; color: #adb5bd; font-size: 0.8rem;'>Generado para Briefing de Comando - PFA Inteligencia</p>", unsafe_allow_html=True)
