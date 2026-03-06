import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="IA Blindaje Patrimonial", page_icon="🛡️")

# --- CONEXIÓN SEGURA CON GEMINI ---
try:
            with st.spinner("Generando tu Blindaje Patrimonial..."):
                # Forzamos la generación con el modelo base
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown("---")
                    st.markdown(response.text)
                else:
                    st.warning("La IA no devolvió respuesta. Revisa tu cuota en Google AI Studio.")
                    
        except Exception as e:
            # Si vuelve a fallar el 404, intentamos con el modelo Pro automáticamente
            st.warning("Intentando con modelo alternativo por error de ruta...")
            try:
                model_alt = genai.GenerativeModel('gemini-pro')
                response = model_alt.generate_content(prompt)
                st.markdown(response.text)
            except:
                st.error(f"Error persistente de Google API: {e}")
                st.info("Verifica en AI Studio que tu API KEY tenga habilitado 'Gemini 1.5 Flash'.")

st.title("🛡️ Diagnóstico de Blindaje Patrimonial")
st.markdown("_El secreto para que tu estilo de vida nunca tenga fecha de caducidad._")

# --- FORMULARIO DE ENTRADA ---
with st.form("diagnostico_form"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre Completo")
        edad = st.number_input("Edad actual", min_value=18, max_value=100, value=30)
    with col2:
        ingreso_anual = st.number_input("Ingresos Totales Anuales ($)", min_value=0, step=1000)

    st.subheader("🚦 Tus Gastos Anuales (Estrategia RAG)")
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        g_verde = st.number_input("VERDE (Necesarios)", help="Súper, Renta, Servicios", min_value=0)
    with col_g2:
        g_amarillo = st.number_input("AMARILLO (Reducibles)", help="Restaurantes, Suscripciones", min_value=0)
    with col_g3:
        g_rojo = st.number_input("ROJO (Eliminables)", help="Gastos hormiga, lujos innecesarios", min_value=0)

    st.subheader("💰 Ahorro y Deuda (Monto Anual)")
    col_ad1, col_ad2 = st.columns(2)
    with col_ad1:
        ahorro_anual = st.number_input("Ahorro/Inversión total al año", min_value=0)
    with col_ad2:
        deuda_anual = st.number_input("Pago de deudas total al año", min_value=0)

    st.subheader("🛡️ Tus Instrumentos Actuales")
    t_auto = st.checkbox("Seguro de Auto")
    t_gastos_medicos = st.checkbox("Seguro de Gastos Médicos Mayores")
    t_vida = st.checkbox("Seguro de Vida")
    t_ppr = st.checkbox("PPR / Afore")
    
    seguros_lista = []
    if t_auto: seguros_lista.append("Seguro de Auto")
    if t_gastos_medicos: seguros_lista.append("Gastos Médicos")
    if t_vida: seguros_lista.append("Seguro de Vida")
    if t_ppr: seguros_lista.append("PPR/Afore")

    enviar = st.form_submit_button("GENERAR DIAGNÓSTICO")

# --- LÓGICA DE PROCESAMIENTO ---
if enviar:
    if ingreso_anual <= 0:
        st.warning("Por favor, ingresa tus ingresos anuales para continuar.")
    else:
        # 1. Análisis de Deuda (Página 7 del PDF)
        pct_deuda = (deuda_anual / ingreso_anual) * 100
        if pct_deuda < 30:
            nivel_d = "CONTROLADA (Menos del 30%)"
        elif 40 <= pct_deuda <= 60:
            nivel_d = "ALARMA (Entre 40% y 60%)"
        else:
            nivel_d = "PELIGROSA (Más del 60%)"

        # 2. Análisis de Ahorro (Regla 50-30-20 - Página 8)
        pct_ahorro = (ahorro_anual / ingreso_anual) * 100
        
        # 3. Prompt con Estrategia de Ventas y Blindaje
        prompt = f"""
        Actúa como un experto en Blindaje Patrimonial. Analiza a {nombre} ({edad} años).
        
        CONTEXTO FINANCIERO:
        - Ingreso Anual: ${ingreso_anual}
        - Ahorro Anual: ${ahorro_anual} ({pct_ahorro:.1f}%)
        - Deuda Anual: ${deuda_anual} (Nivel: {nivel_d})
        - Gastos RAG: Verde ${g_verde}, Amarillo ${g_amarillo}, Rojo ${g_rojo}.
        - Seguros: {', '.join(seguros_lista) if seguros_lista else 'Ninguno'}.

        INSTRUCCIONES OBLIGATORIAS:
        1. Explica que la salud financiera es estar 'blindado' para que un imprevisto no te rompa.
        2. Aplica la Regla 50-30-20. Si el ahorro es menor al 20%, advierte las consecuencias en la vejez.
        3. Clasificación RAG: Indica qué gastos ROJOS debe eliminar ya para invertirlos en su retiro.
        4. Alerta 'Metal vs Vida': Si tiene seguro de auto pero NO tiene PPR o Vida, dile: 'Aseguras el metal por si chocas (probabilidad), pero no tu vida por si llegas a viejo (certeza)'.
        5. Cita que en 2050 habrá 36 millones de adultos mayores y pregúntale: ¿De qué vas a vivir cuando dejes de trabajar?
        6. Usa un tono directo y profesional. Termina con: 'El segundo mejor momento para empezar es HOY'.
        """

        try:
            with st.spinner("Calculando tu blindaje..."):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                
                # Visualización rápida
                st.subheader("Resumen Visual")
                chart_data = pd.DataFrame({
                    "Concepto": ["Ahorro Real", "Meta Ahorro (20%)", "Deuda Actual"],
                    "Porcentaje": [pct_ahorro, 20, pct_deuda]
                })
                st.bar_chart(data=chart_data, x="Concepto", y="Porcentaje")
                
        except Exception as e:
            st.error(f"Error al conectar con la IA: {e}")

