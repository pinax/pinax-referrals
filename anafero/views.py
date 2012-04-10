from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils import simplejson as json
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required

from anafero.models import Referral


@login_required
@require_POST
def create_referral(request):
    target = None
    referral = Referral.create(
        user=request.user,
        redirect_to=request.POST.get("redirect_to"),
        target=target
    )
    return HttpResponse(
        json.dumps({
            "url": referral.url,
            "code": referral.code
        }),
        mimetype="application/json"
    )


def process_referral(request, code):
    referral = get_object_or_404(Referral, code=code)
    referral.respond(request, "RESPONDED")
    request.session["anafero-tracking"] = True
    response = redirect(referral.redirect_to)
    if request.user.is_anonymous():
        response.set_cookie(
            "anafero-referral",
            "%s:%s" % (code, request.session.session_key)
        )
    else:
        response.delete_cookie("anafero-referral")
    
    return response
