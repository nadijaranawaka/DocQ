from fastapi import APIRouter, HTTPException, Depends, status
from supabase import create_client
from pydantic import BaseModel
from dotenv import load_dotenv
from gotrue.types import User
from typing import Any, Dict, List, Optional
from auth import get_current_user
import uuid
import httpx
import os
import math

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

AI_BACKEND_URL: str = os.getenv(
    "AI_BACKEND_URL",
    "http://localhost:8001"
)


class SendMessageRequest(BaseModel):
    content: str


# ── GET /chats/{chat_id}/messages ──────────────────────────────
@router.get("/{chat_id}/messages", response_model=None)
async def get_messages(
    chat_id: str,
    user: User = Depends(get_current_user),
) -> Dict[str, Any]:

    try:
        chat_response: Any = (
            supabase.table("chats")
            .select("*, documents(filename)")
            .eq("chat_id", chat_id)
            .eq("user_id", user.id)
            .single()
            .execute()
        )
        chat_data = getattr(chat_response, "data", None)
        if not isinstance(chat_data, dict):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found.",
            )
        chat: Dict[str, Any] = chat_data

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )

    try:
        msg_response: Any = (
            supabase.table("messages")
            .select("*")
            .eq("chat_id", chat_id)
            .order("created_at", desc=False)
            .execute()
        )

        doc: Optional[Dict[str, Any]] = chat.pop("documents", None)
        chat["document_filename"] = (
            doc.get("filename", "Unknown") if isinstance(doc, dict) else "Unknown"
        )

        raw_messages = getattr(msg_response, "data", None) or []
        messages: List[Dict[str, Any]] = (
            raw_messages if isinstance(raw_messages, list) else []
        )

        return {"chat": chat, "messages": messages}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch messages: {str(e)}",
        )


# ── POST /chats/{chat_id}/messages ─────────────────────────────
@router.post("/{chat_id}/messages", response_model=None)
async def send_message(
    chat_id: str,
    body: SendMessageRequest,
    user: User = Depends(get_current_user),
) -> Dict[str, Any]:

    # ── Verify chat belongs to this user and get document_id ──
    try:
        chat_response: Any = (
            supabase.table("chats")
            .select("*, documents(filename, document_id)")
            .eq("chat_id", chat_id)
            .eq("user_id", user.id)
            .single()
            .execute()
        )
        chat_data = getattr(chat_response, "data", None)
        if not isinstance(chat_data, dict):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat not found.",
            )
        chat: Dict[str, Any] = chat_data

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )

    # ── Check user has credits ──
    try:
        profile_response: Any = (
            supabase.table("profiles")
            .select("credits_remaining")
            .eq("id", user.id)
            .single()
            .execute()
        )
        profile_data = getattr(profile_response, "data", None)
        if not isinstance(profile_data, dict):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found.",
            )

        credits_remaining_raw = profile_data.get("credits_remaining")
        if not isinstance(credits_remaining_raw, int):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User profile is invalid.",
            )

        credits_remaining: int = credits_remaining_raw

        if credits_remaining <= 0:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="No credits remaining. Please upgrade your plan.",
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    # ── Save user message ──
    user_message: Dict[str, Any] = {
        "message_id": str(uuid.uuid4()),
        "chat_id":    chat_id,
        "role":       "user",
        "content":    body.content,
    }
    supabase.table("messages").insert(user_message).execute()

    # ── Extract document_id from chat ──
    documents_data = chat.get("documents")
    document_id: str = (
        str(documents_data.get("document_id", ""))
        if isinstance(documents_data, dict)
        else ""
    )

    # ── Call AI backend ──
    ai_result = await _get_ai_answer(
        question=body.content,
        document_id=document_id,
    )

    ai_answer = ai_result["answer"]
    usage = ai_result["usage"]

    # # ── Save AI response ──
    ai_message: Dict[str, Any] = {
        "message_id": str(uuid.uuid4()),
        "chat_id":    chat_id,
        "role":       "assistant",
        "content":    ai_answer,
    }
    supabase.table("messages").insert(ai_message).execute()

    # Calculate credits based on actual token usage
    total_tokens = usage["total_tokens"]
    credits_to_deduct = max(1, math.ceil(total_tokens / 1000))

    if credits_to_deduct > credits_remaining:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient credits for this request."
        )

    # Never allow the balance to become negative
    new_balance = max(0, credits_remaining - credits_to_deduct)

    supabase.table("profiles").update(
        {"credits_remaining": new_balance}
    ).eq("id", user.id).execute()

    return {
    "user_message": user_message,
    "assistant_message": ai_message,
    "usage": usage,
    "credits_deducted": credits_to_deduct,
    "credits_remaining": new_balance
}

async def _get_ai_answer(
    question: str,
    document_id: str,
) -> Dict[str, Any]:

    if not document_id:
        raise HTTPException(
            status_code=400,
            detail="Could not find the document linked to this chat."
        )

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{AI_BACKEND_URL}/documents/{document_id}/answer",
                json={"question": question},
            )

            response.raise_for_status()

            result = response.json()

            answer = result.get("answer")
            usage = result.get("usage")

            if not isinstance(answer, str) or not answer.strip():
                raise HTTPException(
                    status_code=502,
                    detail="AI backend returned an invalid answer."
                )

            if not isinstance(usage, dict):
                raise HTTPException(
                    status_code=502,
                    detail="AI backend did not return token usage."
                )

            return {
                "answer": answer,
                "usage": usage
            }

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI backend returned status {e.response.status_code}."
        )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="AI backend request timed out."
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="AI backend is currently unavailable."
        )