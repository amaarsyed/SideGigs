from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'assigned_to', 'status', 'price_cents', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'owner__username', 'assigned_to__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'description', 'location_hash', 'status')
        }),
        ('Financial', {
            'fields': ('price_cents', 'scope_json')
        }),
        ('Media', {
            'fields': ('before_photos', 'after_photos')
        }),
        ('Relationships', {
            'fields': ('owner', 'assigned_to')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
