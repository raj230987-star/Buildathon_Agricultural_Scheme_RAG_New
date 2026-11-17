
import json
import re

from Backend.multilingual_retrieval import search_multilingual
from Backend.bm25_retrieval import search_bm25

RRF_K = 60

# Small ranking bonus for exact phrase matches
EXACT_PHRASE_BONUS = 0.005


def get_document_key(document):
    return (
        document.get("source"),
        document.get("page_number"),
        document.get("content")
    )


def normalize_text(text):
    """Normalize text for case-insensitive phrase matching."""
    text = text.casefold()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def get_search_phrases(question):
    """
    Use quoted phrases when available.
    Otherwise, use the complete query as the exact phrase.
    """
    quoted_phrases = re.findall(
        r'["“”]([^"“”]+)["“”]',
        question
    )

    if quoted_phrases:
        return [
            normalize_text(phrase)
            for phrase in quoted_phrases
            if normalize_text(phrase)
        ]

    normalized_question = normalize_text(question)

    return [normalized_question] if normalized_question else []


def has_exact_phrase_match(question, document_content):
    """Check whether a search phrase occurs in the document."""
    content = normalize_text(document_content)

    for phrase in get_search_phrases(question):
        if phrase and phrase in content:
            return True

    return False


def search_hybrid(question, top_k=5, candidate_k=15):

    if not question or not question.strip():
        raise ValueError("Please enter a valid question.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    candidate_k = max(candidate_k, top_k)

    # Multilingual semantic search
    faiss_results = search_multilingual(
        question,
        top_k=candidate_k
    )

    # Keyword search
    bm25_results = search_bm25(
        question,
        top_k=candidate_k
    )

    combined = {}

    # Add multilingual FAISS rankings
    for rank, document in enumerate(faiss_results, start=1):

        key = get_document_key(document)

        if key not in combined:
            combined[key] = {
                **document,
                "rrf_score": 0.0,
                "original_rrf_score": 0.0,
                "exact_phrase_bonus": 0.0,
                "faiss_rank": None,
                "bm25_rank": None,
                "faiss_score": None,
                "bm25_score": None
            }

        combined[key]["rrf_score"] += 1 / (RRF_K + rank)
        combined[key]["faiss_rank"] = rank
        combined[key]["faiss_score"] = document.get(
            "similarity_score"
        )

    # Add BM25 rankings; ignore zero-score matches
    for rank, document in enumerate(bm25_results, start=1):

        if document.get("bm25_score", 0) <= 0:
            continue

        key = get_document_key(document)

        if key not in combined:
            combined[key] = {
                **document,
                "rrf_score": 0.0,
                "original_rrf_score": 0.0,
                "exact_phrase_bonus": 0.0,
                "faiss_rank": None,
                "bm25_rank": None,
                "faiss_score": None,
                "bm25_score": None
            }

        combined[key]["rrf_score"] += 1 / (RRF_K + rank)
        combined[key]["bm25_rank"] = rank
        combined[key]["bm25_score"] = document.get("bm25_score")

    # Apply exact phrase matching bonus
    for document in combined.values():

        original_score = document["rrf_score"]

        document["original_rrf_score"] = original_score

        if has_exact_phrase_match(
            question,
            document.get("content", "")
        ):
            document["exact_phrase_bonus"] = EXACT_PHRASE_BONUS

        document["rrf_score"] = (
            original_score + document["exact_phrase_bonus"]
        )

    # Sort by adjusted RRF score
    results = sorted(
        combined.values(),
        key=lambda item: item["rrf_score"],
        reverse=True
    )

    return results[:top_k]
