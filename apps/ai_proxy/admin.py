from django.contrib import admin
from .models import EmployerScreen

@admin.register(EmployerScreen)
class EmployerScreenAdmin(admin.ModelAdmin):
    list_display = ("email", "rating", "score", "created_at")
    search_fields = ("email", "rating")
    ordering = ("-created_at",)
