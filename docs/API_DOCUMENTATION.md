# வேளாண்மை தோழன் AI – API Documentation

## 1. Overview

வேளாண்மை தோழன் AI uses FastAPI to provide backend services to the Streamlit frontend.

The backend handles PDF uploads, document indexing, semantic search, hybrid retrieval, and AI-powered agricultural government scheme question answering.

**API Version:** 1.2.0

## 2. Backend Configuration

| Item | Configuration |
|---|---|
| Framework | FastAPI |
| ASGI Server | Uvicorn |
| Backend Package | Backend |
| Main Application | Backend/main.py |
| Development Command | `python -m uvicorn Backend.main:app --reload` |
| Swagger Documentation | `/docs` |
| Alternative Documentation | `/redoc` |

## 3. API Endpoint Inventory

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Application information |
| `/health` | GET | Backend health check |
| `/upload-pdf` | POST | Upload and index PDF |
| `/search` | POST | Search document passages |
| `/ask` | POST | AI question answering using hybrid retrieval |

Base URL for local development:

`http://127.0.0.1:8000`

## 4. Home API

**Endpoint:** `GET /`

**Purpose:** Returns application information and API status.

### Example Response

```json
{
  "message": "Agricultural Scheme RAG API is running",
  "status": "success",
  "version": "1.2.0"
}
```

## 5. Health Check API

**Endpoint:** `GET /health`

**Purpose:** Checks whether the backend is running.

### Example Response

```json
{
  "status": "healthy",
  "message": "Backend is working successfully"
}
```

## 6. PDF Upload API

**Endpoint:** `POST /upload-pdf`

**Purpose:** Uploads an agricultural government scheme PDF and indexes it in both FAISS databases.

### Request

