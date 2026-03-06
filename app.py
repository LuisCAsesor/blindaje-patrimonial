import streamlit as st
import google.generativeai as genai

# Configura tu API Key (En producción usa st.secrets)
genai.configure(api_key="TU_API_KEY_AQUÍ")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🛡️ Diagnóstico de Blindaje Patrimonial")

# --- SECCIÓN 1: DATOS PERSONALES ---
nombre = st.text_input("Nombre Completo")
edad = st.number_input("Edad", min_value=18, max_value=100)
ingreso_mensual = st.number_input("Ingresos Mensuales ($)", min_value=0)

# --- SECCIÓN 2: INSTRUMENTOS ---
st.subheader("Tus Seguros e Instrumentos")
seguros = st.multiselect("Selecciona lo que ya tienes:", 
    ["Seguro de Auto", "Seguro de Gastos Médicos", "Seguro de Vida", "PPR / Afore", "Inversiones"])

# --- SECCIÓN 3: GASTOS Y DEUDA ---
st.subheader("Tus Finanzas")
gastos_fijos = st.number_input("Gastos Necesarios (Renta, Súper, Servicios)", min_value=0)
gastos_variables = st.number_input("Gastos Variables (Starbucks, Salidas, Ocio)", min_value=0)
pago_deudas = st.number_input("Monto mensual para pagar deudas", min_value=0)

if st.button("Generar Diagnóstico"):
    # Lógica de niveles de deuda [cite: 60, 61, 62]
    ratio_deuda = (pago_deudas / ingreso_mensual) * 100 if ingreso_mensual > 0 else 0
    nivel_deuda = "Controlada" if ratio_deuda < 30 else "Alarma" if ratio_deuda <= 60 else "Peligrosa"
    
    # Prompt para la IA
    prompt = f"""
    Eres un consultor financiero experto. Analiza este perfil:
    Nombre: {nombre}, Edad: {edad} años.
    Ingresos: {ingreso_mensual}. Deuda: {nivel_deuda} ({ratio_deuda}%).
    Instrumentos actuales: {seguros}.
    Gastos: Fijos {gastos_fijos}, Variables {gastos_variables}.
    
    Instrucciones:
    1. Clasifica los gastos usando la Estrategia RAG (Rojo/Amarillo/Verde).
    2. Aplica la Regla 50-30-20.
    3. Si tiene Seguro de Auto pero NO tiene PPR o Seguro de Vida, lanza una alerta sobre "asegurar metal vs asegurar libertad".
    4. Usa un tono motivador pero directo, mencionando que 'El retiro es una certeza'[cite: 191].
    """
    
    respuesta = model.generate_content(prompt)
    st.markdown(respuesta.text)
