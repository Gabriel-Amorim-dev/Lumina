from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL_NAME
import streamlit as st

@st.cache_resource(show_spinner="Running embending models...")
def get_embeddings_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
