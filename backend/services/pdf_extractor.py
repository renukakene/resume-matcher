"""
PDF Extraction Service
Extracts clean plain text from uploaded PDF resumes using PyMuPDF (fitz).
"""

try:
    import pymupdf as fitz
except ImportError:
    import fitz
from typing import Tuple


class PDFExtractionError(Exception):
    """Custom exception raised when PDF text extraction fails."""
    pass


def extract_text_from_pdf(pdf_bytes: bytes) -> Tuple[str, int]:
    """
    Extracts text and page count from raw PDF bytes.
    
    Args:
        pdf_bytes: Raw bytes of the uploaded PDF file.
        
    Returns:
        Tuple containing (full_extracted_text, page_count).
        
    Raises:
        PDFExtractionError: If PDF cannot be opened, is encrypted with password,
                            or contains no extractable text.
    """
    if not pdf_bytes or len(pdf_bytes) == 0:
        raise PDFExtractionError("The uploaded file is empty.")

    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise PDFExtractionError(f"Could not read PDF file. It might be corrupt or invalid: {str(e)}")

    if doc.is_encrypted:
        raise PDFExtractionError("The PDF file is password protected. Please upload an unprotected PDF.")

    page_count = len(doc)
    if page_count == 0:
        raise PDFExtractionError("The PDF document contains 0 pages.")

    full_text_parts = []
    for page_num in range(page_count):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        if text:
            full_text_parts.append(text)

    doc.close()

    full_text = "\n".join(full_text_parts).strip()

    if not full_text:
        raise PDFExtractionError(
            "No extractable text found in the PDF. The file may be a scanned image or empty. "
            "Please use a text-based PDF resume."
        )

    return full_text, page_count
