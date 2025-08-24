from django.conf import settings
from django.db import models


class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    storage_path = models.CharField(max_length=255)
    signed_url = models.URLField(blank=True)
    parsed_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class IDVerification(models.Model):
    PENDING, APPROVED, REJECTED = "PENDING", "APPROVED", "REJECTED"
    STATUS_CHOICES = [(PENDING, PENDING), (APPROVED, APPROVED), (REJECTED, REJECTED)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_storage_path = models.CharField(max_length=255)
    selfie_storage_path = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=PENDING)
    reviewer_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
