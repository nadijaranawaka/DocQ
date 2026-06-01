from embeddings.embedding import get_embeddings
from ingestion.pdf_loader import load_pdf, pdf_path
from ingestion.parser import clean_text
from ingestion.chunker import chunk_document
from vectorstore.vectorstore import store_doc,get_documents

pdf_text = load_pdf(pdf_path)
final_text = clean_text(pdf_text) 
chunks = chunk_document(final_text)
emb = get_embeddings(chunks)
print(emb)
store_doc(chunks,emb,pdf_path.stem)
docs = get_documents()
print(docs)