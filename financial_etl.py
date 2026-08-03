import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Financial ETL", layout="wide", initial_sidebar_state="collapsed")

# Estética abstracta y minimalista (Acrílico/Vidrio)
st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-top: 1px solid rgba(255,255,255,0.1);
        border-left: 1px solid rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 8px;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def execute_etl():
    # EXTRACT: Generación de datos simulados desde Enero 2026
    fechas = pd.date_range(start="2026-01-01", periods=180)
    df = pd.DataFrame({
        'Fecha': fechas,
        'Ingresos_Brutos': np.random.normal(500000, 25000, len(fechas)),
        'Gastos_Operativos': np.random.normal(300000, 15000, len(fechas))
    })
    
    # TRANSFORM: Limpieza y cálculo de KPIs
    df['Margen_Neto'] = df['Ingresos_Brutos'] - df['Gastos_Operativos']
    df['SMA_30_Margen'] = df['Margen_Neto'].rolling(window=30).mean()
    df.dropna(inplace=True)
    
    # LOAD: Simulación de carga
    return df

# Ejecución del pipeline
df_clean = execute_etl()

st.title("Consolidación Financiera (Automated ETL)")
st.markdown('<hr style="border-color: rgba(255,255,255,0.1);">', unsafe_allow_html=True)

# Layout de métricas
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total Ingresos (2026)", f"${df_clean['Ingresos_Brutos'].sum():,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Promedio Margen Diario", f"${df_clean['Margen_Neto'].mean():,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Estado del Pipeline", "OPERATIVO", delta="0 Errores")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("<br>", unsafe_allow_html=True)

# Visualización
st.markdown('<div class="metric-card">', unsafe_allow_html=True)
st.subheader("Tendencia de Margen Neto vs Media Móvil (30 días)")
st.line_chart(df_clean.set_index('Fecha')[['Margen_Neto', 'SMA_30_Margen']], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
