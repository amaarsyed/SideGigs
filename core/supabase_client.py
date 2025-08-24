import mimetypes
import os
from functools import lru_cache


@lru_cache(maxsize=1)
def get_supabase():
    from supabase import create_client

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE")
    if not url or not key:
        raise RuntimeError("Supabase credentials not configured")
    return create_client(url, key)


def guess_mime(path: str) -> str | None:
    return mimetypes.guess_type(path)[0]


def upload_bytes(data: bytes, path: str, content_type: str | None = None, *, bucket: str | None = None) -> None:
    client = get_supabase()
    bucket_name = bucket or os.getenv("SUPABASE_BUCKET", "uploads")
    if content_type is None:
        content_type = guess_mime(path) or "application/octet-stream"
    # Supabase expects camelCase keys such as `contentType` and `cacheControl`
    options = {
        "contentType": content_type,
        "cacheControl": "3600",
    }
    client.storage.from_(bucket_name).upload(path, data, options)


def create_signed_url(path: str, seconds: int = 7200, *, bucket: str | None = None) -> str:
    client = get_supabase()
    bucket_name = bucket or os.getenv("SUPABASE_BUCKET", "uploads")
    return client.storage.from_(bucket_name).create_signed_url(path, seconds)["signedURL"]


def ensure_bucket(bucket: str) -> None:
    client = get_supabase()
    existing = {b["name"] for b in client.storage.list_buckets()}
    if bucket not in existing:
        client.storage.create_bucket(bucket, {"public": False})
