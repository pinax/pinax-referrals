from django.conf.urls.defaults import url, patterns

from anafero.views import create_referral, process_referral


urlpatterns = patterns("",
    url(r"^$", create_referral, name="anafero_create_referral"),
    url(r"^(?P<code>\w+)/$", process_referral, name="anafero_process_referral")
)
