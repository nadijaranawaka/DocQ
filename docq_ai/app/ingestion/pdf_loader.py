from pypdf import PdfReader
from pathlib import Path
from app.config.settings import BASE_DIR
import logging

#logger object
logger = logging.getLogger(__name__)

#file path
pdf_path = BASE_DIR / "data" / "uploads" / "testpdf.pdf"
#when creating the upload function this will change for now the pdf is hardcoded

def read_pages(pdf_obj) -> list[dict]:
    pages = []
    for i,page in enumerate(pdf_obj.pages):
        pages.append({
            "page":i+1,
            "text":page.extract_text()
        })
    if not pages:
        raise ValueError("No text could be extracted from PDF")
    logger.info(f"Extracted text from {len(pdf_obj.pages)} pages")
    return pages

def load_pdf(path:Path) -> str:
    try:
        if not path.exists():
            raise FileNotFoundError(f"PDF file was not found: {path}")
        pdf = PdfReader(path)
        logger.info(f"Loaded PDF: {path.name}")
        content = read_pages(pdf_obj = pdf)
        return content
    except Exception:
        logger.exception("Failed to load PDF")
        raise