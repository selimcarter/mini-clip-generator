import streamlit as st
import uuid
import openai
import yt_dlp
import os
import re

from utils.video_loader import download_video
from utils.video_processor import extract_clips
from utils.content_analyzer import transcribe_video, extract_important_segments

st.set_page_config(
    page_title="Générateur de Clips Viraux",
    layout="wide",
    page_icon="🎬"
)

if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
else:
    openai.api_key = st.text_input("Entrez votre clé OpenAI (GPT-4)", type="password")
    if not openai.api_key:
        st.warning("Veuillez entrer votre clé OpenAI pour continuer.")
        st.stop()

st.title("Générateur de Clips Viraux")
st.subheader("Transforme une vidéo MP4 ou une URL YouTube en extraits courts à fort potentiel viral.")

mode = st.radio("Choisissez une méthode :", ["Uploader un fichier MP4", "Coller une URL YouTube"])
video_path = None

if mode == "Uploader un fichier MP4":
    video_file = st.file_uploader("Téléverse ta vidéo (.mp4 uniquement)", type=["mp4"])
    if video_file is not None:
        temp_video_path = f"temp_{uuid.uuid4().hex}.mp4"
        with open(temp_video_path, "wb") as f:
            f.write(video_file.read())
        video_path = temp_video_path

elif mode == "Coller une URL YouTube":
    youtube_url = st.text_input("Colle une URL YouTube ici")
    if youtube_url:
        try:
            video_path = download_video(youtube_url)
            st.success("Vidéo téléchargée avec succès !")
        except Exception as e:
            st.error(f"Erreur lors du téléchargement : {e}")
            st.stop()

if video_path:
    try:
        with st.spinner("Transcription en cours..."):
            full_text = transcribe_video(video_path)

        with st.spinner("Analyse des segments..."):
            clips = extract_important_segments(full_text)

        with st.spinner("Génération des clips..."):
            generated_clips = extract_clips(video_path, clips)

        st.success("Clips générés avec succès !")
        for clip_path in generated_clips:
            st.video(clip_path)
    except Exception as e:
        st.error(f"Une erreur est survenue pendant le traitement : {e}")