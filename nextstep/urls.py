from django.contrib import admin
from django.urls import path, include

from core.views import storage_health, api_root
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    # Auth + JWT
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('accounts.urls')),
    # App APIs
    path('api/', include('jobs.urls')),
    path('api/health/storage', storage_health),
]
