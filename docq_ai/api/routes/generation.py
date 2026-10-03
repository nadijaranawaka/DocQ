from fastapi import APIRouter
from api.schemas.requests import SearchRequest
from model.pipeline import Pipeline
from app.vectorstore import ChromaDB
from app.config.settings import VECTOR_PATH,COLLECTION_NAME,MODEL_GEM,TEMP
from model import GeminiModel

gen_router = APIRouter()
chroma = ChromaDB(COLLECTION_NAME, VECTOR_PATH)
llm = GeminiModel(MODEL_GEM, TEMP)
pipeline = Pipeline(llm=llm, vector=chroma)


@gen_router.post("/documents/{document_id}/answer")
async def answer_question(
    document_id:str,
    request:SearchRequest
):
    answer = pipeline.ask_docq(
        question=request.question,
        document_id=document_id
    )

    return {
        "document_id": document_id,
        "answer": answer
    }