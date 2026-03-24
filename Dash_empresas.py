import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Diagnóstico PFA", layout="wide")

st.title("🔍 Diagnóstico de Archivos")

# 1. Ver qué archivos hay en la carpeta
st.write("### Archivos detectados en el servidor:")
archivos = os.listdir('.')
st.write(archivos)

# 2. Intentar cargar el CSV con un método más directo
if 'data.csv' in archivos:
    st.success("✅ El archivo 'data.csv' fue detectado.")
    try:
        # Forzamos la lectura sin caché para probar
        df = pd.read_csv('data.csv', encoding='utf-8')
        st.write("### Vista previa de los datos:")
        st.dataframe(df.head())
        
        st.write("### Columnas detectadas:")
        st.write(list(df.columns))
        
    except Exception as e:
        st.error(f"❌ Error al leer el CSV: {e}")
else:
    st.error("❌ El archivo 'data.csv' NO está en la carpeta raíz.")
    st.info("Asegurate de que en GitHub el archivo esté suelto y no adentro de una carpeta.")

st.write("---")
st.write("Si ves el archivo en la lista de arriba pero da error de lectura, el problema es el formato del CSV.")
