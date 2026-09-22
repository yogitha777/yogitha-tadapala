# 🎓 Smart Document Q&A Assistant (Student Study Edition)

A production-ready **Retrieval-Augmented Generation (RAG)** academic and document assistant that enables students and researchers to upload study materials such as textbooks, lecture slides, syllabi, and research papers and receive grounded answers backed by **exact document and page-number citations**.

---

## 1. Problem Statement

Large PDF documents are difficult to navigate manually. Searching for specific details across multi-page documents is slow and error-prone. Standard keyword searches can fail on natural-language queries, while general LLMs may hallucinate when asked about private domain documents.

This project solves this by retrieving relevant text passages from uploaded PDF documents and generating answers grounded strictly in the retrieved document content.

---

## 2. Project Objective

* **Extract & Tag Metadata:** Read PDF pages using `pypdf` and attach document name and 1-indexed page-number metadata.

* **Chunk & Embed:** Split documents using LangChain's `RecursiveCharacterTextSplitter` and generate dense vector embeddings with `sentence-transformers/all-MiniLM-L6-v2`.

* **FAISS Vector Database:** Index embeddings using FAISS and persist the index locally.

* **Grounded LLM Answers:** Query the Groq LLM using strict system prompts to reduce hallucinations and defend against document prompt injection.

* **Source Attribution:** Display the exact document name and page number for generated answers.

* **Fallback Refusal:** Return the exact string:

  `I could not find this information in the uploaded documents.`

  when the requested information is not available in the uploaded documents.

---

## 3. How the RAG Workflow Works

```text
Upload PDFs
     │
     ▼
Extract Text using pypdf
     │
     ▼
Page Metadata
     │
     ▼
Chunking using LangChain
     │
     ▼
Generate Embeddings
     │
     ▼
FAISS Vector Search
     │
     ▼
Retrieve Relevant Passages
     │
     ▼
Prompt Guardrails
     │
     ▼
Groq LLM
     │
     ▼
Answer + Document/Page Citation
```

### Workflow Steps

1. **Document Upload:** Users upload one or more PDF files through the Streamlit sidebar.

2. **Text Extraction:** `document_loader.py` reads PDF pages using `pypdf`, capturing source filename and page number metadata.

3. **Chunking:** `vector_store.py` splits extracted text using `RecursiveCharacterTextSplitter`.

4. **Vector Embedding:** Document chunks are converted into vector embeddings using `all-MiniLM-L6-v2`.

5. **FAISS Storage:** Embeddings and metadata are stored in a local FAISS vector index.

6. **Query & Retrieval:** The user's question is converted into an embedding and the most relevant document chunks are retrieved.

7. **Prompt Guardrail & Generation:** Retrieved context is combined with system instructions and sent to the Groq LLM.

8. **Attribution / Refusal:** The application displays the generated answer together with document and page references. If the required information is unavailable, the application returns the predefined fallback response.

---

## 4. Technology Stack

| Component                 | Technology                             |
| ------------------------- | -------------------------------------- |
| Programming Language      | Python 3.14                            |
| PDF Processing            | pypdf                                  |
| Text Chunking             | LangChain                              |
| Embedding Model           | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database           | FAISS                                  |
| LLM Engine                | Groq API                               |
| Frontend                  | Streamlit                              |
| Environment Configuration | python-dotenv                          |

---

## 5. Repository Structure

```text
finla_AI_Friend(Repo)/
│
├── app.py
├── rag_pipeline.p_
```
