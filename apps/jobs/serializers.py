from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    price_dollars = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'id', 'owner', 'owner_username', 'assigned_to', 'assigned_to_username',
            'title', 'description', 'location_hash', 'price_cents', 'price_dollars',
            'scope_json', 'status', 'before_photos', 'after_photos',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'assigned_to', 'price_cents', 'scope_json', 'status']


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location_hash', 'before_photos']


class SnapquoteSerializer(serializers.Serializer):
    media_urls = serializers.ListField(child=serializers.URLField())


class JobAcceptSerializer(serializers.Serializer):
    pass  # No additional fields needed for accepting a job


class JobCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['after_photos']
