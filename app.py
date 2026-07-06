import logging
import streamlit as st

from utils import save_uploaded_file, process_pdf, split_documents
from embeddings import get_embeddings_model
from vector_store import save_to_vector_store, get_retriever, reset_vector_store
from rag import get_rag_chain
from styles.loader import load_css
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Lumina",
    page_icon="✨",
)

load_css()


st.html("""
<div class="hero">
    <div class="hero-badge">
        ✨ AI-Powered Document Intelligence
    </div>

    <h1 class="hero-title">
        Lumina
    </h1>

    <p class="hero-subtitle">
        Build a searchable knowledge base from your PDFs and receive
        accurate, citation-backed answers in seconds.
    </p>
</div>
""")

col1, col2, col3 = st.columns(3)

cards = [
    ("📄", "Upload PDFs",
     "Import reports, books, contracts, manuals or research papers."),

    ("🧠", "AI Understanding",
     "Semantic search powered by Retrieval-Augmented Generation."),

    ("📚", "Reliable Answers",
     "Every answer includes citations linked to your documents.")
]

if "messages" not in st.session_state:
    st.session_state.messages = []
if "library" not in st.session_state:
    st.session_state.library = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

def render_citations(sources):
    if not sources:
        return
    chips = "".join(f'<span class="citation-chip">{s}</span>' for s in sources)
    st.markdown(f'<div class="citations">{chips}</div>', unsafe_allow_html=True)


with st.sidebar:
    st.markdown("### Workspace")
    uploaded_files = st.file_uploader(
        "Import Documents", type="pdf", accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if st.button("Add to library", use_container_width=True, type="primary"):
        if uploaded_files:
            with st.spinner("Reading your documents..."):
                try:
                    embeddings = get_embeddings_model()
                    all_chunks = []
                    added = []
                    for uploaded_file in uploaded_files:
                        file_path = save_uploaded_file(uploaded_file)
                        docs = process_pdf(file_path)
                        chunks = split_documents(docs)
                        all_chunks.extend(chunks)
                        added.append(uploaded_file.name)

                    if all_chunks:
                        save_to_vector_store(all_chunks, embeddings, st.session_state.session_id)
                        st.session_state.library.extend(added)
                        st.toast(f"Knowledge base updated. {len(added)} documents are ready to search.", icon="📖")
                except Exception:
                    logger.exception("Failed to add documents to the library")
                    st.error("Couldn't add those documents. Please try again.")
        else:
            st.warning("Choose at least one PDF first.")

    st.divider()

    if st.session_state.library:
        st.markdown(
            f'<p class="lib-count">{len(st.session_state.library)} document(s) indexed</p>',
            unsafe_allow_html=True,
        )
        for name in st.session_state.library:
            st.markdown(
                f'<div class="lib-item"><span class="dot"></span><span>{name}</span></div>',
                unsafe_allow_html=True,
            )
        if st.button("Clear conversation", use_container_width=True):
            embeddings = get_embeddings_model()
            reset_vector_store(embeddings, st.session_state.session_id)
            st.session_state.messages = []
            st.session_state.library = []
            st.rerun()
    else:
        st.caption("Nothing here yet — add a PDF to get started.")

for message in st.session_state.messages:
    avatar = "📖" if message["role"] == "assistant" else "🧑"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        render_citations(message.get("sources"))

if not st.session_state.get("library") and not st.session_state.get("messages"):
    col1, col2, col3 = st.columns(3, gap="small")
    for col, (icon, title, desc) in zip((col1, col2, col3), cards):
        with col:
            st.markdown(f"""
            <div class="feature-card">
              <div class="feature-icon">{icon}</div>
              <div class="feature-title">{title}</div>
              <div class="feature-description">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

if not st.session_state.messages and not st.session_state.library:

    st.markdown("""
        <div class="empty-state">
            <div class="icon">📚</div>
            <h3>Start your knowledge workspace</h3>
            <p>Add a document on the left, then ask your first question here.</p>
        </div>
    """, unsafe_allow_html=True)
elif not st.session_state.messages:
    st.markdown("""
        <div class="empty-state">
            <div class="icon">💬</div>
            <h3>Ready when you are</h3>
            <p>Ask a question below to explore your library.</p>
        </div>
    """, unsafe_allow_html=True)

if prompt := st.chat_input("What would you like to know?..."):
    if not st.session_state.library:
        st.warning("Add at least one document to your library before asking a question.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="📖"):
        try:
            with st.spinner("Thinking..."):
                embeddings = get_embeddings_model()
                retriever = get_retriever(embeddings, st.session_state.session_id)
                rag_chain = get_rag_chain(retriever)
                response = rag_chain.invoke({"input": prompt})
                answer = response["answer"]

                sources = []
                if response.get("context"):
                    for doc in response["context"]:
                        name = doc.metadata.get("source", "Unknown")
                        page = doc.metadata.get("page", "Unknown")
                        sources.append(f"{name} · p.{page}")
                sources = list(dict.fromkeys(sources))

                st.markdown(answer)
                render_citations(sources)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "sources": sources}
                )
        except Exception:
            logger.exception("Failed to generate an answer")
            fallback = "Something went wrong finding that answer. Please try again."
            st.error(fallback)
            st.session_state.messages.append({"role": "assistant", "content": fallback})
