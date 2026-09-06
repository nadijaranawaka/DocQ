from supabase import create_client,Client
from dotenv import load_dotenv
import os

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
if not supabase_url:
            raise ValueError("Supabase URL not found")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
if not supabase_key:
            raise ValueError("Supabase Key not found")

supabase:Client = create_client(supabase_url,supabase_key)
