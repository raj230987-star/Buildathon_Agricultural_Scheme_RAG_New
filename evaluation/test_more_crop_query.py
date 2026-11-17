
from Backend.hybrid_retrieval import search_hybrid
from Backend.multilingual_retrieval import search_multilingual
from Backend.bm25_retrieval import search_bm25

queries = [
    "More crop per drop of water",
    "More Crop Per Drop",
    "Tamil Nadu Irrigated Agriculture Modernization Project objectives",
]

for query in queries:
    print("\n" + "=" * 70)
    print("QUERY:", query)

    print("\n--- FAISS RESULTS ---")
    for rank, doc in enumerate(search_multilingual(query, top_k=5), start=1):
        print(
            f"Rank {rank} | {doc['source']} | "
            f"Page {doc['page_number']} | "
            f"Score {doc['similarity_score']}"
        )

    print("\n--- BM25 RESULTS ---")
    for rank, doc in enumerate(search_bm25(query, top_k=5), start=1):
        print(
            f"Rank {rank} | {doc['source']} | "
            f"Page {doc['page_number']} | "
            f"Score {doc['bm25_score']}"
        )

    print("\n--- HYBRID RRF RESULTS ---")
    for rank, doc in enumerate(
        search_hybrid(query, top_k=5, candidate_k=25), start=1
    ):
        print(
            f"Rank {rank} | {doc['source']} | "
            f"Page {doc['page_number']} | "
            f"RRF {doc['rrf_score']:.6f} | "
            f"FAISS {doc['faiss_rank']} | "
            f"BM25 {doc['bm25_rank']}"
        )

print("\nTEST COMPLETED")
