# 🌾 வேளாண்மை தோழன் AI
### உங்கள் விவசாயத்திற்கு அறிவார்ந்த துணை!

**AI-Powered Agricultural Government Schemes Assistant**

An intelligent Retrieval-Augmented Generation (RAG) application designed to help users access information about Tamil Nadu, Kerala, Karnataka and Central Government agricultural schemes through uploaded PDF documents.

The application combines multilingual embeddings, hybrid search, FAISS vector databases, BM25 keyword retrieval, Reciprocal Rank Fusion (RRF), and OpenAI-powered answer generation.

---

## 1. Project Overview

வேளாண்மை தோழன் AI is a document-based agricultural government scheme assistant.

Users can upload agricultural scheme PDFs, ask questions in English or Tamil, receive AI-generated answers and view supporting PDF citations with page references.

The system uses Retrieval-Augmented Generation (RAG) to generate answers based on retrieved document content.

### Key Features

- **PDF Document Upload:** Upload agricultural government scheme PDFs.
- **PDF Text Extraction:** Extract document text and page numbers.
- **Document Chunking:** Split extracted text into searchable chunks.
- **Multilingual Embeddings:** Use Hugging Face multilingual E5 embeddings.
- **Dual FAISS Databases:** Maintain original and multilingual vector indexes.
- **Hybrid Retrieval:** Combine semantic search and BM25 keyword search.
- **Reciprocal Rank Fusion:** Combine retrieval results using RRF.
- **Tamil Query Translation:** Translate Tamil queries for improved retrieval from English documents.
- **AI Answer Generation:** Generate contextual answers using the OpenAI API.
- **Evidence Validation:** Perform a second AI-based review of answers against retrieved PDF context.
- **Source Citations:** Display PDF filenames and page references.
- **Duplicate Detection:** Identify duplicate PDFs using SHA-256 hashing.
- **Conversation History:** Support context-aware follow-up questions.
- **REST API:** Backend services using FastAPI.
- **Interactive Dashboard:** User interface developed using Streamlit.

---

## 2. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.13 |
| Frontend | Streamlit |
| Backend | FastAPI |
| API Server | Uvicorn |
| PDF Processing | PyPDF |
| Text Chunking | LangChain Text Splitters |
| Embedding Model | intfloat/multilingual-e5-small |
| Embedding Framework | Sentence Transformers |
| Vector Database | FAISS |
| Keyword Retrieval | BM25 |
| Hybrid Ranking | Reciprocal Rank Fusion (RRF) |
| AI Answer Generation | OpenAI API |
| HTTP Communication | Requests |
| Environment Configuration | Python Dotenv |

---

## 3. System Architecture

The application consists of two primary workflows.

### A. Document Ingestion Pipeline

1. User uploads an agricultural scheme PDF through Streamlit.
2. FastAPI receives and validates the PDF.
3. SHA-256 hashing checks for duplicate documents.
4. PyPDF extracts text and page numbers.
5. LangChain Text Splitters divide the extracted text into chunks.
6. Sentence Transformers generate multilingual embeddings.
7. Document embeddings are stored in the FAISS databases.
8. Document chunks and metadata are saved in JSON files.
9. The upload registry is updated after successful processing.

### B. Hybrid Retrieval and Question Answering Pipeline

1. User enters a question through the Streamlit interface.
2. Conversation history is considered for follow-up questions.
3. The question is rewritten into a standalone search query when necessary.
4. Tamil queries are translated into English for retrieval.
5. Multilingual FAISS performs semantic retrieval.
6. BM25 performs keyword-based retrieval.
7. Reciprocal Rank Fusion combines the retrieval results.
8. Relevant document chunks are passed to the answer-generation module.
9. OpenAI generates an answer using the retrieved PDF context.
10. A second AI-based validation step checks the generated answer against the available evidence.
11. The answer and supporting PDF references are displayed in Streamlit.

### Architecture Flow

