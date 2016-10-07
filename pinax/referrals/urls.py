from django.conf.urls import url

from .views import create_referral, process_referral


urlpatterns = [
    url(r"^$", create_referral, name="pinax_referrals_create_referral"),
    url(r"^(?P<code>\w+)/$", process_referral, name="pinax_referrals_process_referral")
]
