from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .upload_views import UploadResumeView, UploadIDView

router = DefaultRouter()
router.register(r'jobs', views.JobViewSet, basename='job')

app_name = 'jobs'

urlpatterns = [
    path('', include(router.urls)),
    # File upload endpoints
    path('upload/resume/', UploadResumeView.as_view(), name='upload_resume'),
    path('upload/id/', UploadIDView.as_view(), name='upload_id'),
]
