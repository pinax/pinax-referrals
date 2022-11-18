from django.core.exceptions import ImproperlyConfigured

from .models import Referral

try:
    from django.utils.deprecation import MiddlewareMixin as MiddlewareBaseClass
except ImportError:
    MiddlewareBaseClass = object


class SessionJumpingMiddleware(MiddlewareBaseClass):

    def process_request(self, request):
        if not hasattr(request, "user"):
            raise ImproperlyConfigured(
                "django.contrib.auth.middleware.AuthenticationMiddleware middleware must come "
                "before pinax.referrals.middleware.SessionJumpingMiddleware"
            )
        cookie = request.COOKIES.get("pinax-referral")
        if request.user.is_authenticated and cookie:
            code, session_key = cookie.split(":")

            try:
                referral = Referral.objects.get(code=code)
                referral.link_responses_to_user(request.user, session_key)
            except Referral.DoesNotExist:
                pass

            request.user._can_delete_pinax_referral_cookie = True

    def process_response(self, request, response):
        if hasattr(request, "user") and getattr(request.user, "_can_delete_pinax_referral_cookie", False):
            response.delete_cookie("pinax-referral")
        return response
