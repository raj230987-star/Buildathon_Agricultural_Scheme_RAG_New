
import json
from pathlib import Path

db_file = Path("faiss_db/documents.json")
documents = json.loads(db_file.read_text(encoding="utf-8"))

def contains_tamil(text):
    return any("\u0B80" <= char <= "\u0BFF" for char in text)

tamil_chunks = []
english_chunks = []

for doc in documents:
    content = doc.get("content", "")

    if contains_tamil(content):
        tamil_chunks.append(doc)
    else:
        english_chunks.append(doc)

print("========== CORPUS LANGUAGE REPORT ==========")
print("Total chunks:", len(documents))
print("Chunks containing Tamil:", len(tamil_chunks))
print("Chunks without Tamil:", len(english_chunks))

print("\n========== TAMIL CONTENT SAMPLES ==========")

for doc in tamil_chunks[:5]:
    print("\nSource:", doc.get("source"))
    print("Page:", doc.get("page_number"))
    print("Content:", doc.get("content", "")[:500])

print("\n========== ENGLISH CONTENT SAMPLES ==========")

for doc in english_chunks[:2]:
    print("\nSource:", doc.get("source"))
    print("Page:", doc.get("page_number"))
    print("Content:", doc.get("content", "")[:300])
