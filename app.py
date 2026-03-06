import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="IA Blindaje Patrimonial", page_icon="🛡️")

# --- CONEXIÓN ROBUSTA CON GEMINI ---
def get_model():
    try:
        api_key = st.secrets["API_KEY"]
        genai.configure(api_key=api_key)
        # Intentamos cimport streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. Configuración de la App
st.set_page_config(page_title="Blindaje Patrimonial IA", page_icon="🛡️")

# 2. Conexión a la IA con manejo de errores robusto
def inicializar_ia():
    try:
        if "API_KEY" not in st.secrets:
            st.error("Falta la API_KEY en Secrets.")
            return None
        genai.configure(api_key=st.secrets["API_KEY"])
        # Usamos Pro para máxima estabilidad y evitar el 404 del Flash
        return genai.GenerativeModel('gemini-1.5-pro')
    except Exception as e:
        st.error(f"Error de configuración: {e}")
        return None

model = inicializar_ia()

st.title("🛡️ Diagnóstico de Blindaje Patrimonial")
st.markdown("Analiza tu libertad financiera futura hoy mismo.")

# 3. Formulario de Datos
with st.form("main_form"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre Completo")
        edad = st.number_input("Edad", min_value=18, max_value=100, value=30)
    with col2:
        ingreso_anual = st.number_input("Ingreso Anual Total ($)", min_value=0)
    
    st.subheader("🚦 Semáforo de Gastos (Anual)")
    c1, c2, c3 = st.columns(3)
    with c1: g_verde = st.number_input("Verde (Necesario)", min_value=0)
    with c2: g_amarillo = st.number_input("Amarillo (Reducible)", min_value=0)
    with c3: g_rojo = st.number_input("Rojo (Eliminable)", min_value=0)
    
    st.subheader("💰 Ahorro y Deuda (Anual)")
    ahorro = st.number_input("¿Cuánto ahorras al año?", min_value=0)
    deuda = st.number_input("¿Cuánto pagas de deuda al año?", min_value=0)
    
    st.subheader("🛡️ Tus Seguros Actuales")
    s_auto = st.checkbox("Seguro de Auto")
    s_vida = st.checkbox("Seguro de Vida")
    s_retiro = st.checkbox("PPR / Retiro")
    
    enviar = st.form_submit_button("GENERAR DIAGNÓSTICO")

# 4. Procesamiento
if enviar:
    if not nombre or ingreso_anual <= 0:
        st.warning("Por favor completa los campos básicos.")
    elif model:
        # Lógica de Deuda [cite: 62]
        pct_deuda = (deuda / ingreso_anual) * 100
        nivel_d = "Controlada" if pct_deuda < 30 else "Alarma" if pct_deuda <= 60 else "Peligrosa" [cite: 60, 61, 62]
        pct_ahorro = (ahorro / ingreso_anual) * 100

        prompt = f"""
        Actúa como experto en Blindaje Patrimonial. Analiza a {nombre} ({edad} años).
        Ingreso: ${ingreso_anual}, Ahorro: {pct_ahorro:.1f}%, Deuda: {nivel_d} ({pct_deuda:.1f}%).
        Gastos RAG: Verde ${g_verde}, Amarillo ${g_amarillo}, Rojo ${g_rojo}.
        Seguros: Auto={s_auto}, Vida={s_vida}, Retiro={s_retiro}.

        REGLAS:
        - Menciona que en 2050 habrá 36 millones de adultos mayores[cite: 24, 25].
        - Si tiene seguro de auto pero no retiro/vida, dile: 'Aseguras el metal por si chocas, pero no tu vida por si llegas a viejo'[cite: 190, 191].
        - Usa la regla 50-30-20: el ahorro e inversión debe ser el 20%[cite: 63, 65].
        - El retiro es una certeza[cite: 191]. Termina con: 'El segundo mejor momento es hoy'.
        """

        try:
            with st.spinner("Generando análisis..."):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                
                # Gráfica Simple
                df = pd.DataFrame({
                    "Concepto": ["Ahorro Actual", "Meta (20%)", "Deuda"],
                    "Porcentaje": [pct_ahorro, 20, pct_deuda]
                })
                st.bar_chart(df.set_index("Concepto"))
        except Exception as e:
            st.error(f"Error de la IA: {e}. Revisa tu API Key.")on el modelo flash directo
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error de configuración: {e}")
        return None

model = get_model()

st.title("🛡️ Diagnóstico de Blindaje Patrimonial")
st.markdown("_El secreto para que tu estilo de vida nunca tenga fecha de caducidad._")

# --- FORMULARIO DE ENTRADA ---
with st.form("diagnostico_form"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre Completo")
        edad = st.number_input("Edad actual", min_value=18, max_value=100, value=30)
    with col2:
        ingreso_anual = st.number_input("Ingresos Totales Anuales ($)", min_value=0, step=1000)

    st.subheader("🚦 Tus Gastos Anuales (Estrategia RAG)")
    st.caption("Verde: Necesarios | Amarillo: Reducibles | Rojo: Eliminables")
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        g_verde = st.number_input("VERDE ($)", min_value=0)
    with col_g2:
        g_amarillo = st.number_input("AMARILLO ($)", min_value=0)
    with col_g3:
        g_rojo = st.number_input("ROJO ($)", min_value=0)

    st.subheader("💰 Ahorro y Deuda (Monto Anual)")
    col_ad1, col_ad2 = st.columns(2)
    with col_ad1:
        ahorro_anual = st.number_input("Ahorro/Inversión total al año", min_value=0)
    with col_ad2:
        deuda_anual = st.number_input("Pago de deudas total al año", min_value=0)

    st.subheader("🛡️ Tus Instrumentos Actuales")
    t_auto = st.checkbox("Seguro de Auto")
    t_vida = st.checkbox("Seguro de Vida")
    t_ppr = st.checkbox("PPR / Afore")
    
    seguros_lista = []
    if t_auto: seguros_lista.append("Seguro de Auto")
    if t_vida: seguros_lista.append("Seguro de Vida")
    if t_ppr: seguros_lista.append("PPR / Afore")

    enviar = st.form_submit_button("GENERAR DIAGNÓSTICO")

# --- LÓGICA DE PROCESAMIENTO ---
if enviar:
    if not nombre or ingreso_anual <= 0:
        st.warning("Por favor, completa tu nombre e ingresos anuales.")
    else:
        # 1. Análisis de Deuda (Basado en Página 7 del PDF)
        pct_deuda = (deuda_anual / ingreso_anual) * 100
        if pct_deuda < 30:
            nivel_d = "CONTROLADA (Menos del 30%)"
        elif 40 <= pct_deuda <= 60:
            nivel_d = "ALARMA (Entre 40% y 60%)"
        else:
            nivel_d = "PELIGROSA (Más del 60%)"

        # 2. Análisis de Ahorro (Basado en Regla 50-30-20 - Página 8)
        pct_ahorro = (ahorro_anual / ingreso_anual) * 100
        
        # 3. Prompt con Estrategia de Blindaje
        prompt = f"""
        Actúa como un experto en Blindaje Patrimonial. Analiza a {nombre} ({edad} años).
        
        CONTEXTO FINANCIERO:
        - Ingreso Anual: ${ingreso_anual}
        - Ahorro Anual: ${ahorro_anual} ({pct_ahorro:.1f}%)
        - Deuda Anual: ${deuda_anual} (Nivel: {nivel_d})
        - Gastos RAG: Verde ${g_verde}, Amarillo ${g_amarillo}, Rojo ${g_rojo}.
        - Seguros: {', '.join(seguros_lista) if seguros_lista else 'Ninguno'}.

        REGLAS DE NEGOCIO (ESTRICTO):
        1. Explica que la salud financiera es estar 'blindado' para que un imprevisto no te rompa.
        2. Aplica la Regla 50-30-20. Si el ahorro es menor al 20%, advierte las consecuencias.
        3. Clasificación RAG: Indica qué gastos ROJOS debe eliminar para invertirlos en su retiro.
        4. Alerta 'Metal vs Vida': Si tiene seguro de auto pero NO tiene PPR o Vida, dile: 'Aseguras el metal por si chocas (probabilidad), pero no tu vida por si llegas a viejo (certeza)'.
        5. Cita que en 2050 habrá 36 millones de adultos mayores en México. Pregunta: ¿De qué vas a vivir cuando dejes de trabajar?
        6. Usa un tono directo. Termina con: 'El segundo mejor momento para empezar es HOY'.
        """

        try:
            with st.spinner("Conectando con la IA..."):
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
                
                # Visualización
                st.subheader("Tu Semáforo Financiero")
                chart_data = pd.DataFrame({
                    "Concepto": ["Ahorro Real", "Meta Ahorro (20%)", "Pago Deuda"],
                    "Porcentaje": [pct_ahorro, 20, pct_deuda]
                })
                st.bar_chart(data=chart_data, x="Concepto", y="Porcentaje")
                
        except Exception as e:
            st.error("Error al generar el contenido. Intentando con modelo de respaldo...")
            try:
                # Intento de respaldo con modelo Pro si el Flash falla
                model_alt = genai.GenerativeModel('gemini-pro')
                response = model_alt.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e2:
                st.error(f"No se pudo conectar: {e2}")

