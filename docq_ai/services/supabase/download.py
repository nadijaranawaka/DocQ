import os

from services.supabase.client import supabase


BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "documents")


def download_file(storage_path: str) -> bytes:
    return supabase.storage.from_(BUCKET).download(storage_path)