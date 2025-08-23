from django.db import models
from django.conf import settings
from apps.jobs.models import Job


class CheckIn(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="checkins")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    qr_hash = models.CharField(max_length=64)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.job.title} - {self.user.username} - {self.started_at}"
    
    @property
    def is_active(self):
        return self.ended_at is None
