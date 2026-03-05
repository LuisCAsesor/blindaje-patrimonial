import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Blindaje Patrimonial", layout="centered")

# Configuración de API
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ Falta la API Key en los Secrets de Streamlit.")
    st.stop()

# ESTA LÍNEA ES CLAVE PARA QUITAR EL ERROR 404
genai.configure(api_key=api_key)

# Inicializamos el modelo de forma segura
try:
    # Usamos el nombre exacto que pide la API estable
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error al configurar el modelo: {e}")

st.title("🛡️ Diagnóstico de Blindaje Patrimonial")
st.write("Calcula tu situación actual y el impacto del tiempo en tu dinero.")

# --- NUEVOS CAMPOS ---
col1, col2 = st.columns(2)
with col1:
    edad = st.number_input("Tu edad actual:", min_value=18, max_value=100, value=30)
with col2:
    monto_ahorro = st.number_input("Ahorro actual (estimado):", min_value=0, value=15000)

user_input = st.text_area("Describe otros activos (casa, ropa, juguetes, etc.):")

if st.button("¡Generar mi Diagnóstico!"):
    if user_input:
        with st.spinner("Calculando impacto financiero..."):
            try:
                # Prompt diseñado para calcular "dinero perdido" por inflación/falta de blindaje
                prompt = f"""
                Actúa como un experto en blindaje patrimonial y finanzas.
                Datos del cliente:
                - Edad: {edad} años.
                - Ahorros: {monto_ahorro} USD (o moneda local).
                - Otros activos: {user_input}
                
                Objetivo:
                1. Calcula cuánto dinero ha perdido este cliente por inflación en los últimos 5 años si ese ahorro no estuvo blindado.
                2. Proyecta cuánto perderá en los próximos 10 años si no toma acción.
                3. Da un diagnóstico de blindaje basado en su edad ({edad} años).
                """
                
                response = model.generate_content(prompt)
                
                st.subheader("📊 Análisis de Pérdida y Blindaje")
                st.markdown(response.text)
                
            except Exception as e:
                # Si el error 404 vuelve a salir, es por la versión de la librería
                st.error("Error de comunicación con la IA.")
                st.info(f"Detalle: {e}")
    else:
        st.warning("Por favor, describe tus activos para el análisis.")
