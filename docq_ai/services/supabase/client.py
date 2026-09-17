from supabase import create_client,Client
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger("docq")

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
if not supabase_url:
    logger.error("No Supabase URL")
    raise ValueError("Supabase URL not found")

supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
if not supabase_key:
    logger.error("No Supabase key")
    raise ValueError("Supabase Key not found")

supabase:Client = create_client(supabase_url,supabase_key)
logger.info("Supabase Working")
