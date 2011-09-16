from django import template

from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.inclusion_tag("anafero/_create_referral_form.html")
def create_referral(url, obj=None):
    if obj:
        return {"url": url, "obj": obj, "obj_ct": ContentType.objects.get_for_model(obj)}
    else:
        return {"url": url, "obj": "", "obj_ct": ""}
