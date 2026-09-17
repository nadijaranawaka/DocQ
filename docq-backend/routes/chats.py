from fastapi import APIRouter, HTTPException, Depends, status
from supabase import create_client
from pydantic import BaseModel
from dotenv import load_dotenv
from gotrue.types import User
from typing import Any, Dict, List, Optional, cast
from auth import get_current_user
import uuid
import os

load_dotenv()

router = APIRouter()

SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is not set in environment variables.")
if not SUPABASE_SERVICE_KEY:
    raise RuntimeError("SUPABASE_SERVICE_KEY is not set in environment variables.")

assert SUPABASE_URL is not None and SUPABASE_SERVICE_KEY is not None
supabase: Any = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


class CreateChatRequest(BaseModel):
    document_id: str


# ── GET /chats ─────────────────────────────────────────────────
@router.get("", response_model=None)
async def get_chats(
    user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    try:
        response: Any = (
            supabase.table("chats")
            .select("*, documents(filename)")
            .eq("user_id", user.id)
            .order("created_at", desc=True)
            .execute()
        )

        raw_chats = getattr(response, "data", None) or []
        if not isinstance(raw_chats, list):
            return []

        chats: List[Dict[str, Any]] = []
        for chat in raw_chats:
            if not isinstance(chat, dict):
                continue
            doc: Optional[Dict[str, Any]] = chat.pop("documents", None)
            if isinstance(doc, dict):
                chat["document_filename"] = doc.get("filename", "Unknown")
            else:
                chat["document_filename"] = "Unknown"
            chats.append(chat)

        return chats

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch chats: {str(e)}",
        )


# ── POST /chats ────────────────────────────────────────────────
@router.post("", response_model=None)
async def create_chat(
    body: CreateChatRequest,
    user: User = Depends(get_current_user),
) -> Dict[str, Any]:

    # Verify the document belongs to this user
    try:
        doc_response: Any = (
            supabase.table("documents")
            .select("document_id, filename")
            .eq("document_id", body.document_id)
            .eq("user_id", user.id)
            .single()
            .execute()
        )
        document: Optional[Dict[str, Any]] = doc_response.data

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )

    try:
        chat_data: Dict[str, Any] = {
            "chat_id":     str(uuid.uuid4()),
            "user_id":     user.id,
            "document_id": body.document_id,
            "title":       "Untitled chat",
        }

        insert_response: Any = (
            supabase.table("chats").insert(chat_data).execute()
        )
        raw_chat_data = getattr(insert_response, "data", None) or []
        if not isinstance(raw_chat_data, list) or not raw_chat_data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create chat (no data returned).",
            )

        chat: Dict[str, Any] = cast(Dict[str, Any], raw_chat_data[0])
        chat["document_filename"] = document.get("filename", "Unknown")

        return chat

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create chat: {str(e)}",
        )


# ── DELETE /chats/{chat_id} ────────────────────────────────────
@router.delete("/{chat_id}", response_model=None)
async def delete_chat(
    chat_id: str,
    user: User = Depends(get_current_user),
) -> Dict[str, str]:

    try:
        check_response: Any = (
            supabase.table("chats")
            .select("chat_id")
            .eq("chat_id", chat_id)
            .eq("user_id", user.id)
            .single()
            .execute()
        )
        raw_check_data = getattr(check_response, "data", None)
        if not raw_check_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found.",
            )

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )

    try:
        supabase.table("chats").delete().eq("chat_id", chat_id).execute()
        return {"message": "Chat deleted successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete chat: {str(e)}",
        )
