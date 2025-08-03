import streamlit as st
import os
from utils import get_downloads

st.title("📁 Mes Téléchargements")

files = get_downloads()

if not files:
    st.info("Aucun fichier téléchargé pour le moment.")
else:
    to_delete = st.multiselect("Sélectionne les fichiers à supprimer :", files)

    for f in files:
        with open(f"downloads/{f}", "rb") as file:
            st.download_button(label=f"⬇️ Télécharger {f}", data=file, file_name=f)

    if st.button("❌ Supprimer les fichiers sélectionnés"):
        for f in to_delete:
            os.remove(os.path.join("downloads", f))
        st.success("Fichiers supprimés !")
        st.experimental_rerun()
