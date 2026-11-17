
from Backend.hybrid_retrieval import search_hybrid

questions = [
    "agricultural machinery hiring centre subsidy",
    "75% subsidy 18.75 lakh",
    "World Bank Tamil Nadu Irrigated Agriculture Modernization",
    "விவசாய இயந்திரங்களை வாடகைக்கு வழங்கும் மையம் அமைப்பதற்கு என்ன மானியம் வழங்கப்படுகிறது?",
    "விவசாயத்தில் தண்ணீரை சிக்கனமாக பயன்படுத்தும் திட்டத்தின் நோக்கம் என்ன?"
]

for question in questions:

    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("=" * 70)

    results = search_hybrid(question, top_k=3)

    for rank, result in enumerate(results, start=1):

        print(f"\nRank: {rank}")
        print("RRF Score:", round(result["rrf_score"], 6))
        print("FAISS Rank:", result["faiss_rank"])
        print("BM25 Rank:", result["bm25_rank"])
        print("FAISS Similarity:", result["faiss_score"])
        print("BM25 Score:", result["bm25_score"])
        print("Source:", result["source"])
        print("Page:", result["page_number"])
        print("Content:", result["content"][:400])

print("\n========== HYBRID RETRIEVAL TEST COMPLETED ==========")
