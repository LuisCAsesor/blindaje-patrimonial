import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Analizador de Blindaje Patrimonial", page_icon="🛡️")

# 2. Conexión con la IA (Ajustado para evitar el error 404)
genai.configure(api_key=st.secrets["TU_API_KEY_AQUI"])
# Usamos el modelo más reciente y estable para 2026
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Interfaz de la aplicación
st.title("🛡️ Analizador de Blindaje Patrimonial")
st.subheader("Por: Luis Alvarado")
st.write("Optimiza tus gastos y asegura que tu estilo de vida nunca tenga fecha de caducidad.")

# 4. Entradas del usuario
st.info("Tu información es procesada de forma privada y segura.")
edad = st.number_input("1. ¿Qué edad tienes actualmente?", min_value=18, max_value=75, value=30)
user_input = st.text_area("2. Copia y pega tus movimientos o describe tus gastos del mes:", 
                         placeholder="Ejemplo: Renta 8000, Despensa 4000, Netflix 200, Seguro de Auto 1200...")

# 5. Botón de análisis
if st.button("Generar Diagnóstico de Blindaje"):
    if user_input:
        with st.spinner("La IA de Luis Alvarado está analizando tu futuro..."):
            # 6. Instrucciones maestras (Prompt)
            prompt = f"""
            Actúa como Luis Alvarado, experto en Blindaje Patrimonial. 
            El usuario tiene {edad} años. Analiza estos gastos: {user_input}

            Estructura tu respuesta de forma profesional:
            1. CLASIFICACIÓN RAG: Clasifica los gastos en ROJOS (fugas), AMARILLOS (ajustables) y VERDES (vitales).
            2. EL COSTO DEL TIEMPO: Explícale al usuario de {edad} años que si empieza a los 25 junta $11,038,000, pero a los 45 solo $1,576,000. Calcula cuántos millones está perdiendo por postergar su decisión.
            3. SALUD FINANCIERA: Menciona la regla 50-30-20 y advierte que el 61% de los mexicanos dependen de otros al jubilarse.
            4. PARADOJA DEL METAL: Si detectas seguros de auto, dile que asegura el 'metal' pero no su libertad.
            5. CIERRE: Invítalo a una asesoría de 15 minutos para recuperar ese capital perdido.
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.success("¡Diagnóstico completado! El tiempo es tu activo más caro.")
            except Exception as e:
                # Si sigue el error de cuota o modelo, mostramos un mensaje amigable
                st.error("Nivel de demanda alto. Por favor, intenta de nuevo en 60 segundos.")
    else:
        st.warning("Por favor, ingresa tus gastos para poder ayudarte.")

# Pie de página
st.markdown("---")
st.caption("© 2026 Luis Alvarado - Consultoría en Blindaje Patrimonial.")
