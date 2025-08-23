from django.contrib import admin
from .models import Escrow


@admin.register(Escrow)
class EscrowAdmin(admin.ModelAdmin):
    list_display = ('job', 'amount_cents', 'status', 'created_at', 'released_at')
    list_filter = ('status', 'created_at', 'released_at')
    search_fields = ('job__title', 'stripe_payment_intent_id')
    readonly_fields = ('created_at',)
