from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Verification


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_minor', 'is_staff')
    list_filter = ('is_minor', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('is_minor', 'guardian_email')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('is_minor', 'guardian_email')}),
    )


@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'guardian_consented')
    list_filter = ('status', 'guardian_consented')
    search_fields = ('user__username', 'user__email')
