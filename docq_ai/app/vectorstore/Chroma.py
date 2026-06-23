import chromadb
import logging
import uuid
from app.embeddings.embedding import get_embeddings

#logger object
logger = logging.getLogger(__name__)

class ChromaDB:
    def __init__(self,collectionName,vectorPath):
        self.client = chromadb.PersistentClient(path=vectorPath)
        self.collection = self.client.get_or_create_collection(
            name = collectionName
        )
        logger.info("Chroma Collection Ready!")
    
    def list_collections(self):
        logger.info("Listed Collections in Chroma")
        return self.client.list_collections()


    def preview_chunks(self,limit=10):
        logger.info(f"The number of chunks in Collection: {self.collection.count()}")
        return self.collection.peek(limit)

    def get_documents(self):
        sources = set()
        results = self.collection.get()
        for metadata in results["metadatas"]:
            sources.add(metadata["source"])
        logger.info(f"Collection consists of: {list(sources)}")

    def if_existing(self,filename):
        existing = self.collection.get(
            where={"source":filename}
        )
        if existing["ids"]:
            return True

    def delete_collection(self,collectionName):
        self.client.delete_collection(
            name=collectionName
        )
        logger.info("Collection Deleted!")

    def print_metadata(self):
        result = self.collection.get()
        logger.info(f"Metadata : {result['metadatas']}")

    def store_doc(self,chunks,embeddings,filename):
        #Validate length of chunks = embeddings length
        if len(chunks) != len(embeddings):
            raise ValueError("" \
                "Chunk and Embedding counts must Match"
            )
        logger.info("Embeddings and Texts match")
        #Unique Ids for chunks is a must
        ids = [
            str(uuid.uuid4())
            for _ in chunks
        ]
        logger.info("Unique chunk IDs created")
        #improve this in later versions
        #for uses use metadata as well
        metadata = [
            {
            "source":filename,
            "chunk_index": i
            }
            for i in range(len(chunks))
        ]
        logger.info("Metadata added")
        self.collection.add(
            ids= ids,
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=metadata
        )
        logger.info("Stored in Vector Database")
    
    def search_doc(self,question, top_k):
        query_embedding = get_embeddings(question)
        result = self.collection.query(
            query_embeddings= [query_embedding.tolist()],
            n_results= top_k
        )
        logger.info("Similarity Search Complete")
        return result



        