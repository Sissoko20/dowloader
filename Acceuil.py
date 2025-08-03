import streamlit as st
from yt_dlp import YoutubeDL
import os
from utils import clear_downloads, get_downloads

st.set_page_config(page_title="Téléchargeur YouTube", layout="centered")

st.title("🎧 Téléchargeur YouTube")

url = st.text_input("🔗 Lien YouTube")

mode = st.radio("🎯 Choix du format :", ["Audio (mp3)", "Vidéo (mp4)"])

if st.button("Télécharger"):
    if not url:
        st.warning("Veuillez entrer un lien valide")
    else:
        format = "mp3" if "Audio" in mode else "mp4"

        # Configuration yt-dlp
        if format == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [],
            }
        else:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
                'progress_hooks': [],
            }

        # Barre de progression
        progress_text = st.empty()
        bar = st.progress(0)

        def hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    percent = int(downloaded / total * 100)
                    bar.progress(min(percent, 100))
                    progress_text.text(f"⏳ Téléchargement... {percent}%")

            if d['status'] == 'finished':
                progress_text.text("✅ Terminé. Conversion en cours...")

        ydl_opts['progress_hooks'] = [hook]

        with YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                st.success("✅ Téléchargement et conversion terminés")
            except Exception as e:
                st.error(f"Erreur : {e}")

# Vider les téléchargements
if st.button("🧹 Vider les téléchargements"):
    clear_downloads()
    st.success("Dossier vidé !")
