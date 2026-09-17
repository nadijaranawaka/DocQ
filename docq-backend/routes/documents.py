from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from supabase import create_client
from dotenv import load_dotenv
from gotrue.types import User
from typing import Any, Dict, List, Optional
from auth import get_current_user
import uuid
import os

load_dotenv()

router = APIRouter()

# ── Fix 1: Validate env vars before passing to create_client ──
# os.getenv() returns str | None — create_client needs str
# asserting after the None check satisfies Pylance
SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is not set in environment variables.")
if not SUPABASE_SERVICE_KEY:
    raise RuntimeError("SUPABASE_SERVICE_KEY is not set in environment variables.")

# Narrow types for the type checker
assert SUPABASE_URL is not None and SUPABASE_SERVICE_KEY is not None

# Now both are guaranteed str — narrow with assert above; use Any to avoid missing stubs
supabase: Any = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

BUCKET = "documents"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

# AI backend base URL — runs on 8001
AI_BACKEND_URL: str = os.getenv("AI_BACKEND_URL", "http://localhost:8001")


# ── GET /documents ─────────────────────────────────────────────
@router.get("", response_model=None)
async def get_documents(
    user: User = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    try:
        # Fix 2: annotate response as Any to silence APIResponse[Unknown]
        response: Any = (
            supabase.table("documents")
            .select("*")
            .eq("user_id", user.id)
            .order("uploaded_at", desc=True)
            .execute()
        )
        data: List[Dict[str, Any]] = response.data or []
        return data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch documents: {str(e)}",
        )


# ── POST /documents/upload ─────────────────────────────────────
@router.post("/upload", response_model=None)
async def upload_document(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
) -> Dict[str, Any]:

    # Fix 3: file.content_type is str | None — guard before comparing
    content_type: Optional[str] = file.content_type
    if content_type is None or content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    # Read file content
    content: bytes = await file.read()

    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 100 MB limit.",
        )

    # Generate a unique document ID
    document_id: str = str(uuid.uuid4())

    # Fix 4: file.filename is str | None — guard before calling .replace()
    original_filename: Optional[str] = file.filename
    if not original_filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must have a valid filename.",
        )

    safe_filename: str = original_filename.replace(" ", "_")
    storage_path: str = f"{user.id}/{document_id}_{safe_filename}"

    # ── 1. Upload to Supabase Storage ──
    try:
        supabase.storage.from_(BUCKET).upload(
            path=storage_path,
            file=content,
            file_options={"content-type": "application/pdf"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file to storage: {str(e)}",
        )

    # ── 2. Write metadata to documents table ──
    try:
        doc_data: Dict[str, Any] = {
            "document_id": document_id,
            "user_id": user.id,
            "filename": original_filename,
            "storage_path": storage_path,
            "status": "uploaded",
        }

        insert_response: Any = supabase.table("documents").insert(doc_data).execute()
        data_list = getattr(insert_response, "data", None) or []
        if not data_list:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save document record (no data returned).",
            )
        document: Dict[str, Any] = data_list[0]

    except Exception as e:
        # If DB write fails, clean up the uploaded file
        try:
            supabase.storage.from_(BUCKET).remove([storage_path])
        except Exception:
            pass

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save document record: {str(e)}",
        )

        # ── 3. Trigger AI backend to process the document ──
    # This runs after we return the document to the frontend
    # so the user sees the document immediately without waiting
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            ai_response = await client.post(
                f"{AI_BACKEND_URL}/process-document",
                json={
                    "document_id": document_id,
                    "storage_path": storage_path,
                },
            )

            # If AI backend confirms ready, update status in DB
            if ai_response.status_code == 200:
                ai_data: Dict[str, Any] = ai_response.json()
                new_status: str = ai_data.get("status", "processing")

                supabase.table("documents").update({"status": new_status}).eq(
                    "document_id", document_id
                ).execute()

                document["status"] = new_status
            else:
                # AI backend returned error — mark as failed
                supabase.table("documents").update({"status": "failed"}).eq(
                    "document_id", document_id
                ).execute()

                document["status"] = "failed"

    except Exception:
        # AI backend unreachable — leave status as processing
        # The AI team can update it to ready/failed when done
        pass

    return document


# ── DELETE /documents/{document_id} ───────────────────────────
@router.delete("/{document_id}", response_model=None)
async def delete_document(
    document_id: str,
    user: User = Depends(get_current_user),
) -> Dict[str, str]:

    # ── 1. Fetch document to get storage_path ──
    try:
        fetch_response: Any = (
            supabase.table("documents")
            .select("*")
            .eq("document_id", document_id)
            .eq("user_id", user.id)
            .single()
            .execute()
        )
        document: Optional[Dict[str, Any]] = fetch_response.data

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

    # ── 2. Delete from Supabase Storage ──
    try:
        storage_path: str = document["storage_path"]
        supabase.storage.from_(BUCKET).remove([storage_path])
    except Exception:
        pass  # Continue even if storage delete fails

    # ── 3. Delete from documents table ──
    try:
        supabase.table("documents").delete().eq("document_id", document_id).execute()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete document record: {str(e)}",
        )

    return {"message": "Document deleted successfully"}