```text
             USER
               |
               v
       STREAMLIT FRONTEND
               |
               v
         FASTAPI BACKEND
               |
       +-------+--------+
       |                |
       v                v
  PDF UPLOAD        USER QUERY
       |                |
       v                v
  PDF EXTRACTION    QUERY REWRITING
       |                |
       v                v
  TEXT CHUNKING     QUERY TRANSLATION
       |                |
       v                v
  MULTILINGUAL       HYBRID SEARCH
  EMBEDDINGS              |
       |          +------+------+
       v          |             |
  FAISS DATABASE  v             v
                 FAISS         BM25
                   |             |
                   +------+------+
                          |
                          v
                     RRF RANKING
                          |
                          v
                  RETRIEVED CONTEXT
                          |
                          v
                  OPENAI GENERATION
                          |
                          v
                  EVIDENCE VALIDATION
                          |
                          v
                  ANSWER + CITATIONS
```

---

## 4. Project Folder Structure

```text
Agricultural_Scheme_RAG_New/
|
|-- Backend/
|   |-- __init__.py
|   |-- main.py
|   |-- pdf_processor.py
|   |-- embedding.py
|   |-- ingestion.py
|   |-- retrieval.py
|   |-- generation.py
|   |-- rebuild_database.py
|   |-- bm25_retrieval.py
|   |-- hybrid_retrieval.py
|   |-- build_multilingual_index.py
|   |-- multilingual_retrieval.py
|   |-- multilingual_ingestion.py
|   |-- query_translation.py
|
|-- Frontend/
|   |-- app.py
|
|-- faiss_db/
|   |-- index.faiss
|   |-- documents.json
|   |-- uploaded_files.json
|
|-- faiss_db_multilingual/
|   |-- index.faiss
|   |-- documents.json
|
|-- uploaded_pdfs/
|
|-- evaluation/
|
|-- tests/
|
|-- docs/
|
|-- .env
|-- .gitignore
|-- requirements.txt
|-- README.md
```

*Note: This is the main application structure. Backup databases and virtual-environment files are not shown.*

### Important Backend Modules

| Module | Responsibility |
|---|---|
| main.py | FastAPI application and API endpoints |
| pdf_processor.py | PDF text extraction |
| embedding.py | Embedding generation |
| ingestion.py | Original FAISS ingestion |
| retrieval.py | Original semantic retrieval |
| multilingual_ingestion.py | Multilingual FAISS ingestion |
| multilingual_retrieval.py | Multilingual semantic retrieval |
| bm25_retrieval.py | BM25 keyword retrieval |
| hybrid_retrieval.py | Hybrid search and RRF ranking |
| query_translation.py | Tamil query translation |
| generation.py | Answer generation, query rewriting and evidence validation |
| rebuild_database.py | Rebuild the original FAISS database |

---

## 5. Installation and Setup

### Prerequisites

- Python 3.13
- Visual Studio Code
- Git
- OpenAI API key
- Internet connection for dependency installation and model download

### Step 1: Clone the Repository

```cmd
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project directory:

```cmd
cd Agricultural_Scheme_RAG_New
```

### Step 2: Create a Virtual Environment

```cmd
python -m venv venv
```

Activate the environment using Windows CMD:

```cmd
venv\Scripts\activate.bat
```

### Step 3: Install Dependencies

```cmd
python -m pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root directory.

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=your_supported_openai_model
```

Replace the placeholder values with your actual credentials and configured model.

**Security:** Never upload `.env` or expose your API key on GitHub.

---

## 6. Run the Application

The application requires two separate CMD terminals.

### Terminal 1: Start FastAPI Backend

Navigate to the project folder and activate the virtual environment.

Run:

```cmd
python -m uvicorn Backend.main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

FastAPI Swagger documentation:

`http://127.0.0.1:8000/docs`

Health check:

`http://127.0.0.1:8000/health`

### Terminal 2: Start Streamlit Frontend

Activate the same virtual environment in another CMD terminal.

Run:

```cmd
python -m streamlit run Frontend/app.py
```

Frontend URL:

`http://localhost:8501`

---

## 7. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend welcome/status |
| GET | `/health` | Backend health check |
| POST | `/upload-pdf` | Upload and process PDF |
| POST | `/search` | Search relevant PDF passages |
| POST | `/ask` | AI-powered question answering |

