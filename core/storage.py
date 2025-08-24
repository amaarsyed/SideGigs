import os
import uuid
from pathlib import Path

from django.core.files.uploadedfile import UploadedFile

from .supabase_client import upload_bytes, create_signed_url, guess_mime


def _ext(filename: str) -> str:
    return Path(filename).suffix.lstrip('.')


def store_django_file(file: UploadedFile, folder: str, user_id: int, bucket_env: str = "SUPABASE_BUCKET"):
    data = file.read()
    ext = _ext(file.name)
    path = f"users/{user_id}/{folder}/{uuid.uuid4()}.{ext}"
    bucket = os.getenv(bucket_env, "uploads")
    content_type = file.content_type or guess_mime(path) or "application/octet-stream"
    upload_bytes(data, path, content_type, bucket=bucket)
    url = create_signed_url(path, 7200, bucket=bucket)
    return path, url


def signed_url(path: str, seconds: int = 3600) -> str:
    return create_signed_url(path, seconds)
