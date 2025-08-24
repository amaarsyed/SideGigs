from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

from core.storage import signed_url
from .models import Resume, IDVerification


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")


@admin.register(IDVerification)
class IDVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "created_at", "reviewed_at")
    list_filter = ("status",)
    readonly_fields = ("id_preview", "selfie_preview", "created_at", "reviewed_at")
    actions = ["approve", "reject"]

    def id_preview(self, obj):
        if obj.id_storage_path:
            url = signed_url(obj.id_storage_path)
            return format_html('<img src="{}" width="150" />', url)
        return ""

    def selfie_preview(self, obj):
        if obj.selfie_storage_path:
            url = signed_url(obj.selfie_storage_path)
            return format_html('<img src="{}" width="150" />', url)
        return ""

    def approve(self, request, queryset):
        queryset.update(status=IDVerification.APPROVED, reviewed_at=timezone.now())

    def reject(self, request, queryset):
        queryset.update(status=IDVerification.REJECTED, reviewed_at=timezone.now())
