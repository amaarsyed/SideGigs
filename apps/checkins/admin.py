from django.contrib import admin
from .models import CheckIn


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'qr_hash', 'started_at', 'ended_at', 'is_active')
    list_filter = ('started_at', 'ended_at')
    search_fields = ('job__title', 'user__username', 'qr_hash')
    readonly_fields = ('started_at',)
    
    fieldsets = (
        ('Check-in Information', {
            'fields': ('job', 'user', 'qr_hash')
        }),
        ('Timestamps', {
            'fields': ('started_at', 'ended_at')
        }),
    )
