# from embeddings.embedding import get_embeddings
# from ingestion.pdf_loader import load_pdf, pdf_path
# from ingestion.parser import clean_text
# from ingestion.chunker import chunk_document
from model.model import chatbot

# emb = get_embeddings(["Hello world"])
# pdf_text = load_pdf(pdf_path)
# final_text = clean_text(pdf_text) 
# chunks = chunk_document(final_text)
# print(chunks)
chatbot()