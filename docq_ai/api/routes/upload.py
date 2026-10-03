from fastapi import APIRouter, HTTPException, status
from api.schemas.requests import DocumentRequestModel
from services.supabase.download import download_file
from app.config.settings import BASE_DIR
from model.pipeline import Pipeline
from app.vectorstore import ChromaDB
from app.config.settings import VECTOR_PATH,COLLECTION_NAME,MODEL_GEM,TEMP
from model import GeminiModel

upload_router = APIRouter()

chroma = ChromaDB(COLLECTION_NAME, VECTOR_PATH)
llm = GeminiModel(MODEL_GEM, TEMP)
pipeline = Pipeline(llm=llm, vector=chroma)

@upload_router.post("/process-document")
async def process_doc(request : DocumentRequestModel):
    documentid = request.document_id
    storagePath = request.storage_path
    try:
        pdf_bytes = download_file(storagePath)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "Could not download the document from Supabase Storage. "
                "Check that SUPABASE_STORAGE_BUCKET exists and matches the "
                f"backend configuration: {exc}"
            ),
        ) from exc

    #temp store
    temp_path = BASE_DIR / "data" / "uploads" / f"{documentid}.pdf"
    temp_path.write_bytes(pdf_bytes)
    pipeline.upload_file(temp_path, documentid)
    return {
        "document_id": documentid,
        "status": "ready"
    }
    
    