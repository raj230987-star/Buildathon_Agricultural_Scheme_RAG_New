
import sys
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Backend.query_translation import translate_query
from Backend.hybrid_retrieval import search_hybrid


test_questions = [
    "விவசாய இயந்திரங்களை வாடகைக்கு வழங்கும் மையம் அமைப்பதற்கு என்ன மானியம் வழங்கப்படுகிறது?",
    "தமிழ்நாடு பாசன வேளாண்மை நவீனமயமாக்கல் திட்டத்தின் நோக்கம் என்ன?",
    "ஒரு துளி நீரில் அதிக பயிர் பெறுவது எந்த திட்டத்தின் நோக்கம்?",
    "What is the subsidy available for agricultural machinery?"
]


for original_question in test_questions:

    print("\n" + "=" * 75)
    print("ORIGINAL QUESTION:")
    print(original_question)

    # Step 1: Translate the question if it is Tamil
    search_query = translate_query(original_question)

    print("\nSEARCH QUERY:")
    print(search_query)

    # Step 2: Perform hybrid retrieval
    results = search_hybrid(
        search_query,
        top_k=5,
        candidate_k=25
    )

    print("\nHYBRID RETRIEVAL RESULTS:")

    if not results:
        print("No relevant documents found.")
        continue

    # Step 3: Display retrieved evidence
    for rank, result in enumerate(results, start=1):

        print(f"\nRank: {rank}")
        print("RRF Score:", result.get("rrf_score"))
        print("FAISS Rank:", result.get("faiss_rank"))
        print("BM25 Rank:", result.get("bm25_rank"))
        print("Source:", result.get("source"))
        print("Page:", result.get("page_number"))
        print("Content:", result.get("content", "")[:500])

print("\nTRANSLATION + HYBRID RETRIEVAL TEST COMPLETED")
