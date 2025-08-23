from django.db import models
from django.conf import settings
from apps.jobs.models import Job


class Escrow(models.Model):
    """
    Escrow model for holding payments until job completion.
    Your teammate will implement the full escrow functionality.
    """
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="escrow")
    amount_cents = models.IntegerField()
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Escrow for {self.job.title} - ${self.amount_cents/100}"
