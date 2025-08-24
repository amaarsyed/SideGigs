from django.urls import path

from .views import upload_resume, upload_id, get_signed_url

urlpatterns = [
    path('storage/resume', upload_resume),
    path('storage/id', upload_id),
    path('storage/signed-url', get_signed_url),
]
