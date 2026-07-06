from langchain_core.prompts import PromptTemplate

qa_template = """Use the following pieces of context to answer the user's question. 
If you don't know the answer based on the context provided, just say that you don't know, don't try to make up an answer.
Include the source document and page number(s) where applicable in your answer.

Context: {context}

Question: {input}

Helpful Answer:"""

QA_PROMPT = PromptTemplate(
    template=qa_template,
    input_variables=["context", "input"]
)