Content type: `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | PDF file | Yes | Agricultural scheme document |

### Processing Workflow

1. Validate the PDF filename and extension.
2. Validate the PDF file signature.
3. Calculate the SHA-256 hash.
4. Check the upload registry for duplicate content.
5. Save the PDF in `uploaded_pdfs`.
6. Extract text and page information.
7. Generate document chunks and embeddings.
8. Update the original FAISS database.
9. Update the multilingual FAISS database.
10. Verify that both databases have matching vector counts.
11. Update the upload registry after successful indexing.

### Example Success Response

```json
{
  "status": "success",
  "message": "PDF uploaded and indexed successfully in both databases",
  "original_filename": "Agricultural_Scheme.pdf",
  "stored_filename": "generated_id_Agricultural_Scheme.pdf",
  "sha256": "calculated_file_hash",
  "total_pages": 5,
  "total_characters": 3747,
  "total_chunks": 11,
  "original_faiss_vectors": 117,
  "multilingual_faiss_vectors": 117,
  "original_database": "faiss_db/index.faiss",
  "multilingual_database": "faiss_db_multilingual/index.faiss"
}
```

*Note: The values above are illustrative. Actual values depend on the uploaded PDF and current database contents.*

### Duplicate Upload Response

```json
{
  "status": "duplicate",
  "message": "This PDF has already been uploaded. No duplicate vectors were added.",
  "original_filename": "Agricultural_Scheme.pdf",
  "existing_filename": "Agricultural_Scheme.pdf",
  "stored_filename": "existing_stored_filename.pdf",
  "sha256": "calculated_file_hash",
  "vectors_added": 0
}
```

### Error Responses

| HTTP Status | Condition |
|---|---|
| 400 | File extension is not PDF |
| 400 | Invalid PDF file signature |
| 400 | No extractable text found |
| 500 | PDF processing or indexing failure |

The upload workflow includes a database snapshot and rollback attempt if indexing fails.

## 7. Document Search API

**Endpoint:** `POST /search`

**Purpose:** Retrieves relevant passages using the original semantic search implementation.

### Request Body

```json
{
  "question": "What is the subsidy available for agricultural machinery?",
  "top_k": 3
}
```

### Request Parameters

| Field | Type | Default | Validation |
|---|---|---|---|
| `question` | String | Required | User search question |
| `top_k` | Integer | 3 | Minimum 1, maximum 10 |

### Example Response Structure

```json
{
  "status": "success",
  "question": "What is the subsidy available for agricultural machinery?",
  "total_results": 3,
  "results": [
    {
      "source": "Agricultural_Scheme.pdf",
      "page_number": 1,
      "content": "Retrieved document passage"
    }
  ]
}
```

The `results` array contains the retrieved document records. Actual result fields depend on the retrieval implementation.

### Error Response

HTTP 500 is returned if document search fails.

## 8. AI Question Answering API

**Endpoint:** `POST /ask`

**Purpose:** Generates answers using conversation context, multilingual query processing, hybrid retrieval, and evidence validation.

### Request Body – English

```json
{
  "question": "What is the objective of the agricultural mechanization scheme?",
  "top_k": 5,
  "conversation_history": []
}
```

### Request Body – Tamil

```json
{
  "question": "வேளாண்மை இயந்திரமயமாக்கல் திட்டத்தின் நோக்கம் என்ன?",
  "top_k": 5,
  "conversation_history": []
}
```

### Request Parameters

| Field | Type | Default | Validation |
|---|---|---|---|
| `question` | String | Required | User question |
| `top_k` | Integer | 5 | Minimum 1, maximum 10 |
| `conversation_history` | Array | Empty list | Maximum 10 messages |

Each conversation history message contains:

| Field | Type | Allowed Values |
|---|---|---|
| `role` | String | `user` or `assistant` |
| `content` | String | Message content |

### Question Answering Workflow

1. Receive the question and conversation history.
2. Rewrite follow-up questions using conversation context.
3. Translate Tamil queries into English for retrieval when required.
4. Search using multilingual FAISS and BM25.
5. Combine retrieval rankings using RRF.
6. Generate an initial answer using retrieved PDF evidence.
7. Validate the answer against the retrieved evidence.
8. Return the final answer with source citations and retrieval information.

### Example Response Structure

```json
{
  "status": "success",
  "question": "What is the objective of the agricultural mechanization scheme?",
  "search_question": "What is the objective of the agricultural mechanization scheme?",
  "translated_search_question": "What is the objective of the agricultural mechanization scheme?",
  "retrieval_method": "FAISS + BM25 + RRF",
  "total_results": 3,
  "answer": "The scheme aims to promote farm mechanization among farmers.",
  "sources": [
    {
      "source": "Sub Mission on Agricultural Mechanization.pdf",
      "page_number": 1,
      "rrf_score": 0.03,
      "faiss_rank": 1,
      "bm25_rank": 2
    }
  ]
}
```

*Note: The answer, translated query, result count, scores, and source records vary according to the question and retrieved documents. The example illustrates the response structure.*

### Error Response

HTTP 500 is returned if question answering fails.

## 9. Error Handling

The API handles the following conditions:

- Invalid PDF filename or format
- Invalid PDF file signature
- PDF containing no extractable text
- Duplicate PDF upload
- PDF processing and indexing failures
- Search failures
- Question answering failures
- Invalid request data through FastAPI/Pydantic validation

## 10. API Testing

FastAPI provides an interactive Swagger interface.

### Testing Procedure

1. Start the backend:

```cmd
python -m uvicorn Backend.main:app --reload
```

2. Open Swagger documentation:

`http://127.0.0.1:8000/docs`

3. Select an API endpoint.
4. Click **Try it out**.
5. Enter the request parameters or upload a PDF.
6. Click **Execute**.
7. Review the response body and HTTP status code.

## 11. Important Notes

- `/search` uses the original semantic retrieval implementation.
- `/ask` uses hybrid retrieval with multilingual FAISS, BM25, and RRF.
- Tamil queries are translated for retrieval; the final response supports Tamil.
- The answer-generation module performs an AI-based evidence review.
- Source citations include document names and page references where available.
- Evidence validation does not guarantee that every generated claim is factually correct.

## 12. Documentation Status

The endpoint paths, request models, processing workflow, and response structures documented here are based on the implemented FastAPI routes in `Backend/main.py`.