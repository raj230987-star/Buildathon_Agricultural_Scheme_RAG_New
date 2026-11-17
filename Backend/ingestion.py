
import json
from pathlib import Path

import faiss

from langchain_text_splitters import RecursiveCharacterTextSplitter

from Backend.embedding import generate_embeddings


# FAISS database folder
DB_DIR = Path("faiss_db")

INDEX_PATH = DB_DIR / "index.faiss"
METADATA_PATH = DB_DIR / "documents.json"

DB_DIR.mkdir(parents=True, exist_ok=True)

# all-MiniLM-L6-v2 produces 384-dimensional vectors
EMBEDDING_DIMENSION = 384


def split_text_into_chunks(pages):
    """
    Split extracted PDF text into smaller chunks.
    Preserve the original PDF page number.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        add_start_index=True
    )

    all_chunks = []

    for page in pages:

        page_text = page["content"]

        if not page_text.strip():
            continue

        chunks = splitter.create_documents(
            [page_text],
            metadatas=[
                {"page_number": page["page_number"]}
            ]
        )

        for chunk in chunks:

            all_chunks.append({
                "content": chunk.page_content,
                "page_number": page["page_number"],
                "start_index": chunk.metadata["start_index"]
            })

    return all_chunks


def add_document_to_faiss(
    pages,
    original_filename,
    stored_filename
):
    """
    Generate embeddings and save PDF chunks in FAISS.
    """

    # STEP 1: Split PDF text into chunks
    chunks = split_text_into_chunks(pages)

    if not chunks:
        raise ValueError("No text chunks available for embedding")

    print(f"Total chunks created: {len(chunks)}")

    # STEP 2: Prepare text for embedding
    texts = [
        chunk["content"]
        for chunk in chunks
    ]

    # STEP 3: Generate embeddings
    embeddings = generate_embeddings(texts)

    # STEP 4: Load existing database or create a new one
    if INDEX_PATH.exists():

        if not METADATA_PATH.exists():
            raise ValueError("FAISS metadata file is missing")

        index = faiss.read_index(str(INDEX_PATH))

        with open(
            METADATA_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            metadata = json.load(file)

        if index.d != EMBEDDING_DIMENSION:
            raise ValueError("FAISS embedding dimension mismatch")

        if index.ntotal != len(metadata):
            raise ValueError("FAISS index and metadata count mismatch")

    else:

        index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)
        metadata = []

    # STEP 5: Add embeddings to FAISS
    index.add(embeddings)

    # STEP 6: Prepare metadata for each chunk
    new_metadata = []

    for chunk in chunks:

        new_metadata.append({
            "content": chunk["content"],
            "source": original_filename,
            "stored_filename": stored_filename,
            "page_number": chunk["page_number"],
            "start_index": chunk["start_index"]
        })

    metadata.extend(new_metadata)

    # STEP 7: Save FAISS index
    faiss.write_index(index, str(INDEX_PATH))

    # STEP 8: Save metadata
    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=4
        )

    return {
        "total_chunks": len(chunks),
        "total_vectors": index.ntotal,
        "database_path": str(INDEX_PATH)
    }
