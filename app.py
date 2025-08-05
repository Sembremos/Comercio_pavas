import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuración de la página ---
st.set_page_config(
    page_title="Encuesta de Seguridad en Pavas",
    page_icon="🚓",
    layout="wide"
)

# --- Estilos CSS para el título del expander ---
# Esto inyecta código CSS para cambiar el color, negrita y tamaño del título de cada expander.
st.markdown("""
<style>
.streamlit-expanderHeader p {
    font-size: 20px;
    color: #30a906;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- Encabezado de imagen y texto justificado ---
try:
    st.image("logo_pavas.png", width=300)
except FileNotFoundError:
    st.warning("Advertencia: El archivo 'logo_pavas.png' no se encontró. Asegúrate de que está en la misma carpeta que 'app.py'.")

st.title("🛡️ Encuesta sobre Seguridad para Comercios en Pavas")
st.markdown(
    """
    <div style="text-align: justify;">
    **Objetivo:** Recopilar información cualitativa sobre las dinámicas de asaltos y robos en las zonas comerciales de Pavas. Los datos son anónimos, confidenciales y serán utilizados exclusivamente para proponer mejoras en las estrategias de seguridad de la Fuerza Pública.
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()

# --- Diccionarios de opciones ---
opciones_tipo_negocio = [
    "Pulpería/Minisúper", "Farmacia", "Restaurante/Soda",
    "Salón de Belleza/Barbería", "Taller mecánico", "Tienda", "Otro"
]
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
opciones_frecuencia_patrullas = [
    "Varias veces al día", "Una vez al día",
    "Algunas veces por semana", "Casi nunca"
]
opciones_calificacion_respuesta = [
    "Excelente", "Bueno", "Regular", "Malo",
    "Nunca han llegado", "No he necesitado de la Fuerza Pública"
]
opciones_presencia_policial = ["Sí", "No", "Parcialmente"]

# --- Sección 1: Caracterización del Comercio (Desplegable) ---
with st.expander("Sección 1: Caracterización del Comercio", expanded=True):
    st.markdown("---")
    tipo_negocio = st.radio("1. Tipo de negocio:", options=opciones_tipo_negocio, horizontal=True)
    otro_negocio = ""
    if tipo_negocio == "Otro":
        otro_negocio = st.text_input("Por favor, especifique el tipo de negocio:")

    ubicacion = st.radio("2. Ubicación general dentro de Pavas:", options=opciones_ubicacion, horizontal=True)
    maneja_efectivo = st.radio("3. ¿Su negocio maneja montos significativos de efectivo de forma visible?", options=opciones_si_no_a_veces, horizontal=True)

# --- Sección 2: Experiencia Directa con Delitos (Desplegable) ---
with st.expander("Sección 2: Experiencia Directa con Delitos (Últimos 12 meses)"):
    st.markdown("---")
    victima_asalto = st.radio("4. ¿Ha sido usted o algún empleado víctima de un ASALTO en el local o sus inmediaciones?", options=opciones_si_no, horizontal=True)
    
    if victima_asalto == "Sí":
        st.markdown("5. Si fue víctima de un asalto, por favor describa el más reciente:")
        movilizacion = st.radio("  - ¿Cómo se movilizaban los delincuentes?", options=opciones_movilizacion, horizontal=True)
        uso_armas = st.radio("  - ¿Usaron armas?", options=opciones_si_no, horizontal=True)
        tipo_arma = ""
        if uso_armas == "Sí":
            tipo_arma = st.text_input("  - ¿Qué tipo de arma?")
        
        hora_asalto = st.text_input("  - ¿A qué hora aproximada ocurrió? (Ej: 14:30)")
        
        principales_robado = st.radio("  - ¿Qué se robaron principalmente?", options=opciones_principalmente_robado, horizontal=True)
        otras_pertenencias = ""
        if principales_robado == "Otras pertenencias de clientes":
            otras_pertenencias = st.text_input("  - Por favor, especifique qué otras pertenencias:")
        
        denuncia = st.radio("6. ¿Presentó la denuncia?", options=opciones_si_no, horizontal=True)
        razon_no_denuncia = ""
        if denuncia == "No":
            razon_no_denuncia = st.text_area("  - ¿Por qué no presentó la denuncia?")
            
    robo_vehiculos = st.radio("7. ¿Han robado vehículos o artículos DENTRO de vehículos (tacha) de clientes o empleados en el área cercana a su negocio?", options=opciones_si_no, horizontal=True)
    
    tipo_robo_vehiculo, facilita_robos = None, None
    if robo_vehiculos == "Sí":
        st.markdown("8. Sobre el robo a vehículos:")
        tipo_robo_vehiculo = st.radio("  - ¿Fue principalmente robo de todo el vehículo o tacha?", options=opciones_tipo_robo_vehiculo, horizontal=True)
        facilita_robos = st.text_area("  - ¿Qué cree que facilita estos robos en la zona? (Ej: Poca luz, calles solas, etc.)")

    problematica_extra = st.text_area("9. ¿Existe alguna otra problemática o delito que esté afectando a su comercio o clientes?")


# --- Sección 3: Percepción y Relación con Fuerza Pública (Desplegable) ---
with st.expander("Sección 3: Percepción y Relación con Fuerza Pública"):
    st.markdown("---")
    seguridad_local = st.radio("10. En una escala de 1 a 5, ¿qué tan seguro se siente en su local?", options=list(opciones_escala_seguridad.keys()), format_func=lambda x: opciones_escala_seguridad[x], horizontal=True)
    frecuencia_patrullas = st.radio("11. ¿Con qué frecuencia ve patrullas de Fuerza Pública en su calle?", options=opciones_frecuencia_patrullas, horizontal=True)
    tiempo_respuesta = st.radio("12. Si ha necesitado a la Fuerza Pública, ¿cómo califica su tiempo de respuesta?", options=opciones_calificacion_respuesta, horizontal=True)
    presencia_previene = st.radio("13. ¿Siente que la presencia policial actual logra prevenir el delito en esta área?", options=opciones_presencia_policial, horizontal=True)
    razon_parcial = ""
    if presencia_previene == "Parcialmente":
        razon_parcial = st.text_area("  - ¿Por qué?")


# --- Sección 4: Medidas de Prevención y Sugerencias (Desplegable) ---
with st.expander("Sección 4: Medidas de Prevención y Sugerencias"):
    st.markdown("---")
    medidas_seguridad = st.text_area("14. ¿Qué medidas de seguridad ha implementado usted en su negocio? (Ej: Alarmas, cámaras, rejas, etc.)")
    sugerencia_jefe_policia = st.text_area("15. Si usted pudiera darle una orden directa al jefe de la policía de Pavas, ¿cuál sería la acción MÁS URGENTE que le pediría para mejorar la seguridad de su negocio y la de sus clientes?")

st.divider()

# --- Botón de Envío y guardado de datos ---
if st.button("Enviar Encuesta"):
    datos_encuesta = {
        "timestamp": datetime.now(),
        "tipo_negocio": tipo_negocio,
        "otro_negocio_especificado": otro_negocio,
        "ubicacion": ubicacion,
        "maneja_efectivo": maneja_efectivo,
        "victima_asalto": victima_asalto,
        "movilizacion_delincuentes": locals().get('movilizacion'),
        "uso_armas": locals().get('uso_armas'),
        "tipo_arma_especificado": locals().get('tipo_arma'),
        "hora_asalto": locals().get('hora_asalto'),
        "principales_robado": locals().get('principales_robado'),
        "otras_pertenencias_especificadas": locals().get('otras_pertenencias'),
        "denuncia_presentada": locals().get('denuncia'),
        "razon_no_denuncia": locals().get('razon_no_denuncia'),
        "robo_vehiculos_cerca": robo_vehiculos,
        "tipo_robo_vehiculo": locals().get('tipo_robo_vehiculo'),
        "facilita_robos": locals().get('facilita_robos'),
        "problematica_extra": problematica_extra,
        "sentimiento_seguridad": seguridad_local,
        "frecuencia_patrullas": frecuencia_patrullas,
        "tiempo_respuesta": tiempo_respuesta,
        "presencia_previene": presencia_previene,
        "razon_parcial": locals().get('razon_parcial'),
        "medidas_seguridad": medidas_seguridad,
        "sugerencia_jefe_policia": sugerencia_jefe_policia,
    }
    
    try:
        df = pd.DataFrame([datos_encuesta])
        
        file_path = "datos_encuesta.csv"
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            df.to_csv(file_path, index=False, encoding="utf-8-sig")
        else:
            df.to_csv(file_path, mode="a", header=False, index=False, encoding="utf-8-sig")

        st.success("🎉 ¡Gracias por completar la encuesta! Tus respuestas han sido enviadas.")
    except Exception as e:
        st.error(f"Ocurrió un error al guardar los datos: {e}")
