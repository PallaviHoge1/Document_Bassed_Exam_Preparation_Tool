from PyPDF2 import PdfReader

def extract_text_from_pdf(path: str) -> str:
    """Extract text from all pages of a PDF file."""
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        # page.extract_text() returns a string or None
        content = page.extract_text() or ""
        text.append(content)
    return "\n".join(text)
