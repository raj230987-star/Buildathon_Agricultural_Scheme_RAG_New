
import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

DB_DIR = Path("faiss_db_multilingual")

INDEX_PATH = DB_DIR / "index.faiss"
METADATA_PATH = DB_DIR / "documents.json"

MODEL_NAME = "intfloat/multilingual-e5-small"

_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading multilingual E5 model...")
        _model = SentenceTransformer(MODEL_NAME, device="cpu")

    return _model


def search_multilingual(question, top_k=5):

    if not question or not question.strip():
        raise ValueError("Please enter a valid question.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if not INDEX_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError("Multilingual FAISS database not found.")

    index = faiss.read_index(str(INDEX_PATH))

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        documents = json.load(file)

    if index.ntotal != len(documents):
        raise ValueError("FAISS index and metadata count mismatch.")

    if index.ntotal == 0:
        return []

    model = get_model()

    query_embedding = model.encode(
        ["query: " + question.strip()],
        normalize_embeddings=True,
        convert_to_numpy=True
    ).astype("float32")

    search_count = min(top_k, index.ntotal)

    scores, indices = index.search(
        query_embedding,
        search_count
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx < 0:
            continue

        document = documents[int(idx)]

        results.append({
            "content": document["content"],
            "source": document["source"],
            "page_number": document["page_number"],
            "similarity_score": round(float(score), 4)
        })

    return results
