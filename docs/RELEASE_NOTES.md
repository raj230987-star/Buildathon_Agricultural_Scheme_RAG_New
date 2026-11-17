# AgriSathi AI – Release Notes

## Project

**Name:** AgriSathi AI  
**Version:** 0.1.0 – Development Baseline  
**Status:** Development

## 1. Project Overview

AgriSathi AI is an AI-powered Agricultural Government Schemes Assistant. It uses Retrieval-Augmented Generation (RAG) to answer questions using uploaded agricultural scheme PDF documents.

## 2. Implemented Features

The following features are available in the current development version:

- PDF document upload
- PDF text extraction
- Text chunking
- Hugging Face embedding generation
- FAISS vector database
- Semantic document retrieval
- OpenAI-based answer generation
- Source document and page references
- Duplicate PDF detection
- Conversation history for follow-up questions
- Streamlit frontend
- FastAPI backend

## 3. Current Knowledge Base

| Component | Current Status |
|---|---|
| Unique document contents | 3 |
| FAISS vectors | 95 |
| Metadata records | 95 |
| Embedding model | all-MiniLM-L6-v2 |
| Embedding dimension | 384 |
| Vector database | FAISS |

## 4. Planned Enhancements

The following features are planned and are not yet confirmed as implemented:

- Multilingual embedding support
- English, Tamil, Hindi, Kannada, Telugu, and Malayalam responses
- BM25 keyword retrieval
- Hybrid search using FAISS and BM25
- Reciprocal Rank Fusion (RRF)
- Improved evidence validation
- Farmer profile management
- Preliminary scheme eligibility guidance
- Government scheme explorer
- Scheme comparison
- Improved dashboard and user interface
- RAG evaluation framework
- Automated backend and retrieval tests

## 5. Data and Migration Notes

The existing FAISS database must be preserved before major changes.

Changing the embedding model requires rebuilding the complete vector index and corresponding metadata using the new model.

The original project folder should remain unchanged while development continues in the new project folder.

## 6. Known Development Considerations

- Retrieved passages may include content that is not directly cited in the generated answer.
- Citation relevance and evidence validation require further improvement.
- Multilingual retrieval needs evaluation before production use.
- Eligibility guidance must be presented as preliminary information, not official government approval.

## 7. Next Development Milestones

1. Complete project documentation.
2. Verify existing backend API routes.
3. Implement multilingual embedding support.
4. Implement BM25 keyword retrieval.
5. Combine retrieval using RRF.
6. Improve evidence validation and citations.
7. Add multilingual response support.
8. Develop farmer profile and eligibility guidance.
9. Redesign the Streamlit dashboard.
10. Implement RAG evaluation and automated testing.

## 8. Release Disclaimer

This is a development version intended for testing and improvement. Scheme details and eligibility conditions should always be checked against the latest official government notifications and guidelines.