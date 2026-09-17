from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import create_client
from gotrue.types import User
from dotenv import load_dotenv
from typing import Optional, Any
import asyncio
import logging
import os

load_dotenv()

logger = logging.getLogger(__name__)

# ── Validate env variables at startup before creating client ──
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is not set in environment variables.")
if not SUPABASE_SERVICE_KEY:
    raise RuntimeError("SUPABASE_SERVICE_KEY is not set in environment variables.")

# ── Create Supabase admin client (service key bypasses RLS) ──
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# ── auto_error=False lets us handle missing header ourselves ──
security = HTTPBearer(auto_error=False)


def _extract_user(response: Any) -> Optional[User]:
    """
    Safely extracts the User object from a Supabase get_user response.
    Handles different response shapes across supabase-py versions.
    Returns None if the user cannot be extracted.
    """
    try:
        # supabase-py v2 — response.user directly
        user: Optional[User] = getattr(response, "user", None)
        if user is not None:
            return user

        # Some versions nest under response.data.user
        data: Any = getattr(response, "data", None)
        if data is not None:
            user = getattr(data, "user", None)
            if user is not None:
                return user

    except Exception:
        pass

    return None


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
) -> User:
    """
    Reads the Bearer token from the Authorization header,
    verifies it with Supabase, and returns the user object.
    Raises 401 if the header is missing, malformed, or token is invalid.
    """

    # Guard against missing Authorization header
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token: str = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token is empty.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Run the sync Supabase call in a threadpool
    # so it does not block the async event loop
    try:
        response: Any = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: supabase.auth.get_user(token),
        )

    except Exception as exc:
        logger.error("Supabase get_user call failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed. Please sign in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user safely — outside the broad except so
    # HTTPException is never swallowed
    user: Optional[User] = _extract_user(response)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token. Please sign in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
