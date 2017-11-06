from django import template
from django.contrib.contenttypes.models import ContentType

from ..conf import settings

register = template.Library()


@register.inclusion_tag("pinax/referrals/_create_referral_form.html", takes_context=True)
def create_referral(context, url, obj=None):
    if obj:
        context.update(
            {"url": url, "obj": obj, "obj_ct": ContentType.objects.get_for_model(obj)}
        )
    else:
        context.update(
            {"url": url, "obj": "", "obj_ct": ""}
        )
    return context


class ReferralResponsesNode(template.Node):

    def __init__(self, user_var, target_var):
        self.user_var = user_var
        self.target_var = target_var

    def render(self, context):
        user = self.user_var.resolve(context)
        qs = settings.PINAX_REFERRALS_RESPONSES_FILTER_CALLBACK(
            user=user
        )
        context[self.target_var] = qs
        return ""


@register.tag
def referral_responses(parser, token):
    bits = token.split_contents()
    tag_name = bits[0]
    bits = bits[1:]
    if len(bits) < 2 or bits[-2] != "as":
        raise template.TemplateSyntaxError(
            "'%s' tag takes at least 2 arguments and the second to last "
            "argument must be 'as'" % tag_name
        )
    return ReferralResponsesNode(parser.compile_filter(bits[0]), bits[2])


@register.filter
def action_display(value):
    return settings.PINAX_REFERRALS_ACTION_DISPLAY.get(value, value)
