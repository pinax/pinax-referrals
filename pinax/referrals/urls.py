from django.conf.urls import url

from .views import create_referral, process_referral

app_name = "pinax_referrals"

urlpatterns = [
    url(r"^$", create_referral, name="create_referral"),
    url(r"^(?P<code>\w+)/$", process_referral, name="process_referral")
]
