import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Application configuration
UPLOAD_DIR = "uploads"
CHROMA_DB_DIR = "chroma_db"

# Model configurations
GROQ_MODEL_NAME = "llama-3.3-70b-versatile"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    return ChatGroq(
        groq_api_key=api_key,
        model_name=GROQ_MODEL_NAME,
        temperature=0
    )

get_llm()