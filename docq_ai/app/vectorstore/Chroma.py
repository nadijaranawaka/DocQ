import chromadb
import logging
import uuid
from app.embeddings import get_embeddings
from datetime import datetime,UTC
from app.config.settings import MAX_DISTANCE

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

    def generate_ids(self,count: int) -> list[str]:
        ids = [
            str(uuid.uuid4())
            for _ in range(count)
        ]
        logger.info(f"Generated {count} unique chunk IDs")
        return ids
    
    def build_metadata(self,chunks:list[dict],filename:str,ids:list[str]) -> list[dict]:
        metadata = []
        for i,chunk in enumerate(chunks):
            metadata.append({
                "source" : filename,
                "page" : chunk["page"],
                "chunk_index" : i,
                "chunk_id" : ids[i],
                "chunk_length" : len(chunk["text"]),
                "created_at" : datetime.now(UTC).isoformat(),
                "document_type" : "pdf"
            })
        logger.info(f"Created metadata for {len(metadata)} chunks.")
        return metadata
    
    def print_metadata(self):
        result = self.collection.get()
        print(
            f"Retrieved metadata for "
            f"{len(result['metadatas'])} chunks"
            f"{result['metadatas'][-1]}"
        )

    def _validate_store_input(
        self,
        chunks,
        embeddings,
        filename
    ):

        if not chunks:
            raise ValueError(
                "Chunks cannot be empty."
            )

        if not filename:
            raise ValueError(
                "Filename cannot be empty."
            )

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Chunks and embeddings must have equal length."
            )
    def store_doc(self,chunks,embeddings,filename):

        self._validate_store_input(chunks,embeddings,filename)
        logger.info("Embeddings and Texts match")

        #Unique Ids for chunks is a must
        ids = self.generate_ids(len(chunks))
        metadata = self.build_metadata(chunks,filename,ids)
        documents = [
            chunk["text"] for chunk in chunks
        ]
        self.collection.add(
            ids= ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadata
        )
        logger.info(f"Stored {len(chunks)} chunks into Chroma.")
    
    def search_doc(self,question, top_k,filename):
        if not question.strip():
            raise ValueError("Question cannot be empty")
        if top_k <= 0:
            raise ValueError("Top_k must be positive")
        
        #later on make this moved to pipeline which means send a embed query right away
        query_embedding = get_embeddings(question)
        try:
            result = self.collection.query(
                query_embeddings= [query_embedding.tolist()],
                n_results= top_k,
                where={
                    "source" : filename
                }
            )
            filtered = {
                "documents": [],
                "metadatas": [],
                "distances": []
            }

            for doc,metadata,distance in zip(
                result["documents"][0],
                result["metadatas"][0],
                result["distances"][0]
            ):
                if distance <= MAX_DISTANCE:
                    filtered["documents"].append(doc)
                    filtered["metadatas"].append(metadata)
                    filtered["distances"].append(distance)

        except Exception:
            logger.exception("Similarity search failed")
            raise
        logger.info("Similarity Search Complete")
        return filtered



        