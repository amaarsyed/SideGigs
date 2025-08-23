from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_minor = models.BooleanField(default=False)
    guardian_email = models.EmailField(blank=True, null=True)


class Verification(models.Model):
    PENDING, VERIFIED, REJECTED = "pending", "verified", "rejected"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (VERIFIED, "Verified"),
        (REJECTED, "Rejected")
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="verification")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    guardian_consented = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.status}"
