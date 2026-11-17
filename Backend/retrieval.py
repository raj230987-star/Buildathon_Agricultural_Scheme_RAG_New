
import json
from pathlib import Path

import faiss

from Backend.embedding import generate_embeddings


# FAISS database files
DB_DIR = Path("faiss_db")
INDEX_PATH = DB_DIR / "index.faiss"
METADATA_PATH = DB_DIR / "documents.json"


def search_documents(question, top_k=3):
    """
    Search the FAISS database using a user question.

    Returns the most relevant PDF text chunks,
    source filename, page number and similarity score.
    """

    # STEP 1: Validate question
    if not question or not question.strip():
        raise ValueError("Please enter a valid question")

    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    # STEP 2: Check database files
    if not INDEX_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError("FAISS database files not found")

    # STEP 3: Load FAISS index
    index = faiss.read_index(str(INDEX_PATH))

    # STEP 4: Load document metadata
    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    if index.ntotal != len(metadata):
        raise ValueError("FAISS index and metadata count mismatch")

    if index.ntotal == 0:
        return []

    # STEP 5: Convert question into embedding
    query_embedding = generate_embeddings([question])

    # STEP 6: Search FAISS for similar vectors
    search_count = min(top_k, index.ntotal)

    scores, indices = index.search(
        query_embedding,
        search_count
    )

    # STEP 7: Prepare search results
    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx < 0:
            continue

        document = metadata[int(idx)]

        results.append({
            "content": document["content"],
            "source": document["source"],
            "page_number": document["page_number"],
            "similarity_score": round(float(score), 4)
        })

    return results
