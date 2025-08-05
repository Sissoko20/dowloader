import streamlit as st
from yt_dlp import YoutubeDL
import os

DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

st.set_page_config(page_title="Téléchargeur YouTube Mobile", layout="centered")
st.title("📱 Téléchargeur YouTube Mobile")

# Injecter le manifest et le service worker
st.markdown("""
<link rel="manifest" href="/manifest.json">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js');
  }
</script>
""", unsafe_allow_html=True)

# 🔍 Recherche YouTube
search_query = st.text_input("🔎 Rechercher une vidéo YouTube")

if search_query:
    with YoutubeDL({'quiet': True}) as ydl:
        try:
            results = ydl.extract_info(f"ytsearch5:{search_query}", download=False)['entries']
            st.subheader("🎯 Résultats de recherche")
            for video in results:
                st.markdown(f"**{video['title']}**")
                st.video(video['webpage_url'])
                if st.button(f"Télécharger {video['title']}", key=video['id']):
                    url = video['webpage_url']
        except Exception as e:
            st.error("❌ Erreur lors de la recherche.")
            st.exception(e)

# 🔗 Téléchargement direct
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

# 📁 Liste des fichiers téléchargés
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

# 🧹 Nettoyage
if st.button("🧹 Vider les téléchargements"):
    for f in files:
        os.remove(os.path.join(DOWNLOADS_DIR, f))
    st.success("🧼 Téléchargements effacés.")
