from django.contrib import admin

from anafero.models import Referral, ReferralResponse


admin.site.register(Referral,
    list_display = ["user", "code", "label", "redirect_to", "target_content_type", "target_object_id", "expired_at"],
    readonly_fields = ["code", "created_at"],
    list_filter = ["target_content_type", "created_at", "expired_at"],
    search_fields = ["user", "code"]
)

admin.site.register(ReferralResponse,
    list_display = ["referral", "session_key", "user", "ip_address", "action"],
    readonly_fields = ["referral", "session_key", "user", "ip_address", "action"],
    list_filter = ["action", "created_at"],
    search_fields = ["referral__code", "referral__user__username", "ip_address"]
)
