
from sentence_transformers import SentenceTransformer

# HuggingFace embedding model
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Load model only once
_model = None


def get_embedding_model():
    global _model

    if _model is None:
        print("Loading HuggingFace embedding model...")

        _model = SentenceTransformer(MODEL_NAME)

        print("Embedding model loaded successfully!")

    return _model


def generate_embeddings(texts):
    """
    Convert text chunks into numerical vectors.
    """

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings.astype("float32")
