import streamlit as st

@st.cache_data(show_spinner=False)
def brutal_analysis(_client, model, text, context_type="texte"):
    """
    Analyzes the text using the Gemini model and displays the result.
    
    Args:
        _client: The initialized Google GenAI client.
        model: The model name to use.
        text: The text content to analyze.
        context_type: Type of content ("texte" or "transcription vidéo") for the prompt.
    """
    prompt = f"Tu es un assistant brutal et direct. Résume en 3 ou 5 points d'action max, sans fioritures : {text}"
    if context_type == "transcription vidéo":
        prompt = f"Tu es un assistant brutal et direct. Résume en 3 ou 5 points d'action max, sans fioritures cette transcription vidéo : {text}"
    else:
        pass
    
    with st.spinner("Extraction de la moelle osseuse..."):
        try:
            response = _client.models.generate_content(
                model=model,
                contents=prompt
            )
            st.subheader("⚙️ RÉSULTAT DU BROYAGE")
            st.code(response.text, language="markdown")
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                return "⚠️ Trop de requêtes. L'API sature, attends une minute."
            elif "401" in error_msg or "API_KEY" in error_msg:
                return "⚠️ Problème de configuration de la clé API."
            else:
                return f"⚠️ Une erreur technique est survenue : {error_msg[:50]}..."
