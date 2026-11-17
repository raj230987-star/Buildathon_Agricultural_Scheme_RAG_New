
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-small"

DB_FILE = Path("faiss_db/documents.json")

documents = json.loads(DB_FILE.read_text(encoding="utf-8"))

print("Loading multilingual E5 model...")
model = SentenceTransformer(MODEL_NAME, device="cpu")

# Tamil questions based on the actual scheme content
questions = [
    "விவசாய இயந்திரங்களை வாடகைக்கு வழங்கும் மையம் அமைப்பதற்கு என்ன மானியம் வழங்கப்படுகிறது?",
    "விவசாய இயந்திர வாடகை மையம் அமைப்பதற்கான அரசு நிதி உதவி எவ்வளவு?",
    "விவசாயத்தில் தண்ணீரை சிக்கனமாக பயன்படுத்தும் திட்டத்தின் நோக்கம் என்ன?"
]

# E5 requires query and passage prefixes
passages = [
    "passage: " + doc.get("content", "")
    for doc in documents
]

print("Creating document embeddings...")
passage_vectors = model.encode(
    passages,
    normalize_embeddings=True,
    convert_to_numpy=True,
    show_progress_bar=True
)

for question in questions:
    query_vector = model.encode(
        ["query: " + question],
        normalize_embeddings=True,
        convert_to_numpy=True
    )[0]

    scores = np.dot(passage_vectors, query_vector)
    top_indices = np.argsort(scores)[::-1][:3]

    print("\n" + "=" * 65)
    print("TAMIL QUESTION:", question)
    print("=" * 65)

    for rank, index in enumerate(top_indices, start=1):
        doc = documents[int(index)]

        print(f"\nRank {rank} | Similarity: {scores[index]:.4f}")
        print("Source:", doc.get("source"))
        print("Page:", doc.get("page_number"))
        print("Content:", doc.get("content", "")[:450])

print("\nREAL CORPUS TEST COMPLETED")

