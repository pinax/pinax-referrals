from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin

from .models import Referral


class SessionJumpingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if not hasattr(request, "user"):
            raise ImproperlyConfigured(
                "django.contrib.auth.middleware.AuthenticationMiddleware middleware must come "
                "before pinax.referrals.middleware.SessionJumpingMiddleware"
            )
        cookie = request.COOKIES.get("pinax-referral")
        if request.user.is_authenticated and cookie:
            code, _, session_key = cookie.partition(":")

            if session_key:
                try:
                    referral = Referral.objects.get(code=code)
                    if referral.is_active():
                        referral.link_responses_to_user(request.user, session_key)
                except Referral.DoesNotExist:
                    pass

            request.user._can_delete_pinax_referral_cookie = True

    def process_response(self, request, response):
        if hasattr(request, "user") and getattr(request.user, "_can_delete_pinax_referral_cookie", False):
            response.delete_cookie("pinax-referral")
        return response
