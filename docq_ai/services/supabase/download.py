from services.supabase.client import supabase

def download_file(storage_path: str) -> bytes:
    print("PATH BEING DOWNLOADED:", storage_path)

    files = supabase.storage.from_("documents").list(
        "2f85c132-232a-45d1-bfe8-448e21232d81"
    )

    print("FILES IN FOLDER:")
    for file in files:
        print(file)

    return supabase.storage.from_("documents").download(storage_path)