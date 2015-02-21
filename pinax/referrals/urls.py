from django.conf.urls import url, patterns

from .views import create_referral, process_referral


urlpatterns = patterns(
    "",
    url(r"^$", create_referral, name="pinax_referrals_create_referral"),
    url(r"^(?P<code>\w+)/$", process_referral, name="pinax_referrals_process_referral")
)
