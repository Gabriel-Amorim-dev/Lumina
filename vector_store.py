from langchain_chroma import Chroma
from config import CHROMA_DB_DIR


def get_vector_store(embeddings, collection_name):
    """Returns an instance of the Chroma vector store for a given collection (session)."""
    return Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings,
        collection_name=collection_name,
    )


def save_to_vector_store(documents, embeddings, collection_name):
    """Saves a list of LangChain Document objects to the vector store."""
    vector_store = get_vector_store(embeddings, collection_name)
    vector_store.add_documents(documents)
    return vector_store


def get_retriever(embeddings, collection_name, search_kwargs={"k": 4}):
    """Returns a retriever object for similarity search."""
    vector_store = get_vector_store(embeddings, collection_name)
    return vector_store.as_retriever(search_kwargs=search_kwargs)


def reset_vector_store(embeddings, collection_name):
    """Deletes all documents from the current session's collection."""
    vector_store = get_vector_store(embeddings, collection_name)
    vector_store.delete_collection()