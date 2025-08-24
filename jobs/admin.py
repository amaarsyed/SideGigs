from django import forms
from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.html import format_html

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

    class RejectForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        reviewer_note = forms.CharField(widget=forms.Textarea, label="Reviewer note")

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
        form = None

        if "apply" in request.POST:
            form = self.RejectForm(request.POST)
            if form.is_valid():
                note = form.cleaned_data["reviewer_note"]
                updated = queryset.update(
                    status=IDVerification.REJECTED,
                    reviewer_note=note,
                    reviewed_at=timezone.now(),
                )
                self.message_user(request, f"Rejected {updated} verification(s).")
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.RejectForm(
                initial={"_selected_action": request.POST.getlist(ACTION_CHECKBOX_NAME)}
            )

        return render(
            request,
            "admin/idverification_reject.html",
            {
                "form": form,
                "queryset": queryset,
                "action_checkbox_name": ACTION_CHECKBOX_NAME,
            },
        )
