
import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

from Backend.ingestion import split_text_into_chunks


DB_DIR = Path("faiss_db_multilingual")

INDEX_PATH = DB_DIR / "index.faiss"
METADATA_PATH = DB_DIR / "documents.json"

MODEL_NAME = "intfloat/multilingual-e5-small"
EMBEDDING_DIMENSION = 384

_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading multilingual E5 model...")
        _model = SentenceTransformer(MODEL_NAME, device="cpu")

    return _model


def add_document_to_multilingual_faiss(
    pages,
    original_filename,
    stored_filename
):
    """
    Append new PDF chunks to the existing multilingual FAISS database.
    Existing vectors and metadata are preserved.
    """

    chunks = split_text_into_chunks(pages)

    if not chunks:
        raise ValueError("No text chunks available for multilingual embedding.")

    DB_DIR.mkdir(parents=True, exist_ok=True)

    # Load existing index and metadata
    if INDEX_PATH.exists() and METADATA_PATH.exists():

        index = faiss.read_index(str(INDEX_PATH))

        with open(METADATA_PATH, "r", encoding="utf-8") as file:
            metadata = json.load(file)

        if index.d != EMBEDDING_DIMENSION:
            raise ValueError("Multilingual FAISS dimension mismatch.")

        if index.ntotal != len(metadata):
            raise ValueError("Multilingual FAISS index and metadata count mismatch.")

    elif not INDEX_PATH.exists() and not METADATA_PATH.exists():

        raise FileNotFoundError(
            "Multilingual database does not exist. "
            "Build it before adding new documents."
        )

    else:
        raise ValueError(
            "Multilingual FAISS index or metadata file is missing."
        )

    # Prepare E5 passage embeddings
    passages = [
        "passage: " + chunk["content"]
        for chunk in chunks
    ]

    model = get_model()

    embeddings = model.encode(
        passages,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=True
    ).astype("float32")

    if embeddings.shape != (len(chunks), EMBEDDING_DIMENSION):
        raise ValueError(
            f"Unexpected embedding shape: {embeddings.shape}"
        )

    # Prepare metadata
    new_metadata = []

    for chunk in chunks:
        new_metadata.append({
            "content": chunk["content"],
            "source": original_filename,
            "stored_filename": stored_filename,
            "page_number": chunk["page_number"],
            "start_index": chunk["start_index"]
        })

    # Append to existing database
    updated_metadata = metadata + new_metadata

    # Work on a copy so the in-memory original is unchanged
    updated_index = faiss.clone_index(index)
    updated_index.add(embeddings)

    if updated_index.ntotal != len(updated_metadata):
        raise ValueError("Updated index and metadata count mismatch.")

    # Save temporary files first
    temp_index = DB_DIR / "index_temp.faiss"
    temp_metadata = DB_DIR / "documents_temp.json"

    try:
        faiss.write_index(updated_index, str(temp_index))

        temp_metadata.write_text(
            json.dumps(updated_metadata, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        # Replace database files after successful preparation
        temp_index.replace(INDEX_PATH)
        temp_metadata.replace(METADATA_PATH)

    finally:
        if temp_index.exists():
            temp_index.unlink()

        if temp_metadata.exists():
            temp_metadata.unlink()

    return {
        "new_chunks": len(chunks),
        "total_vectors": updated_index.ntotal,
        "database_path": str(INDEX_PATH)
    }
