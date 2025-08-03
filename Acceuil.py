import streamlit as st
from yt_dlp import YoutubeDL
import shutil
import os
from utils import clear_downloads, get_downloads

# Vérification de ffmpeg
FFMPEG_FOUND = shutil.which("ffmpeg") is not None

st.set_page_config(page_title="🎧 Téléchargeur YouTube", layout="centered")

# Design mobile-friendly
st.markdown("<h1 style='text-align: center;'>🎧 Téléchargeur YouTube</h1>", unsafe_allow_html=True)

url = st.text_input("🔗 Entrez le lien YouTube")

mode = st.radio("🎯 Choix du format :", ["Audio (mp3)", "Vidéo (mp4)"], horizontal=True)

if st.button("🚀 Télécharger"):
    if not url.strip():
        st.warning("⚠️ Veuillez entrer un lien YouTube valide")
    else:
        format = "mp3" if "Audio" in mode else "mp4"

        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'progress_hooks': [],
            'quiet': True,
            'noplaylist': True,
            'postprocessors': []
        }

        # Configuration selon le format
        if format == "mp3":
            ydl_opts['format'] = 'bestaudio/best'
            if FFMPEG_FOUND:
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                })
            else:
                st.warning("⚠️ ffmpeg non détecté. Fichier audio original sera téléchargé sans conversion.")
        else:
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
            if FFMPEG_FOUND:
                ydl_opts['merge_output_format'] = 'mp4'
            else:
                st.warning("⚠️ ffmpeg non détecté. Le fichier vidéo sera téléchargé dans son format source.")

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
            elif d['status'] == 'finished':
                progress_text.text("✅ Téléchargement terminé. Traitement en cours...")

        ydl_opts['progress_hooks'] = [hook]

        # Téléchargement
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                st.success(f"✅ Fichier téléchargé : {info['title']}")
        except Exception as e:
            if 'Video unavailable' in str(e):
                st.error("🚫 La vidéo est indisponible. Elle a peut-être été supprimée ou restreinte.")
            else:
                st.error(f"❌ Erreur lors du téléchargement : {str(e)}")

# Nettoyage des téléchargements
if st.button("🧹 Vider les téléchargements"):
    clear_downloads()
    st.success("✅ Dossier vidé !")
