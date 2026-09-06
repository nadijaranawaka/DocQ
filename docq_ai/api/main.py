from fastapi import FastAPI
from api.routes.retrieval import router
from api.routes.upload import upload_router

app = FastAPI()

@app.get("/")
def root():
    return {"message":"DOCQ API is running"}

app.include_router(router)
app.include_router(upload_router)