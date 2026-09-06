from services.supabase.client import supabase

def download_file(storage_path:str):
    try:
        pdf_bytes = (
            supabase.storage.from_("documents").download(storage_path)
        )
        return pdf_bytes
    except Exception:
        raise