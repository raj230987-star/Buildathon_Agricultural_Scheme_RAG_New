# வேளாண்மை தோழன் AI – Database Design

## 1. Overview

வேளாண்மை தோழன் AI uses two FAISS vector databases, JSON metadata files, and an uploaded-file registry to manage agricultural government scheme PDF documents.

The application supports:
- Semantic retrieval using FAISS.
- Multilingual semantic retrieval using multilingual E5 embeddings.
- Keyword retrieval using BM25.
- Hybrid ranking using Reciprocal Rank Fusion (RRF).

BM25 is constructed dynamically from the multilingual metadata file. It is not maintained as a separate persistent database.

## 2. Current Storage Structure

```text
Agricultural_Scheme_RAG_New/
│
├── faiss_db/
│   ├── index.faiss
│   ├── documents.json
│   └── uploaded_files.json
│
├── faiss_db_multilingual/
│   ├── index.faiss
│   └── documents.json
│
├── faiss_db_backup/
│   ├── index.faiss
│   └── documents.json
│
├── faiss_db_safety_backup/
│   ├── index.faiss
│   └── documents.json
│
├── uploaded_pdfs/
│
└── Backend/
    ├── embedding.py
    ├── ingestion.py
    ├── multilingual_ingestion.py
    ├── multilingual_retrieval.py
    ├── bm25_retrieval.py
    └── hybrid_retrieval.py
```

## 3. Storage Components

### 3.1 Original FAISS Database

**Location:** `faiss_db/`

Files:
- `index.faiss`
- `documents.json`

Purpose:
- Stores semantic vector embeddings.
- Supports similarity-based document retrieval.
- Maintains associated document metadata.

Embedding configuration:

| Parameter | Value |
|---|---|
| Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector dimension | 384 |
| Current vectors | 135 |
| Metadata records | 135 |

Implementation: `Backend/embedding.py`

### 3.2 Multilingual FAISS Database

**Location:** `faiss_db_multilingual/`

Files:
- `index.faiss`
- `documents.json`

Purpose:
- Stores multilingual semantic embeddings.
- Supports cross-language semantic retrieval.
- Provides document chunks for hybrid search.

Embedding configuration:

| Parameter | Value |
|---|---|
| Model | `intfloat/multilingual-e5-small` |
| Vector dimension | 384 |
| Current vectors | 135 |
| Metadata records | 135 |
| Execution device | CPU |

Implementation: `Backend/multilingual_ingestion.py`

The E5 model uses the `passage:` prefix when generating document embeddings. Query embeddings use the corresponding query prefix in the retrieval implementation.

### 3.3 Document Metadata

Each database maintains a corresponding `documents.json` file.

The multilingual ingestion implementation stores these fields:

| Field | Description |
|---|---|
| `content` | Extracted text chunk |
| `source` | Original PDF filename |
| `stored_filename` | Stored PDF filename |
| `page_number` | Source PDF page number |
| `start_index` | Starting character position of the chunk |

Metadata is used to retrieve source information and page references for answer citations.

The metadata format should remain compatible with its corresponding FAISS index.

### 3.4 Uploaded File Registry

**File:** `faiss_db/uploaded_files.json`

Purpose:
- Tracks uploaded PDF files.
- Supports duplicate document detection.
- Uses SHA-256 file hashes to identify duplicate uploads.

The registry is maintained by the FastAPI upload endpoint.

### 3.5 Uploaded PDF Documents

**Folder:** `uploaded_pdfs/`

Purpose:
- Stores uploaded source PDF files.
- Preserves original documents for reference.
- Provides source documents for processing.

Currently verified: 11 PDF files.

### 3.6 Backup Databases

Backup folders:

- `faiss_db_backup/`
- `faiss_db_safety_backup/`

Purpose:
- Preserve earlier database versions.
- Provide recovery points before major database changes.
- Protect existing vector indexes and metadata.

These backups must not be treated as the active databases.

## 4. Hybrid Retrieval Storage

The application combines semantic and keyword retrieval.

### 4.1 FAISS Semantic Search

FAISS retrieves relevant document chunks using vector similarity.

The application uses the multilingual FAISS database for the hybrid retrieval workflow.

### 4.2 BM25 Keyword Search

Implementation: `Backend/bm25_retrieval.py`

BM25:
1. Reads `faiss_db_multilingual/documents.json`.
2. Tokenizes document content.
3. Builds a BM25 index using `BM25Okapi`.
4. Calculates keyword relevance scores for the user query.
5. Returns the highest-ranked document chunks.

**Storage method:** BM25 is built in memory during search. A separate BM25 index file is not currently persisted.

### 4.3 Reciprocal Rank Fusion (RRF)

Implementation: `Backend/hybrid_retrieval.py`

RRF combines the ranked results from:
- FAISS semantic search.
- BM25 keyword search.

The combined ranking helps retrieve relevant passages using both semantic similarity and keyword relevance.

RRF scores and retrieval ranks are calculated during retrieval; they are not stored as a separate database.

## 5. Document Processing and Storage Flow

1. User uploads a PDF through the Streamlit interface.
2. FastAPI validates the PDF file.
3. SHA-256 hash is calculated for duplicate detection.
4. PDF text and page information are extracted.
5. Extracted text is split into document chunks.
6. Original FAISS embeddings are generated.
7. Multilingual E5 embeddings are generated.
8. Both FAISS indexes and their metadata files are updated.
9. Vector and metadata counts are checked.
10. The uploaded-file registry is updated after successful processing.

The upload workflow also creates temporary snapshots of the active database files before indexing. If processing fails, the application attempts to restore the previous files.

## 6. Database Integrity Checks

The following checks are used to verify database consistency:

- FAISS index files can be loaded.
- Vector counts match metadata record counts.
- Embedding dimensions match the configured models.
- Document source and page references are available.
- Duplicate PDF uploads are detected.
- Original and multilingual database vector counts match after successful uploads.
- Backup files are preserved before major changes.

## 7. Backup and Recovery

Before changing an embedding model or rebuilding a database:

1. Stop the backend application.
2. Preserve the active FAISS index and metadata files.
3. Keep the uploaded source PDFs.
4. Generate embeddings using the intended model.
5. Rebuild the corresponding index and metadata together.
6. Verify vector counts and dimensions.
7. Test retrieval before using the rebuilt database.

**Important:** Do not mix embeddings generated by different models in the same FAISS index. Each database must use its own configured embedding model.

The existing `Backend/rebuild_database.py` rebuilds the original FAISS database. It should not be assumed to rebuild the multilingual database.

## 8. Current Database Verification

Verified database status:

| Item | Original FAISS | Multilingual FAISS |
|---|---:|---:|
| Embedding model | all-MiniLM-L6-v2 | multilingual-e5-small |
| Vector dimension | 384 | 384 |
| FAISS vectors | 135 | 135 |
| Metadata records | 135 | 135 |
| Index and metadata counts | Match | Match |

Additional verification:

| Item | Verified status |
|---|---|
| Upload registry | Available |
| Uploaded PDF files | 11 |
| BM25 implementation | Available |
