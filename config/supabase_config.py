# config/supabase_config.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    _instance = None
    
    @classmethod
    def get_client(cls):
        if cls._instance is None:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
            if not supabase_url or not supabase_key:
                raise ValueError("Supabase credentials not found in environment variables")
            cls._instance = create_client(supabase_url, supabase_key)
        return cls._instance

def get_supabase():
    return SupabaseClient.get_client()