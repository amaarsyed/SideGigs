from rest_framework import permissions, views, response
from .models import Resume, IDVerification
from .storage_supabase import upload_django_file
from .resume_parse import parse_resume_file

class UploadResumeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        f = request.FILES.get("file")
        if not f:
            return response.Response({"error": "file required"}, status=400)
        
        # Parse the resume first (before uploading)
        parsed = parse_resume_file(f)
        
        # Reset file pointer for upload
        f.seek(0)
        
        path, url = upload_django_file(f, "resumes", request.user.id)
        
        rec = Resume.objects.create(
            user=request.user,
            storage_path=path,
            download_url=url,
            parsed_json=parsed
        )
        
        return response.Response({
            "id": rec.id, 
            "download_url": url, 
            "parsed": parsed
        }, status=201)

class UploadIDView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        id_img = request.FILES.get("id_image")
        selfie = request.FILES.get("selfie")
        
        if not id_img:
            return response.Response({"error": "id_image required"}, status=400)
        
        id_path, id_url = upload_django_file(id_img, "id", request.user.id)
        selfie_path, _ = ("", "")
        
        if selfie:
            selfie_path, _ = upload_django_file(selfie, "selfie", request.user.id)
        
        rec = IDVerification.objects.create(
            user=request.user,
            id_storage_path=id_path,
            selfie_storage_path=selfie_path
        )
        
        return response.Response({
            "status": rec.status, 
            "preview": id_url
        }, status=201)
