from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(url, key)

def save_message(text, source="user"):
    supabase.table("memory").insert({
        "content": text,
        "source": source
    }).execute()

def get_memory(limit=10):
    response = supabase.table("memory").select("*").order("timestamp", desc=True).limit(limit).execute()
    return response.data
