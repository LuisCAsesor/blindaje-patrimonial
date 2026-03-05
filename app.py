import streamlit as st
import google.generativeai as genai

# 1. Configuración de la interfaz
st.set_page_config(page_title="Analizador de Blindaje Patrimonial", page_icon="🛡️")

# 2. Conexión con la IA (Ajuste de compatibilidad total)
try:
    genai.configure(api_key=st.secrets["TU_API_KEY_AQUI"])
    # Cambiamos a 'gemini-1.5-flash-latest' para forzar la conexión más estable
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error("Error de configuración: Revisa tu API Key en los Secrets de Streamlit.")

# 3. Interfaz Visual
st.title("🛡️ Analizador de Blindaje Patrimonial")
st.subheader("Por: Luis Alvarado")
st.write("Detecta tus fugas de dinero y protege tu futuro hoy mismo.")

# 4. Entradas de datos
st.divider()
edad = st.number_input("1. ¿Qué edad tienes actualmente?", min_value=18, max_value=75, value=30)
user_input = st.text_area("2. Pega aquí tus gastos mensuales o movimientos:", 
                         placeholder="Ejemplo: Renta 8000, Despensa 4000, Netflix 200, Seguro de Auto 1200...")

# 5. Generación del Diagnóstico
if st.button("¡Generar mi Diagnóstico!"):
    if user_input:
        with st.spinner("Analizando tu patrimonio con IA..."):
            # Prompt optimizado con toda tu metodología
            prompt = f"""
            Eres Luis Alvarado, experto en Blindaje Patrimonial. El usuario tiene {edad} años. 
            Analiza estos datos de gasto: {user_input}

            Genera un reporte con este ADN:
            1. SEMÁFORO DE GASTOS: Clasifica en ROJOS (fugas), AMARILLOS (ajustables) y VERDES (vitales).
            2. EL COSTO DEL TIEMPO: Explícale al usuario de {edad} años que si empieza a los 25 junta $11,038,000, pero a los 45 solo $1,576,000.
               Dile cuántos millones está perdiendo por cada año que posterga su blindaje.
            3. REALIDAD MÉXICO: Menciona que el 61% de los mexicanos dependen de otros al jubilarse.
            4. REGLA 50-30-20: Evalúa su salud financiera actual.
            5. EL METAL: Si hay seguros de auto, critica que asegure el 'metal' (auto) pero no su propia libertad financiera.
            """
            
            try:
                # El método generate_content es el estándar de oro
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.success("¡Diagnóstico completado! El tiempo es tu activo más valioso.")
            except Exception as e:
                # Si el error persiste, este mensaje nos dirá por qué exactamente
                st.error(f"Aviso del servidor: {e}. Por favor, intenta de nuevo en un minuto.")
    else:
        st.warning("Por favor, ingresa tus gastos para que la IA pueda ayudarte.")

st.divider()
st.caption("© 2026 Luis Alvarado | Consultoría en Blindaje Patrimonial")
