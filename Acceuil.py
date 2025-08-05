import streamlit as st
from yt_dlp import YoutubeDL
import os

DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

st.set_page_config(page_title="Téléchargeur YouTube Mobile", layout="centered")
st.title("📱 Téléchargeur YouTube Mobile")

url = st.text_input("🔗 Lien YouTube (vidéo ou playlist)")
mode = st.radio("🎯 Format souhaité :", ["Audio (.webm)", "Vidéo (.mp4)"])

if st.button("📥 Télécharger"):
    if not url:
        st.warning("❗ Veuillez entrer un lien valide.")
    else:
        format_code = "bestaudio" if "Audio" in mode else "bestvideo+bestaudio/best"

        ydl_opts = {
            'format': format_code,
            'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
            'noplaylist': False,
            'quiet': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                st.success(f"✅ Téléchargement terminé : {info.get('title', 'Fichier')}")
        except Exception as e:
            st.error("❌ Une erreur est survenue.")
            st.exception(e)

# Liste des fichiers téléchargés
st.subheader("📁 Fichiers disponibles")
files = os.listdir(DOWNLOADS_DIR)
if files:
    for f in files:
        file_path = os.path.join(DOWNLOADS_DIR, f)
        st.markdown(f"📄 **{f}**")
        with open(file_path, "rb") as file:
            st.download_button(label="⬇️ Télécharger", data=file, file_name=f)
else:
    st.write("Aucun fichier téléchargé.")

# Nettoyage
if st.button("🧹 Vider les téléchargements"):
    for f in files:
        os.remove(os.path.join(DOWNLOADS_DIR, f))
    st.success("🧼 Téléchargements effacés.")
