from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Job
from .serializers import (
    JobSerializer, JobCreateSerializer, SnapquoteSerializer,
    JobAcceptSerializer, JobCompleteSerializer
)
from apps.ai_proxy.client import snapquote
from apps.common.permissions import IsVerified


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Job.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return JobCreateSerializer
        elif self.action == 'snapquote':
            return SnapquoteSerializer
        elif self.action == 'accept':
            return JobAcceptSerializer
        elif self.action == 'complete':
            return JobCompleteSerializer
        return JobSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def snapquote(self, request, pk=None):
        """Get AI-powered quote for a job"""
        job = self.get_object()
        
        if job.status != Job.DRAFT:
            return Response(
                {'error': 'Job must be in draft status to get snapquote'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        media_urls = serializer.validated_data['media_urls']
        
        # Call AI service for snapquote
        try:
            quote_data = snapquote(media_urls)
            
            # Update job with quote data
            job.price_cents = quote_data.get('price_cents', 0)
            job.scope_json = {
                'eta_minutes': quote_data.get('eta_minutes', 0),
                'checklist': quote_data.get('checklist', []),
                'confidence': quote_data.get('confidence', 0.0)
            }
            job.status = Job.OPEN
            job.save()
            
            return Response(JobSerializer(job).data)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to get snapquote: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsVerified])
    def accept(self, request, pk=None):
        """Accept a job assignment"""
        job = get_object_or_404(Job, pk=pk, status=Job.OPEN)
        
        if job.owner == request.user:
            return Response(
                {'error': 'Cannot accept your own job'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            job.assigned_to = request.user
            job.status = Job.ASSIGNED
            job.save()
            
            # Generate QR hash for check-ins (will be implemented in checkins app)
            # This is a placeholder - your teammate will implement the QR generation
            
        return Response(JobSerializer(job).data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a job with after photos"""
        job = get_object_or_404(Job, pk=pk, status=Job.IN_PROGRESS)
        
        if job.assigned_to != request.user:
            return Response(
                {'error': 'Only the assigned worker can complete this job'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            job.after_photos = serializer.validated_data.get('after_photos', [])
            job.status = Job.DONE
            job.save()
            
            # Release escrow (will be implemented in payments app)
            # This is a placeholder - your teammate will implement the escrow release
            
        return Response(JobSerializer(job).data)
