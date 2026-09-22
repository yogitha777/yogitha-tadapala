import os
import streamlit as st
from dotenv import load_dotenv

from rag_pipeline import (
    process_and_index_documents,
    load_persisted_knowledge_base,
    generate_grounded_answer,
    DEFAULT_GROQ_MODEL,
)
from vector_store import DEFAULT_EMBEDDING_MODEL
from prompt import EXACT_FALLBACK_RESPONSE

load_dotenv()

st.set_page_config(
    page_title="Smart Document Q&A Assistant - Student Study Edition",
    page_icon="🎓",
    layout="wide",
)


def init_session_state() -> None:
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = load_persisted_knowledge_base()
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = []
    if "messages" not in st.session_state:
        st.session_state.messages = []


def reset_documents_and_vector_store() -> None:
    st.session_state.vector_store = None
    st.session_state.processed_files = []
    st.session_state.messages = []


def clear_chat_history() -> None:
    st.session_state.messages = []


def main() -> None:
    init_session_state()

    # Custom styling for student edition presentation
    st.markdown(
        """
        <style>
        .student-header {
            font-size: 2.1rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 0.2rem;
        }
        .student-caption {
            font-size: 1.05rem;
            color: #4B5563;
            margin-bottom: 0.8rem;
        }
        .stMetric {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='student-header'>🎓 Smart Document Q&A Assistant</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='student-caption'>Intelligent Academic & Document Assistant with Verified Page-Level Citations</div>",
        unsafe_allow_html=True,
    )

    # Academic & Responsible AI Guidance
    st.info(
        "💡 **Academic Integrity & AI Guidance**: Answers are synthesized strictly from retrieved passages "
        "in your uploaded materials. Cross-reference important formulas, dates, and definitions with primary sources."
    )

    with st.expander("📖 Student Guide: How the Q&A Engine Works", expanded=False):
        st.markdown(
            """
            1. **Upload Study Documents**: Select lecture notes, textbook chapters, or reference PDFs.  
            2. **Text Extraction**: Reads text page-by-page with `pypdf`, preserving document name and 1-based page metadata.  
            3. **Semantic Chunking**: Segments content using LangChain's `RecursiveCharacterTextSplitter` (700–1000 chars).  
            4. **Neural Embeddings**: Generates dense vectors using Sentence Transformers (`all-MiniLM-L6-v2`).  
            5. **FAISS Local Store**: Indexes embeddings into local disk-backed FAISS storage (`vector_store/saved_index/`).  
            6. **Top-k Context Retrieval**: Retrieves the top relevant study passages based on semantic similarity.  
            7. **Grounded Synthesis**: Groq LLM answers questions strictly from retrieved passages with prompt-injection defense.  
            8. **Attribution & Fallback**: Returns exact page citations, or a strict fallback refusal if unmentioned.
            """
        )

    # --- SIDEBAR UI ---
    with st.sidebar:
        st.header("📂 Study Materials & Ingestion")

        # PDF Uploader in Sidebar
        uploaded_files = st.file_uploader(
            "Upload Study PDF(s)",
            type=["pdf"],
            accept_multiple_files=True,
            help="Select course slides, lecture notes, textbook chapters, or reference PDFs (Max 25 MB each).",
        )

        if uploaded_files:
            st.markdown("**Selected Documents:**")
            for f in uploaded_files:
                st.caption(f"• `{f.name}` ({f.size / (1024*1024):.2f} MB)")

        # Ingest Documents Button directly underneath PDF upload area
        process_button = st.button(
            "🚀 Ingest & Index Materials",
            type="primary",
            disabled=not uploaded_files,
            use_container_width=True,
        )

        st.divider()

        st.markdown("**🔍 Retrieval Tuning**")
        chunk_size = st.slider("Passage Chunk Size (chars)", 400, 1500, 800, 50)
        chunk_overlap = st.slider("Passage Overlap (chars)", 0, 300, 120, 10)
        top_k = st.slider("Context Chunks to Retrieve (top-k)", 1, 8, 4)

        if process_button and uploaded_files:
            if chunk_overlap >= chunk_size:
                st.error("Chunk overlap must be smaller than chunk size.")
            else:
                try:
                    with st.spinner("Extracting text, chunking, and indexing in FAISS vector store..."):
                        vector_store, num_chunks, doc_names = process_and_index_documents(
                            uploaded_files,
                            chunk_size=chunk_size,
                            chunk_overlap=chunk_overlap,
                            persist=True,
                        )

                    st.session_state.vector_store = vector_store
                    st.session_state.processed_files = doc_names
                    st.session_state.messages = []
                    st.success(f"Successfully indexed {len(doc_names)} file(s) into {num_chunks} chunks!")
                except Exception as err:
                    st.error(f"Processing Error: {err}")

        st.divider()

        st.header("⚙️ Model & Inference Settings")

        # Secure API Key Handling (NEVER displays raw API key string in UI)
        env_api_key = os.getenv("GROQ_API_KEY", "")
        if env_api_key:
            st.success("🔒 Groq API: Configured (.env)")
            override_key = st.text_input(
                "Override Groq API Key (Optional)",
                type="password",
                value="",
                help="Leave blank to use GROQ_API_KEY from .env",
            )
            api_key = override_key.strip() if override_key.strip() else env_api_key
        else:
            st.warning("⚠️ Groq API Key Not Found in .env")
            api_key = st.text_input(
                "Enter Groq API Key",
                type="password",
                value="",
                help="Enter your Groq API key (e.g. gsk_...)",
            ).strip()

        model_name = st.selectbox(
            "Reasoning Engine (Groq Model)",
            ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "groq/compound"],
            index=0,
        )

        st.caption(f"Embedding Engine: `{DEFAULT_EMBEDDING_MODEL}`")

        st.divider()

        if st.button("🔄 Clear Knowledge Base & Reset", use_container_width=True):
            reset_documents_and_vector_store()
            st.rerun()

    # --- MAIN AREA ---
    if st.session_state.vector_store is None:
        st.info("👈 Please upload your study documents in the sidebar and click **Ingest & Index Materials** to start.")
        return

    # Knowledge Base Metrics Banner
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Indexed Documents", len(st.session_state.processed_files) or "Loaded Index")
    m_col2.metric("Knowledge Chunks", len(st.session_state.vector_store.chunks))
    m_col3.metric("Vector Database", "FAISS (Local Disk)")

    # Action Toolbar with Dedicated Clear Chat Button
    c_col1, c_col2 = st.columns([4, 1])
    with c_col2:
        if st.button("🧹 Clear Conversation", use_container_width=True):
            clear_chat_history()
            st.rerun()

    # Render Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("📌 Grounded Source Passages & Page References"):
                    for src in msg["sources"]:
                        st.markdown(f"**📄 Document:** `{src['source']}` | **📖 Page:** `{src['page_number']}` | **🔖 Chunk ID:** `{src['chunk_id']}`")
                        st.caption(f"Similarity Score: {src['score']:.4f}")
                        st.text(src["text"])

    # Chat Input Box
    question = st.chat_input("Ask a question based on your uploaded documents...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching FAISS index and synthesizing grounded response..."):
                try:
                    answer, sources = generate_grounded_answer(
                        question=question,
                        vector_store=st.session_state.vector_store,
                        top_k=top_k,
                        api_key=api_key,
                        model_name=model_name,
                    )
                    st.markdown(answer)

                    if sources and answer != EXACT_FALLBACK_RESPONSE:
                        with st.expander("📌 Grounded Source Passages & Page References"):
                            for src in sources:
                                st.markdown(f"**📄 Document:** `{src['source']}` | **📖 Page:** `{src['page_number']}` | **🔖 Chunk ID:** `{src['chunk_id']}`")
                                st.caption(f"Similarity Score: {src['score']:.4f}")
                                st.text(src["text"])

                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer, "sources": sources}
                    )
                except Exception as err:
                    st.error(f"Error generating answer: {err}")


if __name__ == "__main__":
    main()