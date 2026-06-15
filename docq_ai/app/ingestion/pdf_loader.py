from pypdf import PdfReader
from config.settings import BASE_DIR
import logging

#logger object
logger = logging.getLogger(__name__)

#file path
pdf_path = BASE_DIR / "data" / "uploads" / "testpdf.pdf"
#when creating the upload function this will change for now the pdf is hardcoded

def read_pages(pdfObj):
    text = ""
    for page in pdfObj.pages:
        pdf_content = page.extract_text()
        if pdf_content:
            text += pdf_content + "\n"
    logger.info("PDF file converted to String")
    return text

def load_pdf(path):
    try:
        pdf = PdfReader(path)
        logger.info("PDF path found")
    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file was not found in {path.strip().replace('/','-')}")
    content = read_pages(pdfObj = pdf)
    return content