from django.contrib import admin
from django.urls import path, include

from core.views import storage_health, api_root

urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('jobs.urls')),
    path('api/health/storage', storage_health),
]
