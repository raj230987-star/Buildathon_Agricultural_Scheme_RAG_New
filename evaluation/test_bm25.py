
from Backend.bm25_retrieval import search_bm25

questions = [
    "agricultural machinery hiring centre subsidy",
    "75% subsidy 18.75 lakh",
    "World Bank Tamil Nadu Irrigated Agriculture Modernization"
]

for question in questions:
    print("\n" + "=" * 60)
    print("QUESTION:", question)
    print("=" * 60)

    results = search_bm25(question, top_k=3)

    for rank, result in enumerate(results, start=1):
        print(f"\nRank {rank}")
        print("BM25 Score:", result["bm25_score"])
        print("Source:", result["source"])
        print("Page:", result["page_number"])
        print("Content:", result["content"][:350])
