from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils import simplejson as json
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from anafero.models import Referral


SECURE_URLS = getattr(settings, "ANAFERO_SECURE_URLS", False)


@login_required
@require_POST
def create_referral(request):
    target = None
    referral = Referral.create(
        user=request.user,
        redirect_to=request.POST.get("redirect_to"),
        target=target
    )
    path = reverse("anafero_process_referral", kwargs={"code": referral.code})
    domain = Site.objects.get_current().domain
    protocol = "https" if SECURE_URLS else "http"
    url = "%s://%s%s" % (protocol, domain, path)
    return HttpResponse(json.dumps({"url": url}))


def process_referral(request, code):
    referral = get_object_or_404(Referral, code=code)
    referral.respond(request, "RESPONDED")
    
    response = redirect(referral.redirect_to)
    if request.user.is_anonymous():
        response.set_cookie(
            "anafero-referral",
            "%s:%s" % (code, request.session.session_key)
        )
    else:
        response.delete_cookie("anafero-referral")
    
    return response
