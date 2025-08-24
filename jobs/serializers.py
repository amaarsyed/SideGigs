from rest_framework import serializers

from .models import Resume, IDVerification


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "storage_path", "signed_url", "parsed_json", "created_at"]
        read_only_fields = fields


class IDVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDVerification
        fields = ["status", "created_at", "reviewed_at", "reviewer_note"]
        read_only_fields = fields
