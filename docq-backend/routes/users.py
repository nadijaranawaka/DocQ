from fastapi import APIRouter, HTTPException, Depends, status
from supabase import create_client
from pydantic import BaseModel
from dotenv import load_dotenv
from gotrue.types import User
from typing import Any, Dict, Optional
from auth import get_current_user
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


class UpdateProfileRequest(BaseModel):
    name: str


# ── GET /users/me ──────────────────────────────────────────────
@router.get("/me", response_model=None)
async def get_profile(
    user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    try:
        response: Any = (
            supabase.table("profiles")
            .select("*")
            .eq("id", user.id)
            .single()
            .execute()
        )
        profile_data = getattr(response, "data", None)
        if not isinstance(profile_data, dict):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found.",
            )

        return profile_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch profile: {str(e)}",
        )


# ── PUT /users/me ──────────────────────────────────────────────
@router.put("/me", response_model=None)
async def update_profile(
    body: UpdateProfileRequest,
    user: User = Depends(get_current_user),
) -> Dict[str, Any]:

    if not body.name or len(body.name.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Display name must be at least 2 characters.",
        )

    try:
        response: Any = (
            supabase.table("profiles")
            .update({"name": body.name.strip()})
            .eq("id", user.id)
            .execute()
        )
        updated_data = getattr(response, "data", None) or []
        if not isinstance(updated_data, list) or not updated_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found.",
            )

        updated: Dict[str, Any] = updated_data[0]
        return updated

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}",
        )
