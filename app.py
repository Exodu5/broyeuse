import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from utils import brutal_analysis

load_dotenv()

model = os.getenv("GEMINI_MODEL")
key = os.getenv("GEMINI_KEY")
# ytb_api = YouTubeTranscriptApi() -- moved to load_transcript



st.set_page_config(page_title="La Broyeuse", page_icon="🦷")
st.markdown("""
    <style>
    /* Fond sombre et police mono pour le côté technique */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Personnalisation des headers */
    h1, h2, h3 {
        color: #ff4b4b !important; /* Rouge brutal */
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Style des boutons : brut et carré */
    .stButton>button {
        width: 100%;
        border-radius: 0px;
        border: 2px solid #ff4b4b;
        background-color: transparent;
        color: #ff4b4b;
        font-weight: bold;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #ff4b4b;
        color: white;
    }

    /* Champs de saisie */
    .stTextArea textarea, .stTextInput input {
        background-color: #1a1c24 !important;
        border: 1px solid #333 !important;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 La Broyeuse")
st.write("Transforme le blabla en résumés concrets.")

client = genai.Client(api_key=key)

c1 = st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center", gap="small", border=True)
with c1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png", width=50)
    youtube_link = st.text_input(label="Lien YouTube à analyser :")

c2 = st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center", gap="small", border=True)
with c2:
    text_to_process = st.text_area("Colle le texte à résumer ici :")

@st.cache_data
def load_transcript(youtube_link):
    ytb_api = YouTubeTranscriptApi()
    fetched_transcript = ytb_api.fetch(youtube_link.split("v=")[-1], languages=['fr', 'en'])
    return " ".join([entry.text for entry in fetched_transcript])

if st.button("Optimiser maintenant"):

    if text_to_process:
        brutal_analysis(client, model, text_to_process)
    elif youtube_link:
        with st.spinner("Broyage de la vidéo..."):
            full_text = load_transcript(youtube_link)
        
        brutal_analysis(client, model, full_text, context_type="transcription vidéo")
    else:
        st.warning("Donne-moi de la matière à broyer.")
