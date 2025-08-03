import streamlit as st
from yt_dlp import YoutubeDL
import os

st.set_page_config(page_title="YouTube MP3 Downloader", layout="centered")

st.title("🎧 Téléchargeur YouTube → MP3")

url = st.text_input("Colle ici le lien de la vidéo ou playlist YouTube")

audio_format = st.selectbox("Choisis un format audio", ["mp3", "aac", "flac", "wav"])

if st.button("Télécharger"):
    if url:
        with st.spinner("Téléchargement en cours..."):
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'downloads/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_format,
                    'preferredquality': '192',
                }]
            }

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                st.success("Téléchargement terminé !")
            except Exception as e:
                st.error(f"Erreur : {e}")
    else:
        st.warning("Merci de coller un lien valide")

# Affiche les fichiers disponibles
if os.path.exists("downloads"):
    for filename in os.listdir("downloads"):
        if filename.endswith(audio_format):
            filepath = os.path.join("downloads", filename)
            with open(filepath, "rb") as f:
                st.download_button(label=f"⬇️ Télécharger {filename}", data=f, file_name=filename)
