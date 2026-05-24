from embeddings.embedding import get_embeddings
from ingestion.pdf_loader import load_pdf, pdf_path

# emb = get_embeddings(["Hello world"])
pdf_text = load_pdf(pdf_path)
print(pdf_text)