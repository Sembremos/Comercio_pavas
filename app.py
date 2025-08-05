import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuración de la página ---
st.set_page_config(
    page_title="Encuesta de Seguridad en Pavas",
    page_icon="🚓",
    layout="wide"
)

# --- Encabezado de imagen ---
st.image("logo_pavas.png", width=700)

# --- Título y descripción de la encuesta ---
st.title("Encuesta sobre Seguridad para Comercios en Pavas")
st.markdown("""
**El Objetivo de esta encuesta es recopilar información cualitativa sobre las dinámicas de asaltos y robos en las zonas comerciales de Pavas. Los datos son anónimos, confidenciales y serán utilizados exclusivamente para proponer mejoras en las estrategias de seguridad de la Fuerza Pública.
""")
st.divider()

# --- Diccionarios de opciones para las preguntas de selección múltiple ---
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


# --- Sección 1: Caracterización del Comercio ---
st.header("Sección 1: Caracterización del Comercio")
st.markdown("---")

tipo_negocio = st.radio("1. Tipo de negocio:", options=opciones_tipo_negocio, horizontal=True)
if tipo_negocio == "Otro":
    otro_negocio = st.text_input("Por favor, especifique el tipo de negocio:")
else:
    otro_negocio = ""

ubicacion = st.radio("2. Ubicación general dentro de Pavas:", options=opciones_ubicacion, horizontal=True)
maneja_efectivo = st.radio("3. ¿Su negocio maneja montos significativos de efectivo de forma visible?", options=opciones_si_no_a_veces, horizontal=True)
st.divider()


# --- Sección 2: Experiencia Directa con Delitos ---
st.header("Sección 2: Experiencia Directa con Delitos (Últimos 12 meses)")
st.markdown("---")

# Pregunta 4
victima_asalto = st.radio("4. ¿Ha sido usted o algún empleado víctima de un ASALTO en el local o sus inmediaciones?", options=opciones_si_no, horizontal=True)

# Lógica condicional para las preguntas 5 y 6
if victima_asalto == "Sí":
    st.markdown("5. Si fue víctima de un asalto, por favor describa el más reciente:")
    movilizacion = st.radio("  - ¿Cómo se movilizaban los delincuentes?", options=opciones_movilizacion, horizontal=True)
    
    uso_armas = st.radio("  - ¿Usaron armas?", options=opciones_si_no, horizontal=True)
    tipo_arma = ""
    if uso_armas == "Sí":
        tipo_arma = st.text_input("  - ¿Qué tipo de arma?")
    
    hora_asalto = st.text_input("  - ¿A qué hora aproximada ocurrió? (Ej: 14:30)")
    
    principales_robado = st.radio("  - ¿Qué se robaron principalmente?", options=opciones_principalmente_robado, horizontal=True)
    if principales_robado == "Otras pertenencias de clientes":
        otras_pertenencias = st.text_input("  - Por favor, especifique qué otras pertenencias:")
    else:
        otras_pertenencias = ""
    
    denuncia = st.radio("6. ¿Presentó la denuncia?", options=opciones_si_no, horizontal=True)
    razon_no_denuncia = ""
    if denuncia == "No":
        razon_no_denuncia = st.text_area("  - ¿Por qué no presentó la denuncia?")

# Pregunta 7
robo_vehiculos = st.radio("7. ¿Han robado vehículos o artículos DENTRO de vehículos (tacha) de clientes o empleados en el área cercana a su negocio?", options=opciones_si_no, horizontal=True)

# Lógica condicional para las preguntas 8 y 9
if robo_vehiculos == "Sí":
    st.markdown("8. Sobre el robo a vehículos:")
    tipo_robo_vehiculo = st.radio("  - ¿Fue principalmente robo de todo el vehículo o tacha?", options=opciones_tipo_robo_vehiculo, horizontal=True)
    
    facilita_robos = st.text_area("  - ¿Qué cree que facilita estos robos en la zona? (Ej: Poca luz, calles solas, etc.)")

# Pregunta 9
problematica_extra = st.text_area("9. ¿Existe alguna otra problemática o delito que esté afectando a su comercio o clientes?")
st.divider()


# --- Sección 3: Percepción y Relación con Fuerza Pública ---
st.header("Sección 3: Percepción y Relación con Fuerza Pública")
st.markdown("---")

# Pregunta 10
seguridad_local = st.radio("10. En una escala de 1 a 5, ¿qué tan seguro se siente en su local?", options=list(opciones_escala_seguridad.keys()), format_func=lambda x: opciones_escala_seguridad[x], horizontal=True)

