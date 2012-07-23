from django import template

from django.contrib.contenttypes.models import ContentType

from anafero.models import ReferralResponse, ACTION_DISPLAY


register = template.Library()


@register.inclusion_tag("anafero/_create_referral_form.html")
def create_referral(url, obj=None):
    if obj:
        return {"url": url, "obj": obj, "obj_ct": ContentType.objects.get_for_model(obj)}
    else:
        return {"url": url, "obj": "", "obj_ct": ""}


@register.assignment_tag
def referral_responses(user):
    return ReferralResponse.objects.filter(
        referral__user=user
    ).order_by("-created_at")


@register.filter
def action_display(value):
    return ACTION_DISPLAY.get(value, value)
