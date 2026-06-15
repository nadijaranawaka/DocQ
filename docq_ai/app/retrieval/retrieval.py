from vectorstore.vectorstore import get_collection
from embeddings.embedding import get_embeddings
from config.settings import TOP_K
import logging

#logger object 
logger = logging.getLogger(__name__)

def search_doc(question, top_k=TOP_K):
    collection = get_collection()
    query_embedding = get_embeddings(question)
    result = collection.query(
        query_embeddings= [query_embedding.tolist()],
        n_results= top_k
    )
    logger.info("Similarity Search Complete")
    return result