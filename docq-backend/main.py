from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import Dict

from routes import documents, chats, messages, users

load_dotenv()

app = FastAPI(title="DocQ API", version="1.0.0")

# ── CORS — allow React frontend to call this API ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routes ──
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(chats.router,     prefix="/chats",     tags=["Chats"])
app.include_router(messages.router,  prefix="/chats",     tags=["Messages"])
app.include_router(users.router,     prefix="/users",     tags=["Users"])

@app.get("/", response_model=None)
def root() -> Dict[str, str]:
    return {"message": "DocQ API is running"}

@app.get("/health", response_model=None)
def health() -> Dict[str, str]:
    return {"status": "ok"}
