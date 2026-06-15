from embeddings.embedding import get_embeddings
from ingestion.pdf_loader import load_pdf, pdf_path
from ingestion.parser import clean_text
from ingestion.chunker import chunk_document
from vectorstore.vectorstore import store_doc,get_documents,preview_chunks,if_existing,delete_collection,print_metadata
from retrieval.retrieval import search_doc
from config import logConfig
import logging

#logger object 
logger = logging.getLogger(__name__)

# delete_collection()

pdf_text = load_pdf(pdf_path)
final_text = clean_text(pdf_text) 
chunks = chunk_document(final_text)
emb = get_embeddings(chunks)
if if_existing(pdf_path.stem):
    logger.info("Document Already Exist")
else:
    store_doc(chunks,emb,pdf_path.stem)
get_documents()
print_metadata()
vector_test = preview_chunks()
question = "What is regression?"

response = search_doc(question)
logger.info(f"Received {len(response['documents'][0])} chunks from the search")