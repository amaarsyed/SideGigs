from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Verification


@receiver(post_save, sender=User)
def create_verification(sender, instance, created, **kwargs):
    """Create verification record when user is created"""
    if created:
        Verification.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_verification(sender, instance, **kwargs):
    """Save verification record when user is saved"""
    if hasattr(instance, 'verification'):
        instance.verification.save()
