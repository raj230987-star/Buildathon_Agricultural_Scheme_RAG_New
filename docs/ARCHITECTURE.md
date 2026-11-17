# வேளாண்மை தோழன் AI – System Architecture

## 1. Project Overview

வேளாண்மை தோழன் AI is an AI-powered Agricultural Government Schemes Assistant.

The application uses Retrieval-Augmented Generation (RAG) to answer agricultural government scheme questions using information extracted from PDF documents.

It supports English and Tamil queries, hybrid document retrieval, context-aware question answering, evidence validation, and source citations.

## 2. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.13 |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Language Model | OpenAI API |
| Embedding Model | intfloat/multilingual-e5-small |
| Original Vector Database | FAISS |
| Multilingual Vector Database | FAISS |
| Keyword Retrieval | BM25 |
| Search Ranking | Reciprocal Rank Fusion (RRF) |
| PDF Processing | PyPDF |
| Text Chunking | LangChain Text Splitter |
| Query Translation | OpenAI API |
| Environment Configuration | Python dotenv |

## 3. High-Level System Architecture

```text
                   FARMER / USER
                         |
                         v
                 STREAMLIT FRONTEND
                         |
                         v
                   FASTAPI BACKEND
                         |
                         v
                  QUERY PROCESSING
                         |
              +----------+----------+
              |                     |
              v                     v
        QUERY REWRITING       TAMIL TRANSLATION
        Conversation          Tamil to English
        Context               for Retrieval
              |                     |
              +----------+----------+
                         |
                         v
                  HYBRID RETRIEVAL
                         |
               +---------+---------+
               |                   |
               v                   v
          FAISS SEARCH          BM25 SEARCH
        Multilingual Index     Keyword Matching
               |                   |
               +---------+---------+
                         |
                         v
                    RRF RANKING
                         |
                         v
                RETRIEVED DOCUMENTS
                         |
                         v
                 OPENAI GENERATION
                         |
                         v
                 INITIAL ANSWER
                         |
                         v
                EVIDENCE VALIDATION
                         |
                         v
                 FINAL RESPONSE
                         |
                         v
                ANSWER WITH CITATIONS
```

## 4. PDF Knowledge Base Pipeline

The document ingestion process follows these steps:

1. User uploads an agricultural government scheme PDF.
2. FastAPI validates the uploaded PDF.
3. SHA-256 hashing is used to detect duplicate documents.
4. PyPDF extracts text and page information.
5. LangChain Text Splitter divides extracted text into smaller chunks.
6. Sentence Transformers generates embeddings.
7. Document chunks are stored in the original FAISS database.
8. The same document chunks are indexed in the multilingual FAISS database.
9. BM25 uses the multilingual database's document metadata for keyword retrieval.
10. The upload registry records successfully processed documents.

## 5. Dual FAISS Database Design

The application maintains two FAISS databases.

| Database | Purpose |
|---|---|
| `faiss_db` | Original document embedding and semantic search |
| `faiss_db_multilingual` | Multilingual embedding and retrieval using multilingual-e5-small |

Each database maintains its own vector index and document metadata.

The PDF upload workflow updates both databases and checks that their vector counts match.

## 6. Hybrid Retrieval Architecture

The application combines semantic search and keyword search.

### FAISS Semantic Search

- Uses multilingual-e5-small embeddings.
- Retrieves semantically related document passages.
- Supports cross-language similarity between Tamil and English queries.

### BM25 Keyword Search

-