from app.config.settings import TOP_K
from model import build_prompt
from app.ingestion import load_pdf
from app.ingestion import clean_text
from app.ingestion import chunk_document
from app.embeddings import get_embeddings
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self,llm,vector):
        if llm is None:
            raise ValueError("LLM instance cannot be None")
        if vector is None:
            raise ValueError("Vector store instance cannot be None")
        self.llm = llm
        self.vector = vector
        logger.info("Pipeline initialized")
    
    def upload_file(self,path:Path) -> None:
        try:
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            
            pdfText = load_pdf(path)
            logger.info(f"Starting ingestion for {path.name}")
            finalText = clean_text(pdfText)
            chunks = chunk_document(finalText)
            embeddings = get_embeddings(chunks)
            logger.info(f"Generated {len(embeddings)} embeddings")

            #check if the document is already stored
            if self.vector.if_existing(path.stem):
                logger.warning(f"{path.stem} already exists")
            else:
                self.vector.store_doc(chunks,embeddings,path.stem)
        except Exception:
            logger.exception("Ingestion Failed")
            raise


    def ask_docq(self,question:str) -> str:
        try:
            results = self.vector.search_doc(question,TOP_K)
            if not results["documents"]:
                raise ValueError("No relevant documents found")
            chunks = results['documents'][0]
            logger.info(f"Retrieved {len(chunks)} chunks")
            prompt = build_prompt(question=question,chunks=chunks)
            answer = self.llm.generate(prompt=prompt)
            return answer
        except Exception:
            logger.exception("Question Answering Failed")
            raise