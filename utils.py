import os
import pdfplumber
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import UPLOAD_DIR


def save_uploaded_file(uploaded_file):
    """Saves a Streamlit UploadedFile to the uploads directory."""
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def process_pdf(file_path):
    """Extracts text from a PDF and returns a list of LangChain Document objects with metadata."""
    documents = []
    file_name = os.path.basename(file_path)

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                doc = Document(
                    page_content=text,
                    metadata={"source": file_name, "page": i + 1}
                )
                documents.append(doc)
    return documents


def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Splits documents into smaller chunks for the vector store."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return text_splitter.split_documents(documents)
