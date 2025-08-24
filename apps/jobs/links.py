import os
from core.supabase_client import get_supabase
from decouple import config

BUCKET = config("SUPABASE_BUCKET", default="uploads")

def signed_url(path: str, seconds=3600) -> str:
    sb = get_supabase()
    res = sb.storage.from_(BUCKET).create_signed_url(path, seconds)
    return res.get("signedURL") or ""
