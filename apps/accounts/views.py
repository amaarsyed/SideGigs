from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from .models import User, Verification
from .serializers import (
    RegisterSerializer, UserSerializer, LoginSerializer,
    VerificationSubmitSerializer, VerificationSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """Get current user info"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_verification(request):
    """Submit verification documents"""
    verification = request.user.verification
    serializer = VerificationSubmitSerializer(verification, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return Response({
        'message': 'Verification submitted successfully',
        'status': verification.status
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_verification(request):
    """Get current user's verification status"""
    verification = request.user.verification
    serializer = VerificationSerializer(verification)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def approve_verification(request, user_id):
    """Admin approve user verification"""
    user = get_object_or_404(User, id=user_id)
    verification = user.verification
    
    verification.status = Verification.VERIFIED
    verification.save()
    
    return Response({
        'message': f'User {user.username} verified successfully',
        'status': verification.status
    })
