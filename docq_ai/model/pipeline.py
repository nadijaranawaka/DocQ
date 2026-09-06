from app.config.settings import TOP_K
from model import build_prompt
from app.ingestion import load_pdf
from app.ingestion import clean_pages
from app.ingestion import chunk_document
from app.embeddings import get_embeddings
from app.ingestion.header_detector import find_headers,remove_headers
from app.vectorstore.context_builder import contextBuilder
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
    
    def upload_file(self,path:Path,document_id:str) -> None:
        try:
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            
            pdfText = load_pdf(path)
            logger.info(f"Starting ingestion for {path.name}")
            headers = find_headers(pdfText)
            pages = remove_headers(pdfText,headers)
            pages = clean_pages(pages)
            chunks = chunk_document(pages)
            texts = [
                chunk["text"]
                for chunk in chunks
            ]
            embeddings = get_embeddings(texts)
            logger.info(f"Generated {len(embeddings)} embeddings")

            #check if the document is already stored
            if self.vector.if_existing(document_id):
                logger.warning(f"{document_id} already exists")
            else:
                self.vector.store_doc(chunks,embeddings,document_id)
        except Exception:
            logger.exception("Ingestion Failed")
            raise


    def ask_docq(self,question:str,filename:str) -> str:
        try:
            results = self.vector.search_doc(question,TOP_K,filename)
            chunks = contextBuilder(result=results)
            logger.info(f"Retrieved {len(chunks)} chunks")
            prompt = build_prompt(question=question,chunks=chunks)
            answer = self.llm.generate(prompt=prompt)
            return answer
        except Exception:
            logger.exception("Question Answering Failed")
            raise