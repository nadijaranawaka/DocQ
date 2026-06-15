from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

#check config
if not EMBEDDING_MODEL:
    raise ValueError("EMBEDDING_MODEL is not defined in settings")

#embedding model this can change according to how we need
modelName = EMBEDDING_MODEL


#load the model
embeddingModel = SentenceTransformer(modelName)

#convert chunk to embeddings
def get_embeddings(text):
    if isinstance(text,str):
        embeddings = embeddingModel.encode(text)
        print(embeddings.shape)
        return embeddings
    elif isinstance(text, list):
        if not all(isinstance(t,str)for t in text):
            raise TypeError("All items in the list should be strings")
        embeddings = embeddingModel.encode(text)
        print(embeddings.shape)
        return embeddings
    else:
        raise TypeError({"Chunks are expected to be a string or a list of strings"})