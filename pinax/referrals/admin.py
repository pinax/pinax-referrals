from django.contrib import admin

from .models import Referral, ReferralResponse


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "code",
        "label",
        "redirect_to",
        "target_content_type",
        "target_object_id"
    ]
    readonly_fields = ["code", "created_at"]
    list_filter = ["target_content_type", "created_at"]
    search_fields = ["user__first_name", "user__last_name", "user__email", "user__username", "code"]


@admin.register(ReferralResponse)
class ReferralResponseAdmin(admin.ModelAdmin):
    list_display = [
        "referral",
        "session_key",
        "user",
        "ip_address",
        "action"
    ]
    readonly_fields = ["referral", "session_key", "user", "ip_address", "action"]
    list_filter = ["action", "created_at"]
    search_fields = ["referral__code", "referral__user__username", "ip_address"]
