from django.urls import path, re_path

from .views import create_referral, process_referral

app_name = "pinax_referrals"

urlpatterns = [
    path("", create_referral, name="create_referral"),
    re_path(r"^(?P<code>[\w-]+)/?$", process_referral, name="process_referral"),
]