For request and response details, visit:

`http://127.0.0.1:8000/docs`

---

## 8. Database Management

The application maintains two FAISS databases.

### Original FAISS Database

Location: `faiss_db/`

- `index.faiss` – Stores vector embeddings.
- `documents.json` – Stores document chunks and metadata.
- `uploaded_files.json` – Tracks uploaded documents and SHA-256 hashes.

### Multilingual FAISS Database

Location: `faiss_db_multilingual/`

- `index.faiss` – Stores multilingual vector embeddings.
- `documents.json` – Stores multilingual-index document chunks and metadata.

### Database Rebuild

The original database can be rebuilt using:

```cmd
python -m Backend.rebuild_database
```

**Important:** Back up the existing database before rebuilding. This command rebuilds the original FAISS index; do not assume it also rebuilds the multilingual database.

---

## 9. Example Questions

### English

- What is the main objective of the Sub Mission on Agricultural Mechanization?
- What subsidy is available for agricultural machinery?
- Who are the eligible beneficiaries?
- What are the benefits of the Seed Village Scheme?

### Tamil

- வேளாண் இயந்திரமயமாக்கல் திட்டத்தின் முக்கிய நோக்கம் என்ன?
- விவசாய இயந்திரங்களுக்கு என்ன மானியம் வழங்கப்படுகிறது?
- சிறு மற்றும் குறு விவசாயிகளுக்கான திட்டங்கள் என்ன?

The application retrieves relevant information from uploaded PDFs and provides supporting source references.

---

## 10. Duplicate PDF Detection

The application calculates a SHA-256 hash for each uploaded PDF.

When identical PDF content is uploaded again:

- The duplicate document is identified.
- Existing database entries are retained.
- No additional FAISS vectors are created.
- A duplicate notification is displayed to the user.

This prevents unnecessary duplicate document ingestion.

---

## 11. Testing and Validation

The following application functions have been tested:

| Test Case | Result |
|---|---|
| FastAPI health check | Passed |
| Streamlit dashboard | Passed |
| English question answering | Passed |
| Tamil question answering | Passed |
| PDF source citations | Passed |
| PDF upload and processing | Passed |
| Original FAISS update | Passed |
| Multilingual FAISS update | Passed |
| Duplicate PDF detection | Passed |
| Vector count verification | Passed |

Testing was performed using the uploaded agricultural scheme PDF documents.

These tests confirm the tested workflows, not universal accuracy for every possible scheme question.

---

## 12. Limitations and Important Notes

- Answers depend on the content and quality of uploaded PDF documents.
- The available document collection may not contain every government scheme or eligibility condition.
- Tamil query translation supports retrieval from English-language documents; it does not mean all source PDFs contain Tamil explanations.
- Evidence validation is an AI-based review and is not a formal guarantee that every generated statement is correct.
- Always verify subsidy amounts, eligibility criteria, application procedures and scheme conditions against the latest official government notifications.
- The application does not provide official government eligibility approval.
- OpenAI API usage may incur charges.

---

## 13. Future Enhancements

Potential future improvements include:

- Farmer profile-based preliminary eligibility guidance.
- Scheme comparison.
- Additional Indian language support.
- Improved retrieval accuracy.
- Advanced RAG evaluation.
- Downloadable reports.
- Mobile application integration.
- Cloud deployment.

These are proposed enhancements and are not represented as completed features.

---

## 14. Author and Project Information

**Project Name:** வேளாண்மை தோழன் AI

**Tagline:** உங்கள் விவசாயத்திற்கு அறிவார்ந்த துணை!

**Project Domain:** Agriculture | Government Schemes | Generative AI | Retrieval-Augmented Generation

**Technologies:** Python | Streamlit | FastAPI | FAISS | Hugging Face | BM25 | OpenAI API

**Project Type:** AI-Powered Document-Based Question Answering System

---

*வேளாண்மை தோழன் AI demonstrates the practical application of Retrieval-Augmented Generation to make agricultural government scheme information more accessible through document-based AI assistance.*
