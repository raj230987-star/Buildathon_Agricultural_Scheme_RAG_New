import json
import re
from pathlib import Path
from rank_bm25 import BM25Okapi

DB_DIR = Path("faiss_db_multilingual")
METADATA_PATH = DB_DIR / "documents.json"


def tokenize(text):
    return re.findall(r"\w+", text.lower(), flags=re.UNICODE)


def search_bm25(question, top_k=5):
    if not question or not question.strip():
        raise ValueError("Please enter a valid question.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if not METADATA_PATH.exists():
        raise FileNotFoundError("Multilingual database metadata not found.")

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        documents = json.load(file)

    if not documents:
        return []

    tokenized_documents = [
        tokenize(doc.get("content", "")) for doc in documents
    ]

    bm25 = BM25Okapi(tokenized_documents)
    tokenized_query = tokenize(question)

    if not tokenized_query:
        return []

    scores = bm25.get_scores(tokenized_query)

    top_indices = sorted(
        range(len(scores)),
        key=lambda index: scores[index],
        reverse=True
    )[:top_k]

    results = []

    for index in top_indices:
        document = documents[index]

        results.append({
            "content": document.get("content", ""),
            "source": document.get("source", "Unknown"),
            "page_number": document.get("page_number"),
            "bm25_score": round(float(scores[index]), 4)
        })

    return results