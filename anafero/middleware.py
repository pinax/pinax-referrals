from django.core.exceptions import ImproperlyConfigured

from anafero.models import Referral


class SessionJumpingMiddleware(object):
    
    def process_request(self, request):
        if not hasattr(request, "user"):
            raise ImproperlyConfigured("django.contrib.auth.middleware.AuthenticationMiddleware middleware must come before anafero.middleware.SessionJumpingMiddleware")
        cookie = request.COOKIES.get("anafero-referral")
        if request.user.is_authenticated() and cookie:
            code, session_key = cookie.split(":")
            
            try:
                referral = Referral.objects.get(code=code)
                for response in referral.responses.filter(session_key=session_key, user__isnull=True):
                    response.user = request.user
                    response.save()
            except Referral.DoesNotExist:
                pass
            
            request.user._can_delete_anafero_cookie = True
    
    def process_response(self, request, response):
        if hasattr(request, "user") and getattr(request.user, "_can_delete_anafero_cookie", False):
            response.delete_cookie("anafero-referral")
        return response
