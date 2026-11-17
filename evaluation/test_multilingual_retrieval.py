
from Backend.multilingual_retrieval import search_multilingual

questions = [
     "விவசாய இயந்திரங்களை வாடகைக்கு வழங்கும் மையம் அமைப்பதற்கு என்ன மானியம் வழங்கப்படுகிறது?",

    "விவசாயத்தில் தண்ணீரை சிக்கனமாக பயன்படுத்தும் திட்டத்தின் நோக்கம் என்ன?",

    "தமிழ்நாடு பாசன வேளாண்மை நவீனமயமாக்கல் திட்டத்தின் நோக்கம் என்ன?",

    "ஒரு துளி நீரில் அதிக பயிர் பெறுவது எந்த திட்டத்தின் நோக்கம்?",

    "What are the objectives of the Tamil Nadu Irrigated Agriculture Modernization Project?",

    "What does More crop per drop of water mean in the TN IAMP project?"
]

for question in questions:

    print("\n" + "=" * 65)
    print("QUESTION:", question)
    print("=" * 65)

    results = search_multilingual(question, top_k=3)

    for rank, result in enumerate(results, start=1):

        print(f"\nRank: {rank}")
        print("Similarity:", result["similarity_score"])
        print("Source:", result["source"])
        print("Page:", result["page_number"])
        print("Content:", result["content"][:400])

print("\nMULTILINGUAL RETRIEVAL TEST COMPLETED")
