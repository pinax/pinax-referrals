import random

from .conf import settings


def generate_code(referral_class):
    def _generate_code():
        t = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890"
        return "".join([random.choice(t) for i in range(40)])
    code = _generate_code()
    while referral_class.objects.filter(code=code).exists():
        code = _generate_code()
    return code


def filter_responses(user=None, referral=None):
    from .models import ReferralResponse
    responses = ReferralResponse.objects.all()
    if user:
        responses = responses.filter(referral__user=user)
    if referral:
        responses = responses.filter(referral=referral)
    return responses.order_by("-created_at")


def get_client_ip(request):
    return request.META.get(settings.PINAX_REFERRALS_IP_ADDRESS_META_FIELD, "")
