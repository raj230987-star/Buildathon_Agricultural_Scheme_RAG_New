
import hashlib
import json
from pathlib import Path
from uuid import uuid4
from typing import Literal

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field

from Backend.pdf_processor import extract_pdf_text
from Backend.ingestion import add_document_to_faiss
from Backend.multilingual_ingestion import (
    add_document_to_multilingual_faiss
)
from Backend.retrieval import search_documents
from Backend.query_translation import translate_query
from Backend.hybrid_retrieval import search_hybrid
from Backend.generation import (
    generate_answer,
    rewrite_question_for_retrieval
)


# --------------------------------------------------
# 1. FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="வேளாண்மை தோழன் AI - Agricultural Scheme Assistant",
    description="AI-powered Agricultural Government Schemes Assistant",
    version="1.2.0"
)


# --------------------------------------------------
# 2. FOLDER CONFIGURATION
# --------------------------------------------------

UPLOAD_DIR = Path("uploaded_pdfs")

DB_DIR = Path("faiss_db")

MULTILINGUAL_DB_DIR = Path("faiss_db_multilingual")

REGISTRY_PATH = DB_DIR / "uploaded_files.json"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)
MULTILINGUAL_DB_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 3. SHA-256 DUPLICATE DETECTION
# --------------------------------------------------

def calculate_sha256(file_content: bytes) -> str:
    return hashlib.sha256(file_content).hexdigest()


# --------------------------------------------------
# 4. DATABASE SNAPSHOT AND RESTORE
# --------------------------------------------------

DATABASE_FILES = [
    DB_DIR / "index.faiss",
    DB_DIR / "documents.json",
    MULTILINGUAL_DB_DIR / "index.faiss",
    MULTILINGUAL_DB_DIR / "documents.json",
    REGISTRY_PATH
]


def create_upload_snapshot():
    """
    Keep the previous database files in memory.
    This allows recovery if either ingestion operation fails.
    """

    snapshot = {}

    for path in DATABASE_FILES:

        if path.exists():
            snapshot[path] = path.read_bytes()
        else:
            snapshot[path] = None

    return snapshot


def restore_upload_snapshot(snapshot):
    """
    Restore all database files to their previous contents.
    """

    for path, content in snapshot.items():

        if content is None:

            if path.exists():
                path.unlink()

        else:

            path.parent.mkdir(parents=True, exist_ok=True)

            temp_path = path.with_name(path.name + ".rollback")

            temp_path.write_bytes(content)
            temp_path.replace(path)


# --------------------------------------------------
# 5. REQUEST MODELS
# --------------------------------------------------

class ConversationMessage(BaseModel):

    role: Literal["user", "assistant"]

    content: str


class SearchRequest(BaseModel):

    question: str

    top_k: int = Field(default=3, ge=1, le=10)


class AskRequest(BaseModel):

    question: str

    top_k: int = Field(default=5, ge=1, le=10)

    conversation_history: list[ConversationMessage] = Field(
        default_factory=list,
        max_length=10
    )


# --------------------------------------------------
# 6. HOME API
# --------------------------------------------------

@app.get("/")
async def root():

    return {
        "message": "Agricultural Scheme RAG API is running",
        "status": "success",
        "version": "1.2.0"
    }


# --------------------------------------------------
# 7. HEALTH CHECK API
# --------------------------------------------------

@app.get("/health")
async def health_check():

    return {
        "status": "healthy",
        "message": "Backend is working successfully"
    }


