from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Referral, ReferralResponse


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "code",
        "label",
        "redirect_to",
        "target_content_type",
        "target_object_id",
        "url",
    ]
    readonly_fields = ["code", "created_at"]
    list_filter = ["target_content_type"]
    search_fields = ["user__username", "user__email", "code"]
    autocomplete_fields = ["user"]


@admin.register(ReferralResponse)
class ReferralResponseAdmin(admin.ModelAdmin):
    list_display = [
        "referral",
        "session_key",
        "user",
        "ip_address",
        "action",
        "target_object_link",
    ]
    readonly_fields = ["referral", "session_key", "user", "ip_address", "action", "target_object_link"]
    list_filter = ["action"]
    search_fields = [
        "referral__code",
        "referral__user__email",
        "referral__user__username",
        "user__email",
        "user__username",
        "ip_address",
    ]

    def target_object_link(self, obj):
        if obj.pk and obj.target:
            admin_link = reverse("admin:%s_%s_change" % (obj.target_content_type.app_label, obj.target_content_type.model), args=(obj.target.pk,))
            return format_html('<a href="{}">{}</a>', admin_link, obj.target.__str__())
