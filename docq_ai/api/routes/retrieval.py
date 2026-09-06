from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SearchRequest(BaseModel):
    question : str

@router.get("/search/")
def search():
    return {"documentID":"123","text":"I love you"}