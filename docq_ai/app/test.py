from app.vectorstore import ChromaDB
from app.config.settings import VECTOR_PATH,COLLECTION_NAME,MODEL_GEM,TEMP

chroma = ChromaDB(COLLECTION_NAME, VECTOR_PATH)
chroma.delete_collection(COLLECTION_NAME)