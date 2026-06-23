from app.config.settings import TOP_K
from model.prompt_builder import build_prompt
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.parser import clean_text
from app.ingestion.chunker import chunk_document
from app.embeddings.embedding import get_embeddings
import logging

logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self,llm,vector):
        self.llm = llm
        self.vector = vector
    
    def upload_file(self,path):
        pdfText = load_pdf(path)
        finalText = clean_text(pdfText)
        chunks = chunk_document(finalText)
        embeddings = get_embeddings(chunks)
        
        #check if the document is already stored
        if self.vector.if_existing(path.stem):
            logger.info("Document Already Exist")
        else:
            self.vector.store_doc(chunks,embeddings,path.stem)


    def ask_docq(self,question):
        results = self.vector.search_doc(question,TOP_K)
        chunks = results['documents'][0]
        prompt = build_prompt(question=question,chunks=chunks)
        answer = self.llm.get_response(prompt=prompt)
        return answer