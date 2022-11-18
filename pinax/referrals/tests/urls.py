from django.urls import include, path

urlpatterns = [
    path("", include("pinax.referrals.urls", namespace="pinax_referrals")),
]
