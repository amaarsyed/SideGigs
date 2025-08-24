import os
import uuid
import mimetypes
from core.supabase_client import get_supabase
from decouple import config
from typing import Tuple

BUCKET = config("SUPABASE_BUCKET", default="uploads")

def _guess_ct(path: str) -> str | None:
    return mimetypes.guess_type(path)[0]

def upload_django_file(django_file, folder: str, user_id: int, upsert: bool=False) -> Tuple[str, str]:
    """
    Returns (storage_path, signed_url)
    storage_path example: users/123/resumes/a1b2c3.pdf
    """
    sb = get_supabase()
    ext = (django_file.name.split(".")[-1] or "bin").lower()
    storage_path = f"users/{user_id}/{folder}/{uuid.uuid4()}.{ext}"
    content_type = _guess_ct(storage_path)

    # read bytes (important: read() consumes the stream)
    data = django_file.read()

    # Upload to private bucket
    sb.storage.from_(BUCKET).upload(
        path=storage_path,
        file=data,
        file_options={"content-type": content_type, "cache-control": "max-age=3600"}
    )

    # Create a short-lived signed URL (2 hours) for preview/download
    signed = sb.storage.from_(BUCKET).create_signed_url(storage_path, expires_in=60*60*2)
    signed_url = signed.get("signedURL") or signed.get("signed_url") or ""

    return storage_path, signed_url
