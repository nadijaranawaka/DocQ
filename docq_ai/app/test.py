from pathlib import Path

from app.config.settings import (
    VECTOR_PATH,
    COLLECTION_NAME,
    MODEL_GEM,
    TEMP
)

from app.vectorstore import ChromaDB
from model import GeminiModel
from model.pipeline import Pipeline
import logging

#Instance Creation
logger = logging.getLogger("docq")


# PDF we want to test
pdf_path = Path("data/uploads/testpdf.pdf")

# Use a test document ID
document_id = "local-summary-test-4"


# Create the same components used by FastAPI
chroma = ChromaDB(
    COLLECTION_NAME,
    VECTOR_PATH
)

llm = GeminiModel(
    MODEL_GEM,
    TEMP
)

pipeline = Pipeline(
    llm=llm,
    vector=chroma
)


# 1. Process the PDF
print("Processing PDF...")

pipeline.upload_file(
    path=pdf_path,
    document_id=document_id
)
print("\n--- CHECK STORED DOCUMENT ---")

stored = chroma.collection.get(
    include=["documents", "metadatas"]
)

print("Number of stored chunks:", len(stored["documents"]))

for metadata, document in zip(
    stored["metadatas"],
    stored["documents"]
):
    if metadata.get("document_id") == document_id:
        print("\nFOUND OUR DOCUMENT")
        print("Metadata:", metadata)
        print("Text:", document[:300])

print("PDF processed successfully.")


# 2. Ask the problematic question
print("\nAsking question...")

answer = pipeline.ask_docq(
    question="What is this document about?",
    document_id=document_id
)

print("\nANSWER:")
print(answer)

print("\n--- DEBUG RETRIEVAL ---")

results = chroma.search_doc(
    question="What is this document about?",
    top_k=5,
    document_id=document_id
)

print(results)