from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config.settings import CHUNK_OVERLAP, CHUNK_SIZE
import logging

#logger object 
logger = logging.getLogger(__name__)


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
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP
    )
    logger.info("Spillter Ready")
    return splitter

def chunk_document(text: str)  -> list[str]:
    
    #input validation
    if not isinstance(text, str):
        raise TypeError(f"Expected String, Got {type(text).__name__}")
    if not text.strip():
        return []
    
    split = set_splitter()

    #Chunking
    docs = split.split_text(text)

    logger.info("Chunking Complete")
    return docs
