import os

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .supabase_client import get_supabase, ensure_bucket


@api_view(["GET"])
@permission_classes([AllowAny])
def storage_health(request):
    bucket = os.getenv("SUPABASE_BUCKET", "uploads")
    try:
        client = get_supabase()
        buckets = client.storage.list_buckets()
        names = {b["name"] for b in buckets}
        if bucket not in names:
            ensure_bucket(bucket)
            buckets = client.storage.list_buckets()
            names = {b["name"] for b in buckets}
        can_list = bucket in names
        return Response({"ok": True, "bucket": bucket, "canList": can_list})
    except Exception:
        return Response({"ok": False, "error": "Supabase credentials invalid or misformatted"}, status=400)
