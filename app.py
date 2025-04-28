import os
import streamlit as st
import base64
from gtts import gTTS
from PIL import Image
import glob
import time

# Título de la aplicación
st.title("Conversión de Texto a Audio")

# Subida de una imagen personalizada
st.subheader("Carga una imagen propia:")
uploaded_image = st.file_uploader("Sube una imagen en formato PNG, JPG o JPEG:", type=["png", "jpg", "jpeg"])
if uploaded_image is not None:
    # Muestra la imagen cargada
    image = Image.open(uploaded_image)
    st.image(image, caption="Imagen cargada por el usuario", use_column_width=True)
else:
    # Muestra una imagen por defecto si no se carga ninguna
    default_image = Image.open('gato_raton.png')  # Asegúrate de tener esta imagen en tu directorio
    st.image(default_image, caption="Imagen predeterminada", width=350)

# Entrada de texto personalizada
st.subheader("Escribe tu propio texto para escucharlo:")
custom_text = st.text_area("Introduce el texto que quieres convertir en audio:")

# Selección del idioma para el texto
tld = 'com'
option_lang = st.selectbox(
    "Selecciona el idioma:",
    ("Español", "English")
)
if option_lang == "Español":
    lg = 'es'
elif option_lang == "English":
    lg = 'en'

# Función para convertir texto a audio
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    try:
        file_name = text[:20].replace(" ", "_")  # Nombre del archivo basado en las primeras palabras
    except:
        file_name = "audio"
    tts.save(f"temp/{file_name}.mp3")
    return file_name, text

# Crear carpeta temporal para guardar el audio
try:
    os.mkdir("temp")
except FileExistsError:
    pass

# Botón para convertir el texto a audio
if st.button("Convertir texto a audio"):
    if custom_text.strip():  # Verifica que el texto no esté vacío
        result, output_text = text_to_speech(custom_text, lg)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        
        st.markdown("### Escucha tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # Proporcionar opción para descargar el archivo
        def get_binary_file_downloader_html(bin_file, file_label='File'):
            with open(bin_file, "rb") as f:
                data = f.read()
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
            return href

        st.markdown(get_binary_file_downloader_html(f"temp/{result}.mp3", file_label="Archivo de Audio"), unsafe_allow_html=True)
    else:
        st.error("Por favor, escribe un texto antes de convertirlo a audio.")

# Función para limpiar archivos temporales después de 7 días
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Archivo eliminado:", f)

remove_files(7)

