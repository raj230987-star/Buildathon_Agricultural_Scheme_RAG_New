
import os
import re
import unicodedata

from dotenv import load_dotenv
from openai import OpenAI

# Load API configuration from .env
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL")


def contains_tamil(text):
    """Check whether the question contains Tamil characters."""
    return bool(re.search(r"[\u0B80-\u0BFF]", text))


def clean_translation(text):
    """
    Clean unwanted Unicode characters and formatting
    from the translated search query.
    """

    # Normalize Unicode representation
    text = unicodedata.normalize("NFKC", text)

    # Remove Unicode control, format and surrogate characters
    text = "".join(
        char for char in text
        if not unicodedata.category(char).startswith("C")
    )

    # Remove unwanted leading/trailing punctuation and spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text.strip(" \t\n\r-–—")


def translate_query(question):
    """
    Translate Tamil agricultural scheme questions into English
    for hybrid retrieval.

    English questions are returned without modification.
    If translation fails, the original question is returned.
    """

    if not question or not question.strip():
        raise ValueError("Please enter a valid question.")

    question = question.strip()

    # No translation required for English questions
    if not contains_tamil(question):
        return question

    if not API_KEY:
        print("Warning: OPENAI_API_KEY not found. Using original question.")
        return question

    if not MODEL:
        print("Warning: OPENAI_MODEL not found. Using original question.")
        return question

    try:
        client = OpenAI(api_key=API_KEY)

        response = client.responses.create(
            model=MODEL,
            instructions=(
                "Translate the user's Tamil agricultural government "
                "scheme question into English for searching agricultural "
                "scheme PDFs. Use official agricultural scheme terminology. "

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

                "Return only the English search query. "
                "Do not include Unicode replacement characters, "
                "control characters, or decorative symbols."
            ),
            input=question
        )

        translated = clean_translation(response.output_text)

        if not translated:
            print("Warning: Empty translation. Using original question.")
            return question

        return translated

    except Exception as error:
        print(f"Translation error: {error}")
        print("Using the original question instead.")
        return question
