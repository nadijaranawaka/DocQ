from pypdf import PdfReader
from pathlib import Path
from app.config.settings import BASE_DIR
import logging

#logger object
logger = logging.getLogger("docq")

#file path
pdf_path = BASE_DIR / "data" / "uploads" / "testpdf.pdf"
#when creating the upload function this will change for now the pdf is hardcoded

def read_pages(pdf_obj) -> list[dict]:
    pages = []
    for i,page in enumerate(pdf_obj.pages):
        text = page.extract_text()
        if not text:
            logger.warning(f"Page {i+1} contains no extractable text")
            text = ""
        pages.append({
            "page":i+1,
            "text": text
        })
    if not any(page["text"].strip() for page in pages):
        raise ValueError(
            "PDF contains no extractable text"
        )
    logger.info(f"Extracted text from {len(pdf_obj.pages)} pages")
    return pages

def load_pdf(path:Path) -> list[dict]:
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