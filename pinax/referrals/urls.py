from django.urls import path

from .views import create_referral, process_referral

app_name = "pinax_referrals"

urlpatterns = [
    path("", create_referral, name="create_referral"),
    path("<str:code>", process_referral, name="process_referral")
]
