from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.me, name='me'),
    
    # Verification
    path('verification/submit/', views.submit_verification, name='submit_verification'),
    path('verification/me/', views.get_verification, name='get_verification'),
    path('verification/approve/<int:user_id>/', views.approve_verification, name='approve_verification'),
]
