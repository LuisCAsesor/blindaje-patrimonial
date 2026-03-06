import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="IA Blindaje Patrimonial", page_icon="🛡️")

# --- CONEXIÓN CON GEMINI (Cuenta Gmail en Secrets) ---
# Recuerda configurar esto en Advanced Settings > Secrets de Streamlit Cloud
API_KEY = st.secrets["API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- ESTILOS ---
st.title("🛡️ Diagnóstico de Blindaje Patrimonial")
st.markdown("""
Esta herramienta analiza tu salud financiera actual y proyecta la seguridad de tu retiro.
*El secreto para que tu estilo de vida nunca tenga fecha de caducidad.*
""")

# --- SECCIÓN 1: DATOS PERSONALES ---
with st.expander("👤 1. Datos Personales", expanded=True):
    nombre = st.text_input("Nombre Completo")
    edad = st.number_input("Edad actual", min_value=18, max_value=100, value=30)
    ingreso_anual = st.number_input("Ingresos Totales Anuales ($)", min_value=0, step=1000)

# --- SECCIÓN 2: INSTRUMENTOS ---
with st.expander("📝 2. Tus Instrumentos Actuales"):
    st.write("Selecciona los seguros o herramientas de ahorro que ya tienes:")
    # Opciones basadas en el Blindaje Financiero (Página 11)
    t_auto = st.checkbox("Seguro de Auto")
    t_gastos_medicos = st.checkbox("Seguro de Gastos Médicos Mayores")
    t_vida = st.checkbox("Seguro de Vida")
    t_ppr = st.checkbox("Plan Personal de Retiro (PPR) / Afore")
    t_inversiones = st.checkbox("Inversiones (Cetes, Acciones, etc.)")
    
    seguros_lista = []
    if t_auto: seguros_lista.append("Seguro de Auto")
    if t_gastos_medicos: seguros_lista.append("Gastos Médicos")
    if t_vida: seguros_lista.append("Seguro de Vida")
    if t_ppr: seguros_lista.append("PPR/Afore")
    if t_inversiones: seguros_lista.append("Inversiones")

# --- SECCIÓN 3: GASTOS (ESTRATEGIA RAG) ---
with st.expander("🚦 3. Tus Gastos (Estrategia RAG)"):
    st.info("Clasifica tus gastos anuales aproximados:")
    g_verde = st.number_input("Gastos VERDE (Necesarios: Súper, Renta, Servicios)", min_value=0)
    g_amarillo = st.number_input("Gastos AMARILLO (Disminuibles: Restaurantes, Suscripciones)", min_value=0)
    g_rojo = st.number_input("Gastos ROJO (Eliminables: Starbucks, Compras impulsivas)", min_value=0)

# --- SECCIÓN 4: AHORRO Y DEUDA ---
with st.expander("💰 4. Ahorro y Deuda (Monto Anual)"):
    ahorro_anual = st.number_input("Monto total que ahorras/inviertes al AÑO ($)", min_value=0)
    deuda_anual = st.number_input("Monto total que pagas en DEUDAS al AÑO ($)", min_value=0)

# --- PROCESAMIENTO ---
if st.button("GENERAR DIAGNÓSTICO"):
    if ingreso_anual == 0:
        st.error("Por favor ingresa tus ingresos anuales.")
    else:
        # Lógica de Deuda (Página 7)
        pct_deuda = (deuda_anual / ingreso_anual) * 100
        if pct_deuda < 30:
            nivel_deuda = "CONTROLADA"
        elif 40 <= pct_deuda <= 60:
            nivel_deuda = "ALARMA"
        else:
            nivel_deuda = "PELIGROSA"

        # Lógica 50-30-20 (Página 8)
        pct_ahorro_real = (ahorro_anual / ingreso_anual) * 100
        gastos_totales = g_verde + g_amarillo + g_rojo
        
        # Gráfica comparativa
        st.subheader(f"Análisis para {nombre}")
        df_data = pd.DataFrame({
            "Categoría": ["Ahorro Actual", "Deuda Actual", "Gastos"],
            "Porcentaje": [pct_ahorro_real, pct_deuda, (gastos_totales/ingreso_anual)*100]
        })
        st.bar_chart(df_data.set_index("Categoría"))

        # --- LLAMADA A LA IA ---
        prompt = f"""
        Eres un experto en Blindaje Patrimonial. Analiza los datos de {nombre} ({edad} años):
        - Ingresos Anuales: ${ingreso_anual}
        - Ahorro Anual: ${ahorro_anual} ({pct_ahorro_real:.1f}%)
        - Deuda Anual: ${deuda_anual} ({pct_deuda:.1f}% - Nivel: {nivel_deuda})
        - Instrumentos: {', '.join(seguros_lista) if seguros_lista else 'Ninguno'}
        - Gastos: Verde ${g_verde}, Amarillo ${g_amarillo}, Rojo ${g_rojo}.

        Instrucciones Obligatorias (basadas en manual de entrenamiento):
        1. Evalúa si cumple la regla 50-30-20 (20% ahorro mínimo).
        2. Alerta Crítica: Si tiene 'Seguro de Auto' pero NO tiene 'PPR' o 'Seguro de Vida', dile que asegura el metal pero no su libertad ni su vejez.
        3. Clasificación RAG: Indica qué debe pasar de Rojo/Amarillo a Verde.
        4. Retiro: Menciona que en 2050 habrá 36 millones de adultos mayores y la mayoría dependerá de caridad o familia si no actúa hoy.
        5. Tono: Empático pero directo. Usa frases como 'El retiro es una certeza, el accidente una probabilidad'.
        """

        with st.spinner("La IA está calculando tu blindaje..."):
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
            
        st.success("¡Diagnóstico terminado! ¿Qué quieres que te diga tu 'Yo' dentro de 20 años: Gracias o ¿Por qué no lo hiciste?")
