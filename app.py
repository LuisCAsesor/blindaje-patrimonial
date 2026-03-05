import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Analizador de Blindaje Patrimonial", page_icon="🛡️")

# 2. Conexión con la IA (Ajuste de nombre de modelo)
try:
    genai.configure(api_key=st.secrets["TU_API_KEY_AQUI"])
    # Usamos el nombre de modelo más compatible para evitar el error 404
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Error de configuración inicial. Revisa tu API Key en Secrets.")

# 3. Interfaz de la aplicación
st.title("🛡️ Analizador de Blindaje Patrimonial")
st.subheader("Por: Luis Alvarado")
st.write("Detecta fugas de dinero y asegura que tu retiro no dependa de la caridad.")

# 4. Entradas del usuario
st.info("Tu información es privada. La IA solo analiza los números para ayudarte.")
edad = st.number_input("1. ¿Qué edad tienes actualmente?", min_value=18, max_value=75, value=30)
user_input = st.text_area("2. Pega aquí tus gastos del mes o movimientos:", 
                         placeholder="Ejemplo: Renta 8000, Despensa 4000, Netflix 200, Seguro de Auto 1200...")

# 5. Botón de análisis
if st.button("Generar Diagnóstico"):
    if user_input:
        with st.spinner("Analizando tu Blindaje Patrimonial..."):
            prompt = f"""
            Eres Luis Alvarado, experto financiero. El usuario tiene {edad} años. 
            Analiza estos gastos: {user_input}

            Genera un reporte con:
            1. CLASIFICACIÓN RAG: Clasifica en ROJOS (fugas), AMARILLOS (ajustables) y VERDES (vitales).
            2. EL COSTO DEL TIEMPO: Como tiene {edad} años, explícale cuánto pierde por esperar. 
               Usa el dato: a los 25 años juntas $11,038,000, pero a los 45 solo $1,576,000.
               Dile cuántos millones está 'quemando' por cada año que no actúa.
            3. REALIDAD DEL RETIRO: Menciona que el 61% de los mexicanos dependen de otros al jubilarse.
            4. REGLA 50-30-20: Evalúa su salud financiera actual.
            5. EL METAL: Si hay seguros de auto, dile que asegura el metal pero no su vida.
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.success("¡Diagnóstico listo! El tiempo es dinero.")
            except Exception as e:
                st.error("El sistema está saturado. Intenta de nuevo en 30 segundos.")
    else:
        st.warning("Por favor, ingresa algunos datos para analizar.")

# Pie de página
st.markdown("---")
st.caption("© 2026 Luis Alvarado | Consultor Financiero")
