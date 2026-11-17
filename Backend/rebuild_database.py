
import hashlib
import json
import re
from pathlib import Path

import faiss

from Backend.pdf_processor import extract_pdf_text
from Backend.ingestion import add_document_to_faiss


UPLOAD_DIR = Path("uploaded_pdfs")
DB_DIR = Path("faiss_db")

REGISTRY_PATH = DB_DIR / "uploaded_files.json"


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(block)

    return sha256.hexdigest()


def clean_filename(filename):
    # Remove repeated UUID prefixes from stored filenames.
    while re.match(r"^[0-9a-fA-F]{32}_", filename):
        filename = filename[33:]

    return filename


def rebuild_database():

    if not UPLOAD_DIR.exists():
        raise FileNotFoundError("uploaded_pdfs folder not found")

    pdf_files = sorted(UPLOAD_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError("No PDF files found")

    # Identify unique PDFs using SHA-256.
    unique_files = {}
    
    for pdf_path in pdf_files:
        file_hash = calculate_sha256(pdf_path)

        if file_hash not in unique_files:
            unique_files[file_hash] = pdf_path
        else:
            print(f"Duplicate skipped: {pdf_path.name}")

    print("\nTotal PDF files:", len(pdf_files))
    print("Unique PDF files:", len(unique_files))

    # Rebuild only after the backup has been created.
    DB_DIR.mkdir(parents=True, exist_ok=True)

    for old_file in [
        DB_DIR / "index.faiss",
        DB_DIR / "documents.json"
    ]:
        if old_file.exists():
            old_file.unlink()

    registry = []

    for file_hash, pdf_path in unique_files.items():

        print("\nProcessing:", pdf_path.name)

        pages = extract_pdf_text(pdf_path)

        original_filename = clean_filename(pdf_path.name)

        result = add_document_to_faiss(
            pages=pages,
            original_filename=original_filename,
            stored_filename=pdf_path.name
        )

        registry.append({
            "sha256": file_hash,
            "original_filename": original_filename,
            "stored_filename": pdf_path.name
        })

        print("Pages:", len(pages))
        print("Chunks added:", result["total_chunks"])
        print("Total vectors:", result["total_vectors"])

    with open(REGISTRY_PATH, "w", encoding="utf-8") as file:
        json.dump(registry, file, ensure_ascii=False, indent=4)

    index = faiss.read_index(str(DB_DIR / "index.faiss"))

    print("\n========== REBUILD COMPLETE ==========")
    print("Unique PDFs:", len(registry))
    print("Total FAISS vectors:", index.ntotal)
    print("Registry created:", REGISTRY_PATH)


if __name__ == "__main__":
    rebuild_database()
