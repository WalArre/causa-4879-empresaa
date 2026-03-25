import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from fpdf import FPDF

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
                if clave == "Dicco1272":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("⚠️ Acceso Denegado")
        return False
    return True

if login():
    st.set_page_config(page_title="PFA - Causa 4879", layout="wide")

    # 2. CSS TÁCTICO
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
.mission-box { background-color: rgba(52, 152, 219, 0.1); border-left: 5px solid #3498db; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

    @st.cache_data
    def load_data():
        df = pd.read_csv('data.csv', sep=None, engine='python', encoding='utf-8')
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        return df

    # --- FUNCIÓN GENERADORA DE PDF EN CUADRITOS ---
    def generar_pdf(df_filtrado):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Helper para evitar errores con tildes y eñes
        def cln(texto):
            return str(texto).encode('latin-1', 'replace').decode('latin-1')

        # Título del Documento
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, txt=cln("Reporte de Inteligencia - Causa 4879"), ln=True, align='C')
        pdf.ln(5)

        empresas = df_filtrado['empresa'].unique()

        for emp in empresas:
            data_emp = df_filtrado[df_filtrado['empresa'] == emp]
            cuit_label = data_emp['cuit'].iloc[0]

            # Cuadro de la Empresa (Fondo Azul)
            pdf.set_fill_color(41, 128, 185) # Azul PFA
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", 'B', 11)
            titulo_empresa = cln(f" EMPRESA: {emp} | CUIT: {cuit_label}")
            pdf.cell(0, 8, txt=titulo_empresa, ln=True, fill=True)

            pdf.set_text_color(0, 0, 0) # Volver texto a negro
            
            # Cuadritos de los Integrantes
            for _, row in data_emp.iterrows():
                estado = row['status']
                # Colores según semáforo
                if estado == 'Verde':
                    pdf.set_fill_color(200, 247, 205) # Verde suave
                elif estado == 'Amarillo':
                    pdf.set_fill_color(255, 249, 196) # Amarillo suave
                else:
                    pdf.set_fill_color(255, 205, 210) # Rojo suave

                # Nombre y Estado
                pdf.set_font("Arial", 'B', 10)
                sujeto_str = cln(f" Objetivo: {row['sujeto']} [{estado.upper()}]")
                pdf.cell(0, 7, txt=sujeto_str, ln=True, fill=True, border=1)

                # Datos (Dom, Tel, Redes)
                pdf.set_font("Arial", '', 9)
                info_str = cln(f" Dom: {row['domicilio']} | Tel: {row['telefonos']}\n Redes: {row['redes_sociales']}")
                pdf.multi_cell(0, 5, txt=info_str, border=1)

                # Reporte Policial
                pdf.set_font("Arial", 'I', 9)
                res_str = cln(f" Informe: {row['resultado']}")
                pdf.multi_cell(0, 5, txt=res_str, border=1)
                
                pdf.ln(2) # Espacio entre personas
            pdf.ln(4) # Espacio entre empresas

        # Devolver el PDF armado en formato bytes
        return pdf.output(dest='S').encode('latin-1')
    # -----------------------------------------------

    try:
        df = load_data()
        st.markdown("<h1 style='text-align: center;'>🚨 Monitoreo de Redes Societarias - Causa 4879</h1>", unsafe_allow_html=True)

        st.markdown("""
        <div class="mission-box">
            <h4 style="color: #3498db; margin-top: 0;">📋 Objetivo del Requerimiento</h4>
            <p style="margin-bottom: 0; font-size: 0.95rem; color: #e0e0e0; line-height: 1.5;">
                En el marco de la presente investigación, se solicitó a esta Unidad el chequeo exhaustivo de las sociedades comerciales vinculadas a la causa. Las tareas comprenden el <b>desglose de personal y directivos</b>, y la <b>constatación física y compulsa de bases</b> para verificar domicilios, medios de contacto y operatividad real en el terreno.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # FILTROS
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

        # BOTÓN DE DESCARGA PDF
        if not df_final.empty:
            pdf_bytes = generar_pdf(df_final)
            st.download_button(
                label="📄 Descargar Reporte Estructurado (PDF)",
                data=pdf_bytes,
                file_name="Reporte_Inteligencia_4879.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("No hay resultados para exportar con los filtros actuales.")
            
        st.markdown("---")

        tab_m, tab_g = st.tabs(["📍 MAPA OPERATIVO", "🏢 ÍNDICE DE EMPRESAS"])

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
