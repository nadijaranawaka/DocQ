from sentence_transformers import SentenceTransformer
from app.config.settings import EMBEDDING_MODEL

#check config
if not EMBEDDING_MODEL:
    raise ValueError("EMBEDDING_MODEL is not defined in settings")

#embedding model this can change according to how we need
modelName = EMBEDDING_MODEL


#load the model
embeddingModel = SentenceTransformer(modelName)

def get_embeddings(text):

    if not isinstance(text,str):
        raise TypeError(f"Excpected String, got {type(text)}")
    if not isinstance(text,list):
        if not all(isinstance(t,str)for t in text):
            raise TypeError("All items in the list should be strings")
        raise TypeError("Chunks are not entered as a list")
    
    embeddings = embeddingModel.encode(text)
    print(embeddings.shape)
    return embeddings