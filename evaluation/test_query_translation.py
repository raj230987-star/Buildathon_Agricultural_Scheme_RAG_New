
import sys
from pathlib import Path

# Add the project root directory to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from Backend.query_translation import translate_query


test_questions = [
    "விவசாய இயந்திரங்களை வாடகைக்கு வழங்கும் மையம் அமைப்பதற்கு என்ன மானியம் வழங்கப்படுகிறது?",
    "தமிழ்நாடு பாசன வேளாண்மை நவீனமயமாக்கல் திட்டத்தின் நோக்கம் என்ன?",
    "What is the subsidy available for agricultural machinery?"
]

for question in test_questions:

    print("\n" + "=" * 70)
    print("ORIGINAL QUESTION:")
    print(question)

    translated = translate_query(question)

    print("\nTRANSLATED SEARCH QUERY:")
    print(translated)
