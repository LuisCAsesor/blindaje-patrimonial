import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- CONFIGURACIÓN SEGURA DE API ---
try:
    API_KEY = st.secrets["API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    st.error("⚠️ Error de Configuración: Falta la API_KEY en los Secrets de Streamlit.")
    st.stop()

# --- EL RESTO DEL CÓDIGO SIGUE IGUAL ---
st.title("🛡️ Diagnóstico de Blindaje Patrimonial")

with st.sidebar:
    st.header("Instrucciones")
    st.write("Completa tus datos para recibir un análisis basado en la metodología de Blindaje Patrimonial.")

# --- FORMULARIO ---
with st.form("my_form"):
    nombre = st.text_input("Nombre Completo")
    edad = st.number_input("Edad", min_value=18, max_value=100, value=30)
    ingreso_anual = st.number_input("Ingresos Totales Anuales ($)", min_value=0)
    
    st.subheader("Tus Gastos Anuales (RAG)")
    g_verde = st.number_input("Gastos Necesarios (Súper, Vivienda)", min_value=0)
    g_amarillo = st.number_input("Gastos Variables (Suscripciones, Cine)", min_value=0)
    g_rojo = st.number_input("Gastos Eliminables (Gastos hormiga, Lujos)", min_value=0)
    
    st.subheader("Ahorro y Deuda Anual")
    ahorro_anual = st.number_input("¿Cuánto ahorras al año?", min_value=0)
    deuda_anual = st.number_input("¿Cuánto pagas de deudas al año?", min_value=0)

    st.subheader("¿Qué tienes hoy?")
    t_auto = st.checkbox("Seguro de Auto")
    t_vida = st.checkbox("Seguro de Vida")
    t_retiro = st.checkbox("PPR / Afore")
    
    submit = st.form_submit_button("Generar Diagnóstico")

if submit:
    # Validaciones básicas de ingresos [cite: 67]
    if ingreso_anual <= 0:
        st.warning("Por favor, ingresa un ingreso anual válido para realizar el cálculo.")
    else:
        # Lógica de deuda basada en niveles de control [cite: 59, 60, 61, 62]
        pct_deuda = (deuda_anual / ingreso_anual) * 100
        nivel_deuda = "Controlada" if pct_deuda < 30 else "Alarma" if pct_deuda <= 60 else "Peligrosa"
        
        prompt = f"""
        Genera un diagnóstico financiero para {nombre} de {edad} años.
        Datos: Ingreso ${ingreso_anual}, Ahorro ${ahorro_anual}, Deuda {nivel_deuda} ({pct_deuda:.1f}%).
        Seguros: Auto:{t_auto}, Vida:{t_vida}, Retiro:{t_retiro}.
        Gastos RAG: Verde ${g_verde}, Amarillo ${g_amarillo}, Rojo ${g_rojo}.
        
        Usa estas reglas del Blindaje Patrimonial:
        - Si tiene seguro de auto pero no de vida o retiro, dile que 'asegura el metal pero no su libertad'[cite: 190, 192].
        - Menciona que para 2050 habrá 36 millones de adultos mayores y la mayoría dependerá de otros[cite: 3, 18, 25].
        - Aplica la regla 50-30-20 para recomendar ahorro e inversión[cite: 63, 65].
        - Explica que el retiro es una certeza, mientras que un accidente es solo probabilidad.
        """
        
        try:
            with st.spinner("Consultando a tu asesor de IA..."):
                res = model.generate_content(prompt)
                st.markdown("### 📊 Tu Diagnóstico Personalizado")
                st.markdown(res.text)
        except Exception as e:
            st.error(f"Hubo un problema con la conexión a la IA. Error: {e}")
            st.info("Revisa que tu API_KEY sea válida y que tengas cuota disponible en Google AI Studio.")

