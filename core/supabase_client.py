import os
from functools import lru_cache
from supabase import create_client, Client
from decouple import config

@lru_cache(maxsize=1)
def get_supabase() -> Client:
    url = config("SUPABASE_URL")
    key = config("SUPABASE_SERVICE_ROLE")  # server-side only
    return create_client(url, key)
