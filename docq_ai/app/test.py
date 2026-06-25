from app.embeddings.embedding import get_embeddings
from app.ingestion.pdf_loader import load_pdf, pdf_path
from app.ingestion.parser import clean_text
from app.ingestion.chunker import chunk_document
from app.vectorstore.vectorstore import store_doc,get_documents,preview_chunks,if_existing,delete_collection,print_metadata
from app.retrieval.retrieval import search_doc

# delete_collection()

pdf_text = load_pdf(pdf_path)
final_text = clean_text(pdf_text) 
chunks = chunk_document(final_text)
emb = get_embeddings(chunks)
print(emb)
if if_existing(pdf_path.stem):
    print("Document Already Exists")
else:
    store_doc(chunks,emb,pdf_path.stem)
docs = get_documents()
print_metadata()
# print(docs)
vector_test = preview_chunks()
# print(vector_test)
question = "What is regression?"

response = search_doc(question)
print(response["documents"][0])