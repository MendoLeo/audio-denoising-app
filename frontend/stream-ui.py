import streamlit as st
import requests
from pydub import AudioSegment
from io import BytesIO

# Titre de l'application
st.title("Interface de débruitage d'audio")

# Zone pour charger un ou plusieurs fichiers audio
uploaded_files = st.file_uploader(
    "Chargez un ou plusieurs fichiers audio :", type=["wav", "mp3", "ogg", 'pcm', 'opus'], accept_multiple_files=True
)

# Bouton pour démarrer le traitement
if uploaded_files:
    if st.button("Lancer le débruitage"):
        # URL de l'API de débruitage (en local)
        api_url = "http://127.0.0.1:8000/denoise/"

        for uploaded_file in uploaded_files:
            st.subheader(f"Fichier : {uploaded_file.name}")

            # Lecture et affichage du fichier audio original
            audio_bytes = uploaded_file.read()
            st.audio(audio_bytes, format="audio/mpeg", start_time=0)

            # Envoi du fichier à l'API de débruitage
            st.write("**Traitement en cours...**")
            try:
                files = {"file": (uploaded_file.name, audio_bytes)}
                response = requests.post(api_url, files=files)

                if response.status_code == 200:
                    st.write(f"✅ **Débruitage terminé pour {uploaded_file.name} !**")

                    # Récupération de l'audio débruité
                    debruite_audio = BytesIO(response.content)
                    debruite_audio.seek(0)

                    # Affichage de l'audio débruité
                    st.audio(debruite_audio, format="audio/mpeg", start_time=0)
                else:
                    st.error(f"Erreur lors du traitement de {uploaded_file.name} : " + response.text)
            except Exception as e:
                st.error(f"Une erreur est survenue lors du traitement de {uploaded_file.name} : {e}")
