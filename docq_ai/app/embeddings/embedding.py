from sentence_transformers import SentenceTransformer
from app.config.settings import EMBEDDING_MODEL
import logging

#logger object 
logger = logging.getLogger("docq")

#embedding model this can change according to how we need
modelName = EMBEDDING_MODEL

#load the model
try:    
    embeddingModel = SentenceTransformer(modelName)
except Exception:
    logger.exception("Failed to load to embedding model")
    raise

#convert chunk to embeddings
def get_embeddings(text):
    #check config
    if not EMBEDDING_MODEL:
        raise ValueError("EMBEDDING_MODEL is not defined in settings")
    logger.info("Embedding Model Activated")
    if isinstance(text,str):
        if not text.strip():
            raise ValueError("Text cannot be empty")
        embeddings = embeddingModel.encode(text)
        logger.info(f"Created embedding shape={embeddings.shape[0]}")
        logger.info("Embedding Complete took String as Input")
        return embeddings
    elif isinstance(text, list):
        if len(text) == 0:
            raise ValueError("Text list cannot be empty")
        if not all(isinstance(t,str)for t in text):
            raise TypeError("All items in the list should be strings")
        elif not all(t.strip() for t in text):
            raise ValueError("List contains empty strings")
        embeddings = embeddingModel.encode(text)
        logger.info(f"Created embedding shape={embeddings.shape[0]} : {embeddings.shape[1]}")
        logger.info("Embedding complete took a list of Strings as input")
        return embeddings
    else:
        raise TypeError("Chunks are expected to be a string or a list of strings")