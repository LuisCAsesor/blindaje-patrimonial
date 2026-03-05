import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Analizador de Blindaje Patrimonial - Luis Alvarado", layout="centered")

# Título e Imagen de marca
st.title("🛡️ Analizador de Blindaje Patrimonial")
# Nuevo campo para que el cliente ponga su edad
edad = st.number_input("1. ¿Qué edad tienes actualmente?", min_value=18, max_value=75, value=30)

# El cuadro de texto que ya tenías (solo asegúrate de que esté debajo)
user_input = st.text_area("2. Copia y pega tus movimientos o describe tus gastos:")
st.subheader("Por: Luis Alvarado")
st.write("Optimiza tus gastos y asegura que tu estilo de vida nunca tenga fecha de caducidad.")

# Configurar la API de Gemini (Aquí pondrás tu llave)
genai.configure(api_key=st.secrets["TU_API_KEY_AQUI"])
model = genai.GenerativeModel('gemini-2.0-flash')

# Área de entrada de datos
st.info("Copia y pega los movimientos de tu estado de cuenta aquí abajo. Tu información es procesada de forma privada.")
data_input = st.text_area("Movimientos del mes:", height=200, placeholder="Ejemplo: 15/10 - Starbucks $95.00...")

if st.button("Generar Diagnóstico de Blindaje"):
    if data_input:
        with st.spinner("Analizando tus finanzas con la metodología de Luis Alvarado..."):
            # El "Prompt" con tu metodología
            prompt = f"""
prompt = f"""
Actúa como un experto en Blindaje Patrimonial. El usuario tiene {edad} años. 
Analiza los siguientes movimientos de su estado de cuenta: {user_input}

Instrucciones para tu reporte:
1. Clasifica los gastos en: Rojos (fugas de dinero), Amarillos (ajustables) y Verdes (vitales).
2. Explícale al usuario de {edad} años cuánto dinero está perdiendo por el factor tiempo. 
3. Usa la estadística: A los 25 años se pueden juntar $11,038,000, pero a los 45 solo $1,576,000. 
4. Recuérdale que el 61% de los mexicanos llegan a la vejez dependiendo de terceros si no aplican la regla 50-30-20.
5. Si ves un seguro de auto, dile que 'asegura el metal' pero no su libertad financiera.
"""
            Actúa como un experto en Blindaje Patrimonial siguiendo la metodología de Luis Alvarado.
            Analiza los siguientes gastos y genera un reporte estructurado:
            
            1. Clasificación RAG: Identifica gastos Rojos (eliminar), Amarillos (reducir) y Verdes (necesarios) [cite: 72-83].
            2. Evaluación 50-30-20: Revisa si los gastos cumplen con el tope de 30% en deudas y si hay un 20% para ahorro/retiro [cite: 63-66].
            3. Alerta de "Aseguramiento de lo Material": Si hay seguros de auto pero no de vida/retiro, menciónalo [cite: 190-192].
            4. Factor Tiempo: Explica cuánto dinero están perdiendo si no invierten esos excedentes hoy mismo[cite: 178].
            
            Gastos a analizar:
            {data_input}
            
            Responde de forma profesional, motivadora y directa.
            """
            
            response = model.generate_content(prompt)
            st.markdown("### 📊 Tu Diagnóstico Personalizado")
            st.write(response.text)
            
            st.success("¡Análisis completado! Si quieres profundizar en este diagnóstico, solicita una asesoría de 15 minutos con Luis.")
    else:

        st.warning("Por favor, ingresa algunos datos para poder ayudarte.")





