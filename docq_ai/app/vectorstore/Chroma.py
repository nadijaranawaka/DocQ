import chromadb
import logging
import uuid
from app.embeddings import get_embeddings

#logger object
logger = logging.getLogger(__name__)

class ChromaDB:
    def __init__(self,collectionName,vectorPath):
        if not collectionName:
            raise ValueError(
                "Collection name cannot be empty"
            )

        if not vectorPath:
            raise ValueError(
                "Vector path cannot be empty"
            )
        try:
            self.client = chromadb.PersistentClient(path=vectorPath)
            self.collection = self.client.get_or_create_collection(
                name = collectionName
            )
            logger.info(f"Connected to Collection: {collectionName}")
        except Exception:
            logger.exception("Failed to initialize ChromaDB")
            raise
    
    def list_collections(self) -> list:
        logger.info("Listed Collections in Chroma")
        return self.client.list_collections()


    def preview_chunks(self,limit=10):
        logger.info(f"The number of chunks in Collection: {self.collection.count()}")
        return self.collection.peek(limit)

    def get_documents(self) -> list:
        sources = set()
        results = self.collection.get()
        for metadata in results["metadatas"]:
            sources.add(metadata["source"])
        documents = list(sources)
        logger.info(f"Collection consists of: {documents}")
        return documents

    def if_existing(self,filename) -> bool:
        existing = self.collection.get(
            where={"source":filename}
        )
        return bool(existing["ids"])

    def delete_collection(self,collectionName):
        self.client.delete_collection(
            name=collectionName
        )
        logger.info("Collection Deleted!")

    def print_metadata(self):
        result = self.collection.get()
        logger.info(
            f"Retrieved metadata for "
            f"{len(result['metadatas'])} chunks"
        )

    def store_doc(self,chunks,embeddings,filename):

        if not chunks:
            raise ValueError("Chunks cannot be empty")
        if not filename:
            raise ValueError("Filename cannot be empty")
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
        if not question.strip():
            raise ValueError("Question cannot be empty")
        if top_k <= 0:
            raise ValueError("Top_k must be positive")
        
        #later on make this moved to pipeline which means send a embed query right away
        query_embedding = get_embeddings(question)
        try:
            result = self.collection.query(
                query_embeddings= [query_embedding.tolist()],
                n_results= top_k
            )
        except Exception:
            logger.exception("Similarity search failed")
            raise
        logger.info("Similarity Search Complete")
        return result



        