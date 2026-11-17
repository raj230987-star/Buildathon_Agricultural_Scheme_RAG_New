
import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

SOURCE_DB = Path("faiss_db")
NEW_DB = Path("faiss_db_multilingual")

MODEL_NAME = "intfloat/multilingual-e5-small"
DIMENSION = 384


def build_index():
    metadata_path = SOURCE_DB / "documents.json"

    if not metadata_path.exists():
        raise FileNotFoundError("Original documents.json not found.")

    documents = json.loads(
        metadata_path.read_text(encoding="utf-8")
    )

    if not documents:
        raise ValueError("No documents found.")

    print("Total document chunks:", len(documents))
    print("Loading multilingual E5 model...")

    model = SentenceTransformer(MODEL_NAME, device="cpu")

    passages = [
        "passage: " + doc.get("content", "")
        for doc in documents
    ]

    print("Generating multilingual embeddings...")

    embeddings = model.encode(
        passages,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=True
    ).astype("float32")

    if embeddings.shape != (len(documents), DIMENSION):
        raise ValueError(
            f"Unexpected embedding shape: {embeddings.shape}"
        )

    NEW_DB.mkdir(parents=True, exist_ok=True)

    index = faiss.IndexFlatIP(DIMENSION)
    index.add(embeddings)

    faiss.write_index(
        index,
        str(NEW_DB / "index.faiss")
    )

    (NEW_DB / "documents.json").write_text(
        json.dumps(documents, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("\n========== BUILD SUCCESSFUL ==========")
    print("Database folder:", NEW_DB)
    print("Total vectors:", index.ntotal)
    print("Vector dimension:", index.d)
    print("Metadata records:", len(documents))


if __name__ == "__main__":
    build_index()
