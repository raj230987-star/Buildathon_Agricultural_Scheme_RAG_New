
from pypdf import PdfReader


def extract_pdf_text(file_path):
    """
    Extract text from a PDF document.
    Preserve page numbers for source tracking.
    """

    reader = PdfReader(file_path)

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        extracted_pages.append({
            "page_number": page_number,
            "content": text
        })

    return extracted_pages
