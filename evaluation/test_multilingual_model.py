
from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_NAME = "intfloat/multilingual-e5-small"

print("Loading multilingual model...")
model = SentenceTransformer(MODEL_NAME, device="cpu")

# Test 1: Tamil question -> English passage
tamil_query = "query: விதை கிராம திட்டம் விவசாயிகளுக்கு தரமான விதைகளை வழங்குகிறது."

english_passages = [
    "passage: The Seed Village Scheme provides quality seeds to farmers.",
    "passage: Solar energy systems generate electricity using sunlight.",
    "passage: Agricultural machinery helps farmers perform field operations."
]

# Test 2: English question -> Tamil passage
english_query = "query: Government subsidy for agricultural machinery."

tamil_passages = [
    "passage: விவசாய இயந்திரங்கள் வாங்குவதற்கு அரசு மானியம் வழங்குகிறது.",
    "passage: சூரிய ஆற்றல் மூலம் மின்சாரம் உற்பத்தி செய்யப்படுகிறது.",
    "passage: விவசாயிகளுக்கு தரமான விதைகள் வழங்கப்படுகின்றன."
]


def test_retrieval(query, passages, expected_index, test_name):

    query_vector = model.encode(
        [query],
        normalize_embeddings=True
    )

    passage_vectors = model.encode(
        passages,
        normalize_embeddings=True
    )

    scores = np.dot(
        passage_vectors,
        query_vector[0]
    )

    best_index = int(np.argmax(scores))

    print("\n", test_name)
    print("-" * 45)

    for i, score in enumerate(scores):
        print(f"Passage {i + 1}: {score:.4f}")

    print("Best matching passage:", best_index + 1)

    if best_index == expected_index:
        print("RESULT: PASS")
        return True

    print("RESULT: REVIEW REQUIRED")
    return False


test1 = test_retrieval(
    tamil_query,
    english_passages,
    0,
    "Tamil Question -> English Passage"
)

test2 = test_retrieval(
    english_query,
    tamil_passages,
    0,
    "English Question -> Tamil Passage"
)

print("\n========== FINAL RESULT ==========")
print("Tests passed:", int(test1) + int(test2), "/ 2")
