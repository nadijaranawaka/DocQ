from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config.settings import CHUNK_OVERLAP, CHUNK_SIZE
import logging

#logger object 
logger = logging.getLogger("docq")


# def set_params(text: str):
#     length = len(text)
# add dynamic chunking in v2

def set_splitter() -> RecursiveCharacterTextSplitter:
    
    #chunk validation
    if CHUNK_SIZE <= 0:
        raise ValueError("CHUNK_SIZE must be positive")

    if CHUNK_OVERLAP >= CHUNK_SIZE:
        raise ValueError(
            "CHUNK_OVERLAP must be smaller than CHUNK_SIZE"
        )
    
    #Setting RecursiveCharacterTextSplitter
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = CHUNK_SIZE,
            chunk_overlap = CHUNK_OVERLAP
        )
    except Exception:
        logger.exception("Failed to Create text splitter")
        raise
    logger.info(f"Spiltter Ready. Chunk size={CHUNK_SIZE}. Chunk Overlap={CHUNK_OVERLAP}")
    return splitter

def chunk_document(pages: list[dict]) -> list[dict]:
    
    #input validation
    if not isinstance(pages, list):
        raise TypeError(
            f"Expected list, got {type(pages).__name__}"
        )
    
    split = set_splitter()
    chunks = []

    #Chunking
    for page in pages:

        page_number = page["page"]
        text = page["text"]

        if not text.strip():
            continue

        page_chunks = split.split_text(text)

        for chunk in page_chunks:

            chunks.append({
                "page": page_number,
                "text": chunk
            })
    if not chunks:
        raise ValueError("Chunking produced no chunks")

    logger.info(f"Chunking Complete. Created {len(chunks)} chunks")
    return chunks
