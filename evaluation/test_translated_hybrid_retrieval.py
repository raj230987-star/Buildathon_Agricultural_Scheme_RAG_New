
import os
from dotenv import load_dotenv
from openai import OpenAI

from Backend.hybrid_retrieval import search_hybrid

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env")

if not MODEL:
    raise ValueError("OPENAI_MODEL not found in .env")

client = OpenAI(api_key=API_KEY)


def translate_query(question):
    response = client.responses.create(
        model=MODEL,
        
instructions=(
    "Translate the user's Tamil agricultural government scheme "
    "question into English for searching agricultural scheme PDFs. "
    "Use official agricultural scheme terminology. "

    "For a machinery hiring centre, prefer the exact phrase "
    "'Integrated Agricultural Machinery Hiring Business Centre' "
    "instead of only 'Custom Hiring Centre'. "

    "Include relevant search terms such as subsidy, benefits, "
    "project cost, eligibility and funding pattern when appropriate. "

    "Do not invent subsidy amounts, scheme details or answers. "

    "Do not introduce alternative scheme names, acronyms, "
    "or government programmes that are not explicitly mentioned "
    "or clearly established by the original question. "
    "Preserve the user's intended meaning. "

    "Return only the English search query."
),
        input=question
    )

    return response.output_text.strip()


questions = [
    "விவசாய இயந்திரங்களை வாடகைக்கு வழங்கும் மையம் அமைப்பதற்கு என்ன மானியம் வழங்கப்படுகிறது?",
    "தமிழ்நாடு பாசன வேளாண்மை நவீனமயமாக்கல் திட்டத்தின் நோக்கம் என்ன?",
    "ஒரு துளி நீரில் அதிக பயிர் பெறுவது எந்த திட்டத்தின் நோக்கம்?"
]


for question in questions:

    print("\n" + "=" * 70)
    print("ORIGINAL TAMIL QUESTION:")
    print(question)

    translated = translate_query(question)

    print("\nTRANSLATED ENGLISH QUERY:")
    print(translated)

    results = search_hybrid(
        translated,
        top_k=5,
        candidate_k=25
    )

    print("\nHYBRID RETRIEVAL RESULTS:")

    for rank, result in enumerate(results, start=1):

        print(f"\nRank: {rank}")
        print("RRF Score:", round(result["rrf_score"], 6))
        print("FAISS Rank:", result["faiss_rank"])
        print("BM25 Rank:", result["bm25_rank"])
        print("Source:", result["source"])
        print("Page:", result["page_number"])
        print("Content:", result["content"][:350])

print("\nTRANSLATED HYBRID RETRIEVAL TEST COMPLETED")
