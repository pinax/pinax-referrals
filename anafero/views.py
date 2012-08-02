from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils import simplejson as json
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from anafero.models import Referral
from anafero.utils import ensure_session_key


@login_required
@require_POST
def create_referral(request):
    target = None
    ctx = {"url": request.POST.get("redirect_to")}
    
    if request.POST.get("obj_ct_pk") and request.POST.get("obj_pk"):
        ct = ContentType.objects.get(pk=request.POST.get("obj_ct_pk"))
        target = ct.get_object_for_this_type(pk=request.POST.get("obj_pk"))
        ctx["obj"] = target
        ctx["obj_ct"] = ct
    
    referral = Referral.create(
        user=request.user,
        redirect_to=request.POST.get("redirect_to"),
        label=request.POST.get("label", ""),
        target=target
    )
    
    return HttpResponse(
        json.dumps({
            "url": referral.url,
            "code": referral.code,
            "html": render_to_string(
                "anafero/_create_referral_form.html",
                ctx,
                context_instance=RequestContext(request)
            )
        }),
        mimetype="application/json"
    )


def process_referral(request, code):
    referral = get_object_or_404(Referral, code=code)
    session_key = ensure_session_key(request)
    referral.respond(request, "RESPONDED")
    response = redirect(referral.redirect_to)
    if request.user.is_anonymous():
        response.set_cookie(
            "anafero-referral",
            "%s:%s" % (code, session_key)
        )
    else:
        response.delete_cookie("anafero-referral")
    
    return response
