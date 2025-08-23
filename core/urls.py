"""
URL configuration for job platform backend.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.http import JsonResponse

def api_root(request):
    """API root endpoint showing available endpoints"""
    return JsonResponse({
        'message': 'Job Platform Backend API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'accounts': {
                'register': '/api/accounts/register/',
                'login': '/api/accounts/login/',
                'me': '/api/accounts/me/',
                'verification_submit': '/api/accounts/verification/submit/',
                'verification_me': '/api/accounts/verification/me/',
                'verification_approve': '/api/accounts/verification/approve/{user_id}/',
                'token_refresh': '/api/accounts/token/refresh/',
            }
        }
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    # path('api/', include('apps.jobs.urls')),
    # path('api/', include('apps.checkins.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
]

#  media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
