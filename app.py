import streamlit as st
import requests

# 1. Configuración de Estilo y Página
st.set_page_config(page_title="Blindaje Patrimonial", page_icon="🛡️")
st.title("🛡️ Diagnóstico de Blindaje Patrimonial")

# 2. Credenciales (Asegúrate de que el nombre coincida en tu Dashboard de Streamlit)
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. Interfaz de Usuario
col1, col2 = st.columns(2)
with col1:
    edad = st.number_input("Tu edad actual:", min_value=18, max_value=100, value=37)
with col2:
    monto_ahorro = st.number_input("Dinero en efectivo/ahorro (USD):", min_value=0, value=1000)

activos = st.text_area("Describe otros activos (casa, negocio, bienes, etc.):", 
                       placeholder="Ej: Casa 100k, Negocio de ropa, 2 autos...")

if st.button("¡Generar mi Diagnóstico!"):
    if not API_KEY:
        st.error("❌ Error: No se encontró la API Key en los Secrets de Streamlit.")
    else:
        # URL de la versión 1 (ESTABLE), no la v1beta que te da el error 404
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        
        headers = {'Content-Type': 'application/json'}
        
        # El Prompt con la lógica que pediste (Edad + Pérdida de dinero)
        prompt_text = (
            f"Eres un experto en blindaje patrimonial. El cliente tiene {edad} años. "
            f"Tiene {monto_ahorro} USD en efectivo y estos activos: {activos}. "
            f"1. Calcula cuánto poder adquisitivo ha perdido su efectivo en los últimos 5 años por inflación (aprox 20% total). "
            f"2. Explica el riesgo patrimonial según su edad de {edad} años. "
            f"3. Da 3 pasos urgentes para blindar este patrimonio."
        )

        payload = {
            "contents": [{"parts": [{"text": prompt_text}]}]
        }

        with st.spinner("Calculando impacto financiero..."):
            try:
                response = requests.post(url, headers=headers, json=payload)
                response_data = response.json()
                
                # Extraemos la respuesta de la IA
                if "candidates" in response_data:
                    texto_ia = response_data["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("✅ Diagnóstico Generado")
                    st.markdown("---")
                    st.markdown(texto_ia)
                else:
                    # Si Google responde con otro error, lo mostramos aquí
                    st.error("Error en la respuesta de Google")
                    st.json(response_data)
                    
            except Exception as e:
                st.error(f"Fallo de conexión: {str(e)}")
