from rest_framework import serializers
from .models import CheckIn


class CheckInSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = CheckIn
        fields = [
            'id', 'job', 'job_title', 'user', 'user_username',
            'qr_hash', 'started_at', 'ended_at', 'is_active'
        ]
        read_only_fields = ['user', 'started_at', 'ended_at']


class CheckInStartSerializer(serializers.Serializer):
    qr_hash = serializers.CharField(max_length=64)


class CheckInEndSerializer(serializers.Serializer):
    pass  # No additional fields needed for ending a check-in
