import chromadb
from config.settings import VECTOR_PATH,COLLECTION_NAME
import uuid

def get_client():
    client = chromadb.PersistentClient(path = VECTOR_PATH)
    return client

def get_collection():
    chroma = get_client()
    collection = chroma.get_or_create_collection(
        name = COLLECTION_NAME
    )
    return collection
def store_doc(chunks,embeddings,filename):
    #validation to see chunks and embeddings match
    if len(chunks) != len(embeddings):
        raise ValueError(
            "Chunks and embeddings count must match"
        )
    #get the collection - I want to get multiple collections for each user which is something I need to work on
    collection = get_collection()
    #creating ids for chunks
    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]
    #improve this in later versions
    metadata = [
        {
        "source":filename,
        "chunk_index": i
         }
        for i in range(len(chunks))
    ]
    collection.add(
        ids= ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadata
    )

def list_collections():
    client = get_client()
    return client.list_collections()

def preview_chunks(limit=10):
    collection = get_collection()
    print(collection.count())
    return collection.peek(limit)

def get_documents():
    collection = get_collection()
    sources = set()
    results = collection.get()
    for metadata in results["metadatas"]:
        sources.add(metadata["source"])
    return list(sources)

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

def print_metadata():
    collection = get_collection()
    result = collection.get()
    print(result["metadatas"])
