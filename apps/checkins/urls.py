from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'checkins', views.CheckInViewSet, basename='checkin')

app_name = 'checkins'

urlpatterns = [
    path('', include(router.urls)),
]
