# utils/supabase_client.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validate environment variables
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Supabase credentials not found. "
        "Please set SUPABASE_URL and SUPABASE_KEY in your .env file"
    )

# Create Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client initialized successfully")
except Exception as e:
    print(f"Error initializing Supabase client: {e}")
    raise