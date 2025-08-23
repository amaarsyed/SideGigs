from django.db import models
from django.conf import settings


class Job(models.Model):
    DRAFT, OPEN, ASSIGNED, IN_PROGRESS, DONE = "draft", "open", "assigned", "in_progress", "done"
    STATUS_CHOICES = [
        (DRAFT, "Draft"),
        (OPEN, "Open"),
        (ASSIGNED, "Assigned"),
        (IN_PROGRESS, "In Progress"),
        (DONE, "Done")
    ]
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted_jobs")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="taken_jobs")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    location_hash = models.CharField(max_length=128)
    price_cents = models.IntegerField(default=0)
    scope_json = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    before_photos = models.JSONField(default=list)
    after_photos = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.status}"
    
    @property
    def price_dollars(self):
        return self.price_cents / 100
