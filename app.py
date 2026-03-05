import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Analizador de Blindaje Patrimonial", page_icon="🛡️")

# 2. Conexión Estable con la IA
try:
    # Asegúrate de que en tus Secrets de Streamlit la clave se llame exactamente: TU_API_KEY_AQUI
    genai.configure(api_key=st.secrets["TU_API_KEY_AQUI"])
    
    # Usamos gemini-1.5-flash porque es el más estable a nivel mundial
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Error de configuración. Revisa tus Secrets en Streamlit.")

# 3. Interfaz de usuario
st.title("🛡️ Analizador de Blindaje Patrimonial")
st.subheader("Por: Luis Alvarado")
st.write("Detecta tus fugas de dinero y protege tu futuro hoy mismo.")

# 4. Entradas de datos
st.divider()
edad = st.number_input("1. ¿Qué edad tienes?", min_value=18, max_value=75, value=30)
user_input = st.text_area("2. Pega tus movimientos o gastos del mes aquí:", 
                         placeholder="Ejemplo: Renta 8000, Despensa 4000, Netflix 200, Seguro de Auto 1200...")

# 5. El Corazón de la IA
if st.button("¡Generar mi Diagnóstico!"):
    if user_input:
        with st.spinner("Analizando tu blindaje..."):
            # Prompt optimizado para Luis Alvarado
            prompt = f"""
            Eres Luis Alvarado, experto en finanzas. El usuario tiene {edad} años. 
            Analiza estos datos: {user_input}

            Reporte solicitado:
            1. SEMÁFORO DE GASTOS: Clasifica en ROJOS (fugas), AMARILLOS (ajustables) y VERDES (vitales).
            2. EL COSTO DEL TIEMPO: Como tiene {edad} años, explícale cuánto pierde por esperar. 
               Usa el dato: a los 25 años juntas 11038000, pero a los 45 solo 1576000. 
               La diferencia son casi 9.5 millones de pesos.
            3. REALIDAD MÉXICO: Menciona que el 61% de los mexicanos dependen de otros al jubilarse.
            4. REGLA 50-30-20: Evalúa su salud financiera.
            5. EL METAL: Si hay seguros de auto, critica que asegure el metal pero no su vejez.
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                st.success("¡Diagnóstico terminado! Toma acción hoy.")
            except Exception as e:
                st.error(f"Lo siento, el sistema está saturado. Intenta en 1 minuto. (Detalle: {e})")
    else:
        st.warning("Por favor, escribe tus gastos para poder ayudarte.")

st.divider()
st.caption("© 2026 Luis Alvarado | Consultoría en Blindaje Patrimonial")
