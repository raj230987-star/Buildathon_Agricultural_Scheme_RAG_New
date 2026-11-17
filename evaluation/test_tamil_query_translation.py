
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env")

if not MODEL:
    raise ValueError("OPENAI_MODEL not found in .env")

client = OpenAI(api_key=API_KEY)

questions = [
    "விவசாய இயந்திரங்களை வாடகைக்கு வழங்கும் மையம் அமைப்பதற்கு என்ன மானியம் வழங்கப்படுகிறது?",
    "தமிழ்நாடு பாசன வேளாண்மை நவீனமயமாக்கல் திட்டத்தின் நோக்கம் என்ன?",
    "ஒரு துளி நீரில் அதிக பயிர் பெறுவது எந்த திட்டத்தின் நோக்கம்?"
]

for question in questions:
    print("\n" + "=" * 65)
    print("ORIGINAL TAMIL QUESTION:")
    print(question)

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
    "Return only the English search query."
),

        input=question
    )

    translated = response.output_text.strip()

    print("\nTRANSLATED ENGLISH QUERY:")
    print(translated)

print("\nTAMIL QUERY TRANSLATION TEST COMPLETED")
