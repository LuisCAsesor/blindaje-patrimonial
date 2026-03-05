import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Blindaje Patrimonial", layout="centered")

# 2. Obtener la API Key desde los "Secrets" de Streamlit
# Asegúrate de haberla guardado en el Dashboard de Streamlit como GOOGLE_API_KEY
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ No se encontró la API Key. Configúrala en los Secrets de Streamlit.")
    st.stop()

# 3. Configurar el SDK de Google
genai.configure(api_key=api_key)

# 4. Inicializar el modelo (Usando el nombre más estable para evitar el error 404)
try:
    # Usamos 'gemini-1.5-flash' que es rápido y eficiente para diagnósticos
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}")

# 5. Interfaz de la Aplicación
st.title("🛡️ Diagnóstico de Blindaje Patrimonial")
st.write("Bienvenido. Completa los datos para generar tu análisis.")

# Ejemplo de input para tu diagnóstico
user_input = st.text_area("Describe tu situación patrimonial actual:")

if st.button("¡Generar mi Diagnóstico!"):
    if user_input:
        with st.spinner("Analizando con IA..."):
            try:
                # Generar contenido
                response = model.generate_content(
                    f"Actúa como un experto en blindaje patrimonial. "
                    f"Analiza lo siguiente y da recomendaciones claras: {user_input}"
                )
                
                st.subheader("Tu Diagnóstico:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error("Hubo un problema con la conexión:")
                st.info(f"Detalle técnico: {e}")
                st.warning("Sugerencia: Revisa si tu API Key en AI Studio tiene cuota disponible.")
    else:
        st.warning("Por favor, ingresa alguna información para el análisis.")
