from vectorstore.vectorstore import get_collection
from embeddings.embedding import get_embeddings

def search_doc(question, top_k=3):
    collection = get_collection()
    query_embedding = get_embeddings(question)
    result = collection.query(
        query_embeddings= [query_embedding.tolist()],
        n_results= top_k
    )
    return result