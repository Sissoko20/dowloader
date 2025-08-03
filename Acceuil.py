import streamlit as st
from yt_dlp import YoutubeDL
import os
import shutil
import subprocess

# Crée dossier downloads si inexistant
DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

st.set_page_config(page_title="Téléchargeur YouTube", layout="centered")

st.markdown(
    """
    <style>
        .stTextInput, .stRadio, .stButton {
            font-size: 1.1rem !important;
        }
        @media (max-width: 768px) {
            .stTextInput, .stRadio, .stButton {
                font-size: 1rem !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📥 Téléchargeur YouTube")

url = st.text_input("🔗 Lien YouTube")

mode = st.radio("🎯 Choix du format :", ["Audio (mp3)", "Vidéo (mp4)"])

ffmpeg_found = shutil.which("ffmpeg") is not None

if not ffmpeg_found:
    st.warning("⚠️ FFmpeg est introuvable. Le fichier sera téléchargé dans son format source sans conversion.")

if st.button("Télécharger"):
    if not url:
        st.warning("❗ Veuillez entrer un lien valide")
    else:
        format_choice = "mp3" if "Audio" in mode else "mp4"
        progress_text = st.empty()
        bar = st.progress(0)

        def progress_hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    percent = int(downloaded / total * 100)
                    bar.progress(min(percent, 100))
                    progress_text.text(f"⏳ Téléchargement... {percent}%")
            elif d['status'] == 'finished':
                progress_text.text("✅ Terminé. Conversion en cours...")

        ydl_opts = {
            'format': 'bestaudio/best' if format_choice == 'mp3' else 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'noplaylist': True,
            'quiet': True,
        }

        if format_choice == 'mp3' and ffmpeg_found:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        elif format_choice == 'mp4' and ffmpeg_found:
            ydl_opts['merge_output_format'] = 'mp4'

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            st.success("✅ Téléchargement terminé !")
        except Exception as e:
            st.error("❌ Une erreur est survenue.")
            st.exception(e)

# Option : Vider les téléchargements
if st.button("🧹 Vider les téléchargements"):
    for f in os.listdir(DOWNLOADS_DIR):
        os.remove(os.path.join(DOWNLOADS_DIR, f))
    st.success("🧼 Téléchargements effacés.")
