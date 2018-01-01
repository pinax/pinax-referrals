from django.conf.urls import include, url

urlpatterns = [
    url(r"^", include("pinax.referrals.urls", namespace="pinax_referrals")),
]
