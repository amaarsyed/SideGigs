from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core.storage import store_django_file, signed_url
from .models import Resume, IDVerification
from .resume_parse import parse_resume


@api_view(["POST"])
def upload_resume(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"detail": "file required"}, status=400)
    data = file.read()
    file_copy = SimpleUploadedFile(file.name, data, file.content_type)
    path, url = store_django_file(file_copy, "resumes", request.user.id)
    parsed = parse_resume(data, file.name)
    resume = Resume.objects.create(user=request.user, storage_path=path, signed_url=url, parsed_json=parsed)
    return Response({"id": resume.id, "signed_url": url, "parsed": parsed}, status=201)


@api_view(["POST"])
def upload_id(request):
    id_image = request.FILES.get("id_image")
    if not id_image:
        return Response({"detail": "id_image required"}, status=400)
    allowed_types = {"image/jpeg", "image/png"}
    if id_image.content_type not in allowed_types:
        return Response({"detail": "unsupported id_image type"}, status=400)
    selfie = request.FILES.get("selfie")
    if selfie and selfie.content_type not in allowed_types:
        return Response({"detail": "unsupported selfie type"}, status=400)
    id_path, _ = store_django_file(id_image, "id", request.user.id)
    selfie_path = ""
    if selfie:
        selfie_path, _ = store_django_file(selfie, "selfie", request.user.id)
    IDVerification.objects.create(user=request.user, id_storage_path=id_path, selfie_storage_path=selfie_path)
    return Response({"status": "PENDING"}, status=201)


@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def get_signed_url(request):
    path = request.query_params.get("path")
    if not path:
        return Response({"detail": "path required"}, status=400)
    url = signed_url(path, 3600)
    return Response({"url": url})
