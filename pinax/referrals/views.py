from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from .models import Referral
from .utils import ensure_session_key

try:
    from account.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required

try:
    from django.utils.http import url_has_allowed_host_and_scheme
except ImportError:  # Django < 3.0
    from django.utils.http import is_safe_url as url_has_allowed_host_and_scheme


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

    return JsonResponse({
        "url": referral.url,
        "code": referral.code,
        "html": render_to_string(
            "pinax/referrals/_create_referral_form.html",
            context=ctx,
            request=request
        )
    })


def process_referral(request, code):
    referral = get_object_or_404(Referral, code=code)
    session_key = ensure_session_key(request)
    referral.respond(request, "RESPONDED")
    max_age = getattr(settings, "PINAX_COOKIE_MAX_AGE", None)
    try:
        next_url = request.GET[
            getattr(settings, "PINAX_REFERRALS_REDIRECT_ATTRIBUTE", "redirect_to")
        ]
        url_is_safe = url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts=request.get_host(),
            require_https=request.is_secure(),
        )
        if url_is_safe:
            response = redirect(next_url)
        else:
            response = redirect(referral.redirect_to)
    except KeyError:
        response = redirect(referral.redirect_to)
    if request.user.is_anonymous:
        response.set_cookie(
            "pinax-referral",
            f"{code}:{session_key}",
            max_age=max_age
        )
    else:
        response.delete_cookie("pinax-referral")

    return response
