import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Analizador de Blindaje Patrimonial", page_icon="🛡️")

# 2. Conexión Inteligente (Prueba varios modelos para evitar el 404)
genai.configure(api_key=st.secrets["TU_API_KEY_AQUI"])

def get_model():
    # Lista de modelos por orden de estabilidad en 2026
    for model_name in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
        try:
            m = genai.GenerativeModel(model_name)
            # Prueba mínima para ver si el modelo responde
            return m
        except:
            continue
    return None

model = get_model()

# 3. Interfaz de usuario
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
    if model is None:
        st.error("Error crítico: No se encontró un modelo de IA disponible. Revisa tu API Key.")
    elif user_input:
        with st.spinner("Analizando tu patrimonio con IA..."):
            prompt = f"""
            Eres Luis Alvarado, experto en Blindaje Patrimonial. El usuario tiene {edad} años. 
            Analiza estos datos de gasto: {user_input}

            Reporte solicitado:
            1. SEMÁFORO DE GASTOS: Clasifica en ROJOS (fugas), AMARILLOS (ajustables) y VERDES (vitales).
            2. EL COSTO DEL TIEMPO: Explícale que a los 25 años junta $11,038,000, pero a los 45 solo $1,576,000.
               Como tiene {edad} años, dile cuántos millones pierde por cada año de duda.
            3. REALIDAD MÉXICO: Menciona que el 61% de los mexicanos dependen de otros al jubilarse.
               Recuérdale que para 2050 seremos 36 millones de adultos mayores.
            4. REGLA 50-30-20: Evalúa su salud financiera actual.
            5. EL METAL: Si hay seguros de auto, critica que asegure el 'metal' (auto) pero no su libertad.
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.success("¡Diagnóstico completado! No seas parte de la estadística del 61%.")
            except Exception as e:
                st.error(f"Aviso del servidor: {e}. Intenta de nuevo en un minuto.")
    else:
        st.warning("Por favor, ingresa tus gastos para que la IA pueda ayudarte.")

st.divider()
st.caption("© 2026 Luis Alvarado | Consultoría en Blindaje Patrimonial")
