import cv2
import numpy as np
import pytesseract
import streamlit as st
from PIL import Image

# Configuración de página con un diseño más amplio y título profesional
st.set_page_config(
    page_title="Escáner Inteligente de Texto", page_icon="🔍", layout="wide"
)

st.title("🔍 Escáner Inteligente de Texto (OCR)")
st.caption(
    "Captura una imagen o documento para extraer su contenido en texto automáticamente."
)

# Panel lateral de configuración
with st.sidebar:
    st.header("⚙️ Opciones de Procesamiento")

    # Reemplazamos la radio simple por selecciones más descriptivas
    modo_procesamiento = st.selectbox(
        "Estilo de Filtro",
        ["Sin Filtro (Original)", "Invertir Colores", "Escala de Grises"],
    )

    # Añadimos un selector de idioma para Tesseract
    idioma = st.selectbox(
        "Idioma del texto",
        ["spa (Español)", "eng (Inglés)"],
        help="Asegúrate de tener instalado el paquete de idioma en Tesseract.",
    )
    lang_code = "spa" if "spa" in idioma else "eng"

# Layout en 2 columnas para organizar mejor la vista
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("1. Captura de Imagen")
    img_file_buffer = st.camera_input("Toma una foto al documento o texto")

if img_file_buffer is not None:
    # Convertir el buffer de Streamlit a formato OpenCV
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(
        np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR
    )

    # Aplicar el filtro seleccionado
    if modo_procesamiento == "Invertir Colores":
        cv2_img = cv2.bitwise_not(cv2_img)
    elif modo_procesamiento == "Escala de Grises":
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)

    # Conversión necesaria para PyTesseract y Streamlit
    if len(cv2_img.shape) == 3:
        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    else:
        img_rgb = cv2_img  # Ya está en escala de grises

    # Extracción del texto
    texto_detectado = pytesseract.image_to_string(
        img_rgb, lang=lang_code
    ).strip()

    with col_der:
        st.subheader("2. Texto Detectado")

        if texto_detectado:
            # Mostrar métricas del texto procesado
            num_caracteres = len(texto_detectado)
            num_palabras = len(texto_detectado.split())

            st.metric(
                label="Estadísticas",
                value=f"{num_palabras} palabras",
                delta=f"{num_caracteres} caracteres",
            )

            # Área de texto interactiva para poder copiar fácilmente
            st.text_area(
                "Resultado:",
                texto_detectado,
                height=250,
                help="Puedes editar o copiar el texto desde esta área.",
            )
        else:
            st.warning(
                "⚠️ No se detectó texto en la imagen. Intenta cambiar el filtro o enfocar mejor."
            )
else:
    with col_der:
        st.info("👈 Toma una foto desde el panel izquierdo para ver el texto.")


    


