from pydantic import BaseModel


class SearchRequest(BaseModel):
    question: str

class DocumentRequestModel(BaseModel):
    document_id : str
    storage_path : str