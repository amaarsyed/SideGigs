from django.db import models

class EmployerScreen(models.Model):
    email = models.EmailField(blank=True)
    input = models.JSONField(default=dict)        # raw request you sent
    score = models.PositiveIntegerField()
    rating = models.CharField(max_length=10)
    reasons = models.JSONField(default=list)
    next_steps = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email or 'unknown'} • {self.rating} • {self.score}"
