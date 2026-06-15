import chromadb
from config.settings import VECTOR_PATH,COLLECTION_NAME
import uuid
import logging

#logger object 
logger = logging.getLogger(__name__)

def get_client():
    client = chromadb.PersistentClient(path = VECTOR_PATH)
    logger.info("Chroma DB client Received")
    return client

def get_collection():
    chroma = get_client()
    collection = chroma.get_or_create_collection(
        name = COLLECTION_NAME
    )
    logger.info("Chroma Collection Set")
    return collection
def store_doc(chunks,embeddings,filename):
    #validation to see chunks and embeddings match
    if len(chunks) != len(embeddings):
        raise ValueError(
            "Chunks and embeddings count must match"
        )
    logger.info("Embeddings and Texts match")
    #get the collection - I want to get multiple collections for each user which is something I need to work on
    collection = get_collection()
    #creating ids for chunks
    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]
    logger.info("Unique chunk IDs created")
    #improve this in later versions
    metadata = [
        {
        "source":filename,
        "chunk_index": i
         }
        for i in range(len(chunks))
    ]
    logger.info("Metadata added")
    collection.add(
        ids= ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadata
    )
    logger.info("Stored in Vector Database")
    

def list_collections():
    client = get_client()
    logger.info("Listed Collections in Chroma")
    return client.list_collections()


def preview_chunks(limit=10):
    collection = get_collection()
    logger.info(f"The number of chunks in Collection: {collection.count()}")
    return collection.peek(limit)

def get_documents():
    collection = get_collection()
    sources = set()
    results = collection.get()
    for metadata in results["metadatas"]:
        sources.add(metadata["source"])
    logger.info(f"Collection consists of: {list(sources)}")

def if_existing(filename):
    collection = get_collection()
    existing = collection.get(
        where={"source":filename}
    )
    if existing["ids"]:
        return True

def delete_collection():
    chroma = get_client()
    chroma.delete_collection(
        name=COLLECTION_NAME
    )
    logger.info("Collection Deleted!")

def print_metadata():
    collection = get_collection()
    result = collection.get()
    logger.info(f"Metadata : {result['metadatas']}")
