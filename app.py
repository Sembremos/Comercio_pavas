import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

# --- Configuración de la página ---
st.set_page_config(
    page_title="Encuesta de Seguridad en Pavas",
    page_icon="🚓",
    layout="wide"
)

# --- Estilos CSS personalizados para el título del expander ---
st.markdown("""
<style>
/* Estilo para el título del expander */
div.st-emotion-cache-1ft84e1 p {
    font-size: 20px;
    color: #30a906;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- Encabezado de imagen y texto justificado ---
try:
    # Asegúrate de que el archivo 'logo_pavas.png' esté en tu repositorio de GitHub
    st.image("logo_pavas.png", width=700)
except FileNotFoundError:
    st.warning("Advertencia: El archivo 'logo_pavas.png' no se encontró. Asegúrate de que está en la misma carpeta que 'app.py'.")

st.title("🛡️ Encuesta sobre Seguridad para Comercios en Pavas")
st.markdown(
    """
    <div style="text-align: justify;">
    El objetivo de esta encuesta es recopilar información cualitativa sobre las dinámicas de asaltos y robos en las zonas comerciales de Pavas. Los datos son anónimos, confidenciales y serán utilizados exclusivamente para proponer mejoras en las estrategias de seguridad de la Fuerza Pública.
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()

# --- Diccionarios de opciones ---
opciones_tipo_negocio = ["Pulpería/Minisúper", "Farmacia", "Restaurante/Soda",
                        "Salón de Belleza/Barbería", "Taller mecánico", "Tienda", "Otro"]
opciones_ubicacion = ["Circuito 1", "Circuito 2", "Circuito 3", "Circuito 4"]
opciones_si_no_a_veces = ["Sí", "No", "A veces"]
opciones_si_no = ["Sí", "No"]
opciones_movilizacion = ["A pie", "Motocicleta", "Carro"]
opciones_principalmente_robado = ["Efectivo", "Celulares", "Otras pertenencias de clientes"]
opciones_tipo_robo_vehiculo = ["Robo de vehículo", "Tacha"]
opciones_escala_seguridad = {
    1: "1 - Muy Inseguro", 2: "2 - Inseguro", 3: "3 - Neutral",
    4: "4 - Seguro", 5: "5 - Muy Seguro"
}
opciones_frecuencia_patrullas = ["Varias veces al día", "Una vez al día",
                                "Algunas veces por semana", "Casi nunca"]
opciones_calificacion_respuesta = ["Excelente", "Bueno", "Regular", "Malo",
                                   "Nunca han llegado", "No he necesitado de la Fuerza Pública"]
opciones_presencia_policial = ["Sí", "No", "Parcialmente"]

# --- Función para guardar los datos en Google Sheets de forma segura ---
def save_to_gsheet(data):
    try:
        # CONVERSIÓN CRUCIAL: Lee el secreto como un string y lo convierte a JSON
        creds_json_string = st.secrets["gcp_credentials"]
        creds_json = json.loads(creds_json_string)
        creds = ServiceAccountCredentials.from_json(creds_json)
        
        # Define los permisos (scope) y autoriza el cliente de gspread
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        client = gspread.authorize(creds.create_delegated(scope))
        
        # Abre la hoja de cálculo por su ID y nombre de la hoja
        sheet_id = "1HtNM0amp35MF2jrxXLdClhFrABpfC_ofaT00Am2lJK8"
        sheet = client.open_by_key(sheet_id).worksheet("Hoja 1")
        
        # Agrega una nueva fila con los datos de la encuesta
        sheet.append_row(data)
        
        return True
    except Exception as e:
        st.error(f"Ocurrió un error al guardar en Google Sheets: {e}")
        return False

# --- Lógica del formulario ---
st.header("Completa la Encuesta Anónima")
with st.form("encuesta_seguridad"):
    
    # Sección 1: Caracterización del Comercio
    with st.expander("Sección 1: Caracterización del Comercio", expanded=True):
        st.markdown("---")
        tipo_negocio = st.radio("1. Tipo de negocio:", options=opciones_tipo_negocio, horizontal=True, key="q1_tipo_negocio")
        otro_negocio = ""
        if tipo_negocio == "Otro":
            otro_negocio = st.text_input("Por favor, especifique el tipo de negocio:", key="q1_otro_negocio")

        ubicacion = st.radio("2. Ubicación general dentro de Pavas:", options=opciones_ubicacion, horizontal=True, key="q2_ubicacion")
        maneja_efectivo = st.radio("3. ¿Su negocio maneja montos significativos de efectivo de forma visible?", options=opciones_si_no_a_veces, horizontal=True, key="q3_maneja_efectivo")

    # Sección 2: Experiencia Directa con Delitos
    with st.expander("Sección 2: Experiencia Directa con Delitos (Últimos 12 meses)"):
        st.markdown("---")
        victima_asalto = st.radio("4. ¿Ha sido usted o algún empleado víctima de un ASALTO en el local o sus inmediaciones?", options=opciones_si_no, horizontal=True, key="q4_victima_asalto")
        
        movilizacion, uso_armas, tipo_arma, hora_asalto, principales_robado, otras_pertenencias, denuncia, razon_no_denuncia = [None] * 8
        if victima_asalto == "Sí":
            st.markdown("5. Si fue víctima de un asalto, por favor describa el más reciente:")
            movilizacion = st.radio("  - ¿Cómo se movilizaban los delincuentes?", options=opciones_movilizacion, horizontal=True, key="q5_movilizacion")
            uso_armas = st.radio("  - ¿Usaron armas?", options=opciones_si_no, horizontal=True, key="q5_uso_armas")
            tipo_arma = ""
            if uso_armas == "Sí":
                tipo_arma = st.text_input("  - ¿Qué tipo de arma?", key="q5_tipo_arma")
            
            hora_asalto = st.text_input("  - ¿A qué hora aproximada ocurrió? (Ej: 14:30)", key="q5_hora_asalto")
            principales_robado = st.radio("  - ¿Qué se robaron principalmente?", options=opciones_principalmente_robado, horizontal=True, key="q5_principalmente_robado")
            otras_pertenencias = ""
            if principales_robado == "Otras pertenencias de clientes":
                otras_pertenencias = st.text_input("  - Por favor, especifique qué otras pertenencias:", key="q5_otras_pertenencias")
            
            denuncia = st.radio("6. ¿Presentó la denuncia?", options=opciones_si_no, horizontal=True, key="q6_denuncia")
            razon_no_denuncia = ""
            if denuncia == "No":
                razon_no_denuncia = st.text_area("  - ¿Por qué no presentó la denuncia?", key="q6_razon_no_denuncia")
                
        robo_vehiculos = st.radio("7. ¿Han robado vehículos o artículos DENTRO de vehículos (tacha) de clientes o empleados en el área cercana a su negocio?", options=opciones_si_no, horizontal=True, key="q7_robo_vehiculos")
        
        tipo_robo_vehiculo, facilita_robos = None, None
        if robo_vehiculos == "Sí":
            st.markdown("8. Sobre el robo a vehículos:")
            tipo_robo_vehiculo = st.radio("  - ¿Fue principalmente robo de todo el vehículo o tacha?", options=opciones_tipo_robo_vehiculo, horizontal=True, key="q8_tipo_robo_vehiculo")
            facilita_robos = st.text_area("  - ¿Qué cree que facilita estos robos en la zona? (Ej: Poca luz, calles solas, etc.)", key="q8_facilita_robos")

        problematica_extra = st.text_area("9. ¿Existe alguna otra problemática o delito que esté afectando a su comercio o clientes?", key="q9_problematica_extra")


    # Sección 3: Percepción y Relación con Fuerza Pública
    with st.expander("Sección 3: Percepción y Relación con Fuerza Pública"):
        st.markdown("---")
        seguridad_local = st.radio("10. En una escala de 1 a 5, ¿qué tan seguro se siente en su local?", options=list(opciones_escala_seguridad.keys()), format_func=lambda x: opciones_escala_seguridad[x], horizontal=True, key="q10_seguridad_local")
        frecuencia_patrullas = st.radio("11. ¿Con qué frecuencia ve patrullas de Fuerza Pública en su calle?", options=opciones_frecuencia_patrullas, horizontal=True, key="q11_frecuencia_patrullas")
        tiempo_respuesta = st.radio("12. Si ha necesitado a la Fuerza Pública, ¿cómo califica su tiempo de respuesta?", options=opciones_calificacion_respuesta, horizontal=True, key="q12_tiempo_respuesta")
        presencia_previene = st.radio("13. ¿Siente que la presencia policial actual logra prevenir el delito en esta área?", options=opciones_presencia_policial, horizontal=True, key="q13_presencia_previene")
        razon_parcial = ""
        if presencia_previene == "Parcialmente":
            razon_parcial = st.text_area("  - ¿Por qué siente que la presencia es solo parcial o no del todo efectiva?", key="q13_razon_parcial")

        sugerencias = st.text_area("14. Si tuviera alguna sugerencia para la Fuerza Pública, ¿cuál sería?", key="q14_sugerencias")

    # Botón de envío
    submitted = st.form_submit_button("Enviar Encuesta")
    
    if submitted:
        # Recopila los datos del formulario
        data = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            otro_negocio if tipo_negocio == "Otro" else tipo_negocio,
            ubicacion,
            maneja_efectivo,
            victima_asalto,
            movilizacion,
            uso_armas,
            tipo_arma,
            hora_asalto,
            principales_robado,
            otras_pertenencias,
            denuncia,
            razon_no_denuncia,
            robo_vehiculos,
            tipo_robo_vehiculo,
            facilita_robos,
            problematica_extra,
            opciones_escala_seguridad[seguridad_local],
            frecuencia_patrullas,
            tiempo_respuesta,
            presencia_previene,
            razon_parcial,
            sugerencias
        ]

        if save_to_gsheet(data):
            st.success("¡Gracias! Tu encuesta ha sido guardada correctamente.")
        else:
            st.error("Hubo un error al enviar la encuesta. Por favor, inténtalo de nuevo más tarde.")
