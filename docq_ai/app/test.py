from app.ingestion.pdf_loader import pdf_path
from app.config.settings import VECTOR_PATH,COLLECTION_NAME,MODEL_GEM,TEMP
from app.config import logConfig
from model.pipeline import Pipeline
from app.vectorstore import ChromaDB
from model import GeminiModel
import logging

#Instance Creation
logger = logging.getLogger(__name__)
chroma = ChromaDB(COLLECTION_NAME,VECTOR_PATH)
llm = GeminiModel(MODEL_GEM,TEMP)
pipeline = Pipeline(llm=llm,vector=chroma)
pipeline.upload_file(pdf_path)
chroma.print_metadata()
# question = "What is regression?"
# answer = pipeline.ask_docq(question)
# print(answer)