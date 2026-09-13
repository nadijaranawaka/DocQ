from fastapi import FastAPI
from api.routes.upload import upload_router
from api.routes.generation import gen_router
from app.config import logConfig
import logging

#Instance Creation
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def root():
    return {"message":"DOCQ API is running"}

app.include_router(upload_router)
app.include_router(gen_router)