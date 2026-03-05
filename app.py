import streamlit as st
import google.generativeai as genai
import os

# 1. Configuración de la página
st.set_page_config(page_title="Analizador de Blindaje", page_icon="🛡️")

# 2. Inicialización Blindada
try:
    # Forzamos la configuración limpia
    api_key = st.secrets["TU_API_KEY_AQUI"]
    genai.configure(api_key=api_key)
    
    # Usamos el nombre del modelo sin prefijos para mayor compatibilidad
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")

# 3. Interfaz
st.title("🛡️ Analizador de Blindaje Patrimonial")
st.subheader("Por: Luis Alvarado")
st.write("Tu herramienta para no ser parte del 61% que depende de otros al jubilarse.")

# 4. Entradas
edad = st.number_input("¿Qué edad tienes?", min_value=18, max_value=75, value=30)
user_input = st.text_area("Pega tus gastos o movimientos aquí:")

# 5. Ejecución con manejo de errores mejorado
if st.button("¡Generar mi Diagnóstico!"):
    if user_input:
        with st.spinner("Conectando con la IA de Blindaje..."):
            try:
                # Instrucciones precisas de la metodología Luis Alvarado
                prompt = f"""
                Eres Luis Alvarado, experto financiero. El usuario tiene {edad} años. 
                Analiza estos gastos: {user_input}
                
                1. SEMÁFORO RAG: Clasifica en ROJOS (fugas), AMARILLOS (ajustables) y VERDES (vitales).
                2. COSTO DEL TIEMPO: Explícale cuánto pierde por esperar (25 años vs 45 años = $9.4 millones de diferencia).
                3. REGLA 50-30-20: Evalúa su salud financiera actual.
                4. EL METAL: Si hay seguros de auto, dile que asegura el metal pero no su libertad.
                5. RETIRO: Menciona que el 61% de los mexicanos dependen de otros al jubilarse.
                """
                
                response = model.generate_content(prompt)
                st.markdown("---")
                st.write(response.text)
                
            except Exception as e:
                # Si el error 404 persiste, intentamos una ruta alternativa automáticamente
                st.warning("Reintentando conexión por vía alterna...")
                try:
                    alt_model = genai.GenerativeModel('gemini-1.5-pro')
                    response = alt_model.generate_content(prompt)
                    st.write(response.text)
                except:
                    st.error(f"Error de conexión con Google: {e}")
                    st.info("Sugerencia: Genera una NUEVA API Key en Google AI Studio, a veces las llaves se 'ciclan'.")



