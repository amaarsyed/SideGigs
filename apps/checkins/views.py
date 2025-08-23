import hashlib
import secrets
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction

from .models import CheckIn
from .serializers import CheckInSerializer, CheckInStartSerializer, CheckInEndSerializer
from apps.jobs.models import Job


class CheckInViewSet(viewsets.ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CheckIn.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'start':
            return CheckInStartSerializer
        elif self.action == 'end':
            return CheckInEndSerializer
        return CheckInSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def start(self, request):
        """Start a job check-in using QR hash"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        qr_hash = serializer.validated_data['qr_hash']
        
        # Find job by QR hash
        try:
            job = Job.objects.get(assigned_to=request.user, status=Job.ASSIGNED)
        except Job.DoesNotExist:
            return Response(
                {'error': 'No assigned job found for this user'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if QR hash matches (simplified - in real app, you'd validate the hash)
        # For now, we'll generate a hash based on job ID and user
        expected_hash = self._generate_qr_hash(job, request.user)
        
        if qr_hash != expected_hash:
            return Response(
                {'error': 'Invalid QR code'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already checked in
        existing_checkin = CheckIn.objects.filter(
            job=job, 
            user=request.user, 
            ended_at__isnull=True
        ).first()
        
        if existing_checkin:
            return Response(
                {'error': 'Already checked in to this job'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Create check-in
            checkin = CheckIn.objects.create(
                job=job,
                user=request.user,
                qr_hash=qr_hash
            )
            
            # Update job status
            job.status = Job.IN_PROGRESS
            job.save()
        
        return Response(CheckInSerializer(checkin).data)
    
    @action(detail=True, methods=['post'])
    def end(self, request, pk=None):
        """End a job check-in"""
        checkin = get_object_or_404(CheckIn, pk=pk, user=request.user, ended_at__isnull=True)
        
        with transaction.atomic():
            checkin.ended_at = timezone.now()
            checkin.save()
            
            # Job status remains IN_PROGRESS until completion
        
        return Response(CheckInSerializer(checkin).data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active check-in for current user"""
        active_checkin = CheckIn.objects.filter(
            user=request.user,
            ended_at__isnull=True
        ).first()
        
        if active_checkin:
            return Response(CheckInSerializer(active_checkin).data)
        else:
            return Response({'message': 'No active check-in'})
    
    def _generate_qr_hash(self, job, user):
        """Generate QR hash for a job-user combination"""
        # In a real implementation, this would be more secure
        # For now, using a simple hash of job ID + user ID
        hash_input = f"{job.id}-{user.id}-{job.assigned_to_id}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
