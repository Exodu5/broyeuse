import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from utils import brutal_analysis

load_dotenv()

model = os.getenv("GEMINI_MODEL")
key = os.getenv("GEMINI_KEY")
ytb_api = YouTubeTranscriptApi()


st.set_page_config(page_title="Brutal optimiser", page_icon="⚡️")
st.title("⚡️ Brutal optimiser")
st.write("Transforme le jargon en actions concrètes.")

client = genai.Client(api_key=key)

c1 = st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center", gap="small", border=True)
with c1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png", width=50)
    youtube_link = st.text_input(label="Lien YouTube à analyser :")

c2 = st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center", gap="small", border=True)
with c2:
    text_to_process = st.text_area("Colle le texte à optimiser ici :")

if st.button("Optimiser maintenant"):

    if text_to_process:
        brutal_analysis(client, model, text_to_process)
    elif youtube_link:
        with st.spinner("Broyage de la vidéo..."):
            fetched_transcript = ytb_api.fetch(youtube_link.split("v=")[-1], languages=['fr', 'en'])
            full_text = " ".join([entry.text for entry in fetched_transcript])
        
        brutal_analysis(client, model, full_text, context_type="transcription vidéo")
    else:
        st.warning("Donne-moi de la matière à broyer.")
