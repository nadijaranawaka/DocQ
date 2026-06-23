from pathlib import Path

#Project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

#Logs
LOG_DIR = BASE_DIR / "logs"

#embedding model 
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

#Chunk dimensions
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

#Vector database
VECTOR_PATH = "/vector"
COLLECTION_NAME = "documents"

#Retrieval
TOP_K = 3

#embedding model 
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

#LLM
MODEL_GEM = "gemini-2.5-flash"
TEMP = 0.7
