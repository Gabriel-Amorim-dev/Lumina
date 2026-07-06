from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from prompts import QA_PROMPT
from config import GROQ_MODEL_NAME
import os


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment.")

    return ChatGroq(
        groq_api_key=api_key,
        model_name=GROQ_MODEL_NAME,
        temperature=0.0
    )


def get_rag_chain(retriever):
    llm = get_llm()
    question_answer_chain = create_stuff_documents_chain(llm, QA_PROMPT)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    return rag_chain
