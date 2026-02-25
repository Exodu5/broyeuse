import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_KEY")

st.set_page_config(page_title="Brutal optimiser", page_icon="⚡️")
st.title("⚡️ Brutal optimiser")
st.write("Transforme le jargon en actions concrètes.")

client = genai.Client(api_key=key)

text_to_process = st.text_area("Colle le texte à optimiser ici :")

if st.button("Optimiser maintenant"):
    if text_to_process:
        with st.spinner("Extraction de la moelle osseuse..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Tu es un assistant brutal et direct. Résume en 3 points d'action max, sans fioritures : {text_to_process}"
            )
            st.subheader("Analyse Brutale :")
            st.success(response.text)
    else:
        st.warning("Donne-moi de la matière à broyer.")