# Pregunta 11
frecuencia_patrullas = st.radio("11. ¿Con qué frecuencia ve patrullas de Fuerza Pública en su calle?", options=opciones_frecuencia_patrullas, horizontal=True)

# Pregunta 12
tiempo_respuesta = st.radio("12. Si ha necesitado a la Fuerza Pública, ¿cómo califica su tiempo de respuesta?", options=opciones_calificacion_respuesta, horizontal=True)

# Pregunta 13
presencia_previene = st.radio("13. ¿Siente que la presencia policial actual logra prevenir el delito en esta área?", options=opciones_presencia_policial, horizontal=True)
razon_parcial = ""
if presencia_previene == "Parcialmente":
    razon_parcial = st.text_area("  - ¿Por qué?")
st.divider()


# --- Sección 4: Medidas de Prevención y Sugerencias ---
st.header("Sección 4: Medidas de Prevención y Sugerencias")
st.markdown("---")

# Pregunta 14
medidas_seguridad = st.text_area("14. ¿Qué medidas de seguridad ha implementado usted en su negocio? (Ej: Alarmas, cámaras, rejas, etc.)")

# Pregunta 15
sugerencia_jefe_policia = st.text_area("15. Si usted pudiera darle una orden directa al jefe de la policía de Pavas, ¿cuál sería la acción MÁS URGENTE que le pediría para mejorar la seguridad de su negocio y la de sus clientes?")
st.divider()


# --- Botón de Envío y guardado de datos ---
if st.button("Enviar Encuesta"):
    # Recopilar todos los datos en un diccionario
    datos_encuesta = {
        "timestamp": datetime.now(),
        "tipo_negocio": tipo_negocio,
        "otro_negocio_especificado": otro_negocio,
        "ubicacion": ubicacion,
        "maneja_efectivo": maneja_efectivo,
        "victima_asalto": victima_asalto,
        "movilizacion_delincuentes": movilizacion if victima_asalto == "Sí" else None,
        "uso_armas": uso_armas if victima_asalto == "Sí" else None,
        "tipo_arma_especificado": tipo_arma if victima_asalto == "Sí" and uso_armas == "Sí" else None,
        "hora_asalto": hora_asalto if victima_asalto == "Sí" else None,
        "principales_robado": principales_robado if victima_asalto == "Sí" else None,
        "otras_pertenencias_especificadas": otras_pertenencias if victima_asalto == "Sí" and principales_robado == "Otras pertenencias de clientes" else None,
        "denuncia_presentada": denuncia if victima_asalto == "Sí" else None,
        "razon_no_denuncia": razon_no_denuncia if victima_asalto == "Sí" and denuncia == "No" else None,
        "robo_vehiculos_cerca": robo_vehiculos,
        "tipo_robo_vehiculo": tipo_robo_vehiculo if robo_vehiculos == "Sí" else None,
        "facilita_robos": facilita_robos if robo_vehiculos == "Sí" else None,
        "problematica_extra": problematica_extra,
        "sentimiento_seguridad": seguridad_local,
        "frecuencia_patrullas": frecuencia_patrullas,
        "tiempo_respuesta": tiempo_respuesta,
        "presencia_previene": presencia_previene,
        "razon_parcial": razon_parcial if presencia_previene == "Parcialmente" else None,
        "medidas_seguridad": medidas_seguridad,
        "sugerencia_jefe_policia": sugerencia_jefe_policia,
    }
    
    # Aquí puedes agregar la lógica para guardar los datos.
    # Por ejemplo, a un archivo CSV, a una base de datos, etc.
    # A continuación, un ejemplo simple para guardar en un archivo CSV:
    
    try:
        # Convertir el diccionario a un DataFrame de pandas para manejarlo fácilmente
        df = pd.DataFrame([datos_encuesta])
        
        # Guardar en un archivo CSV. 'mode="a"' es para añadir al final, 'header=False' para no repetir los encabezados.
        # Se comprueba si el archivo existe para crear el encabezado solo una vez.
        try:
            df.to_csv("datos_encuesta.csv", mode="a", header=False, index=False, encoding="utf-8-sig")
        except FileNotFoundError:
            df.to_csv("datos_encuesta.csv", index=False, encoding="utf-8-sig")

        st.success("🎉 ¡Gracias por completar la encuesta! Tus respuestas han sido enviadas.")
    except Exception as e:
        st.error(f"Ocurrió un error al guardar los datos: {e}")
