import streamlit as st
import google.generativeai as genai

# 1. Configuración profesional de la página
st.set_page_config(page_title="Analizador de Blindaje Patrimonial", page_icon="🛡️")

# 2. Conexión con la IA (Modelo Gemini 3 Flash - Actualizado 2026)
try:
    genai.configure(api_key=st.secrets["TU_API_KEY_AQUI"])
    # Nombre oficial del modelo para el Paid Tier en 2026
    model = genai.GenerativeModel('gemini-3-flash')
except Exception as e:
    st.error("Error en la llave de acceso. Revisa tus Secrets en Streamlit.")

# 3. Interfaz de usuario
st.title("🛡️ Analizador de Blindaje Patrimonial")
st.subheader("Por: Luis Alvarado")
st.write("No permitas que tu retiro dependa de la caridad. Identifica tus fugas hoy.")

# 4. Entradas de datos
st.divider()
edad = st.number_input("1. ¿Qué edad tienes actualmente?", min_value=18, max_value=75, value=30)
user_input = st.text_area("2. Pega aquí tus gastos mensuales o movimientos:", 
                         placeholder="Ejemplo: Renta 8000, Despensa 4000, Netflix 200, Seguro de Auto 1200...")

# 5. Lógica del Diagnóstico
if st.button("Generar Diagnóstico de Blindaje"):
    if user_input:
        with st.spinner("Gemini 3 está analizando tu futuro financiero..."):
            prompt = f"""
            Eres Luis Alvarado, experto en Blindaje Patrimonial. El usuario tiene {edad} años. 
            Analiza estos datos: {user_input}

            Genera un reporte de alto impacto con esta estructura:
            1. DIAGNÓSTICO RAG: Clasifica en ROJOS (fugas), AMARILLOS (ajustables) y VERDES (vitales).
            2. EL GOLPE DE REALIDAD ($9.4M): Como tiene {edad} años, calcula cuánto está perdiendo por cada año de indecisión. 
               Usa el dato: a los 25 años se juntan $11,038,000, pero a los 45 solo $1,576,000.
               Dile cuántos millones está 'quemando' literalmente por no empezar hoy.
            3. ESTADÍSTICA DE SUPERVIVENCIA: Menciona que el 61% de los mexicanos dependen de otros al jubilarse.
            4. REGLA 50-30-20: Evalúa su salud financiera según este estándar.
            5. EL METAL VS LA LIBERTAD: Si hay seguros de auto, critica que asegure el 'metal' pero no su vejez.
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.success("¡Análisis completado! El tiempo es tu activo más caro.")
            except Exception as e:
                # Mostramos el error real para poder ayudarte mejor
                st.error(f"Error del sistema: {e}. Intenta de nuevo en 60 segundos.")
    else:
        st.warning("Por favor, ingresa tus datos para generar el diagnóstico.")

st.divider()
st.caption("© 2026 Luis Alvarado | Consultoría en Blindaje Patrimonial")