# --------------------------------------------------
# 8. PDF UPLOAD API - DUAL FAISS INDEXING
# --------------------------------------------------

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    stored_path = None

    database_snapshot = None

    ingestion_started = False

    try:

        # 1. Validate filename

        original_name = Path(file.filename or "").name

        if not original_name.lower().endswith(".pdf"):

            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )

        # 2. Read PDF content

        file_content = await file.read()

        if not file_content.startswith(b"%PDF-"):

            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file"
            )

        # 3. Calculate SHA-256

        file_hash = calculate_sha256(file_content)

        # 4. Read upload registry

        if REGISTRY_PATH.exists():

            with open(
                REGISTRY_PATH,
                "r",
                encoding="utf-8"
            ) as f:

                registry = json.load(f)

        else:

            registry = []

        # 5. Duplicate detection

        for document in registry:

            if document["sha256"] == file_hash:

                return {
                    "status": "duplicate",
                    "message": (
                        "This PDF has already been uploaded. "
                        "No duplicate vectors were added."
                    ),
                    "original_filename": original_name,
                    "existing_filename": document["original_filename"],
                    "stored_filename": document["stored_filename"],
                    "sha256": file_hash,
                    "vectors_added": 0
                }

        # 6. Save PDF

        stored_name = f"{uuid4().hex}_{original_name}"

        stored_path = UPLOAD_DIR / stored_name

        stored_path.write_bytes(file_content)

        # 7. Extract PDF text

        pages = extract_pdf_text(stored_path)

        total_characters = sum(
            len(page["content"]) for page in pages
        )

        if total_characters == 0:

            raise HTTPException(
                status_code=400,
                detail="No extractable text found in this PDF"
            )

        # 8. Create database snapshot before indexing

        database_snapshot = create_upload_snapshot()

        ingestion_started = True

        # 9. Add PDF to original FAISS database

        original_result = add_document_to_faiss(
            pages=pages,
            original_filename=original_name,
            stored_filename=stored_name
        )

        # 10. Add PDF to multilingual FAISS database

        multilingual_result = add_document_to_multilingual_faiss(
            pages=pages,
            original_filename=original_name,
            stored_filename=stored_name
        )

        # 11. Verify both databases have matching counts

        original_vectors = original_result["total_vectors"]

        multilingual_vectors = multilingual_result["total_vectors"]

        if original_vectors != multilingual_vectors:

            raise RuntimeError(
                "FAISS database vector counts do not match. "
                "Upload will be rolled back."
            )

        # 12. Update registry only after both indexing operations succeed

        registry.append({
            "sha256": file_hash,
            "original_filename": original_name,
            "stored_filename": stored_name
        })

        with open(
            REGISTRY_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                registry,
                f,
                ensure_ascii=False,
                indent=4
            )

        # 13. Success response

        return {
            "status": "success",
            "message": "PDF uploaded and indexed successfully in both databases",
            "original_filename": original_name,
            "stored_filename": stored_name,
            "sha256": file_hash,
            "total_pages": len(pages),
            "total_characters": total_characters,
            "total_chunks": original_result["total_chunks"],
            "original_faiss_vectors": original_vectors,
            "multilingual_faiss_vectors": multilingual_vectors,
            "original_database": str(DB_DIR / "index.faiss"),
            "multilingual_database": str(
                MULTILINGUAL_DB_DIR / "index.faiss"
            )
        }

    except HTTPException:

        if ingestion_started and database_snapshot is not None:

            try:
                restore_upload_snapshot(database_snapshot)

            except Exception as rollback_error:

                print("Database rollback error:", str(rollback_error))

        if stored_path and stored_path.exists():

            stored_path.unlink()

        raise

    except Exception as e:

        if ingestion_started and database_snapshot is not None:

            try:
                restore_upload_snapshot(database_snapshot)

                print("Database rollback completed.")

            except Exception as rollback_error:

                print("Database rollback error:", str(rollback_error))

        if stored_path and stored_path.exists():

            stored_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(e)}"
        )


# --------------------------------------------------
# 9. DOCUMENT SEARCH API
# --------------------------------------------------

@app.post("/search")
async def search(request: SearchRequest):

    try:

        results = search_documents(
            question=request.question,
            top_k=request.top_k
        )

        return {
            "status": "success",
            "question": request.question,
            "total_results": len(results),
            "results": results
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


# --------------------------------------------------
# 10. AI QUESTION ANSWERING WITH HYBRID RETRIEVAL
# --------------------------------------------------

@app.post("/ask")
async def ask_question(request: AskRequest):

    try:

        # 1. Convert conversation history

        conversation_history = [
            message.model_dump()
            for message in request.conversation_history
        ]

        # 2. Rewrite follow-up question

        search_question = rewrite_question_for_retrieval(
            question=request.question,
            conversation_history=conversation_history
        )

        # 3. Translate Tamil query into English if required

        translated_question = translate_query(search_question)

        print("\n========== AGRICULTURAL SCHEME RAG ==========")

        print("Original question:", request.question)

        print("Rewritten question:", search_question)

        print("Translated search query:", translated_question)

        # 4. Hybrid retrieval: FAISS + BM25 + RRF

        results = search_hybrid(
            question=translated_question,
            top_k=request.top_k,
            candidate_k=25
        )

        print("Retrieved documents:", len(results))

        # 5. Generate answer using retrieved PDF evidence

        answer = generate_answer(
            question=request.question,
            retrieved_documents=results,
            conversation_history=conversation_history
        )

        # 6. Prepare PDF source citations

        sources = []

        for document in results:

            sources.append({
                "source": document.get("source"),
                "page_number": document.get("page_number"),
                "rrf_score": document.get("rrf_score"),
                "faiss_rank": document.get("faiss_rank"),
                "bm25_rank": document.get("bm25_rank")
            })

        # 7. Return response

        return {
            "status": "success",
            "question": request.question,
            "search_question": search_question,
            "translated_search_question": translated_question,
            "retrieval_method": "FAISS + BM25 + RRF",
            "total_results": len(results),
            "answer": answer,
            "sources": sources
        }

    except Exception as e:

        print("Question answering error:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Question answering failed: {str(e)}"
        )
