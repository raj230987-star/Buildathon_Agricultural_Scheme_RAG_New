
import json
import tempfile
import sys
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import faiss
import numpy as np

from Backend import multilingual_ingestion as ingestion


def test_multilingual_ingestion():

    print("\n========== MULTILINGUAL INGESTION TEST ==========")

    # Create an isolated temporary database
    with tempfile.TemporaryDirectory() as temp_dir:

        test_db = Path(temp_dir)

        ingestion.DB_DIR = test_db
        ingestion.INDEX_PATH = test_db / "index.faiss"
        ingestion.METADATA_PATH = test_db / "documents.json"

        # Create one initial test vector
        model = ingestion.get_model()

        initial_embedding = model.encode(
            ["passage: Initial test document"],
            normalize_embeddings=True,
            convert_to_numpy=True
        ).astype("float32")

        index = faiss.IndexFlatIP(384)
        index.add(initial_embedding)

        faiss.write_index(index, str(ingestion.INDEX_PATH))

        initial_metadata = [{
            "content": "Initial test document",
            "source": "initial.pdf",
            "stored_filename": "initial.pdf",
            "page_number": 1,
            "start_index": 0
        }]

        ingestion.METADATA_PATH.write_text(
            json.dumps(initial_metadata),
            encoding="utf-8"
        )

        print("Initial vectors:", index.ntotal)

        # Add a new synthetic PDF page
        test_pages = [{
            "page_number": 1,
            "content": (
                "Agricultural machinery hiring centres "
                "provide farm equipment rental services."
            )
        }]

        result = ingestion.add_document_to_multilingual_faiss(
            pages=test_pages,
            original_filename="test_agriculture.pdf",
            stored_filename="test_agriculture.pdf"
        )

        # Verify updated database
        updated_index = faiss.read_index(
            str(ingestion.INDEX_PATH)
        )

        documents = json.loads(
            ingestion.METADATA_PATH.read_text(encoding="utf-8")
        )

        print("\nNew chunks:", result["new_chunks"])
        print("Total vectors:", updated_index.ntotal)
        print("Metadata records:", len(documents))
        print("New source:", documents[-1]["source"])

        assert updated_index.ntotal == len(documents)
        assert updated_index.ntotal == 2
        assert documents[-1]["source"] == "test_agriculture.pdf"

        print("\nTEST PASSED")
        print("Existing test vector preserved.")
        print("New PDF chunk successfully appended.")


if __name__ == "__main__":
    test_multilingual_ingestion()
