from urllib.parse import urlsplit

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse
from django.http.request import split_domain_port
from django.shortcuts import get_object_or_404, resolve_url
from django.template.loader import render_to_string
from django.urls import NoReverseMatch
from django.utils.http import is_same_domain, url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .conf import settings
from .models import Referral
from .utils import ensure_session_key

try:
    from account.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required


def _allowed_redirect_hosts(request, url):
    """
    The host serving the request, plus url's host if it matches
    PINAX_REFERRALS_ALLOWED_REDIRECT_HOSTS.
    """
    allowed_hosts = {request.get_host()}
    try:
        netloc = urlsplit(url).netloc
    except ValueError:  # url_has_allowed_host_and_scheme() refuses an unparsable URL too
        return allowed_hosts
    domain, _port = split_domain_port(netloc)
    if domain and any(is_same_domain(domain, host) for host in settings.PINAX_REFERRALS_ALLOWED_REDIRECT_HOSTS):
        allowed_hosts.add(netloc)
    return allowed_hosts


def _is_safe_redirect_url(request, url):
    if not url:
        return False
    return url_has_allowed_host_and_scheme(
        url=url,
        allowed_hosts=_allowed_redirect_hosts(request, url.strip()),
        require_https=request.is_secure(),
    )


def _redirect_url(request, *candidates):
    """The first candidate that is a safe URL or URL name, resolved; "/" if none is."""
    for url in candidates:
        if _is_safe_redirect_url(request, url):
            try:
                return resolve_url(url)
            except NoReverseMatch:
                pass
    return "/"


@login_required
@require_POST
def create_referral(request):
    redirect_to = request.POST.get("redirect_to")
    if not _is_safe_redirect_url(request, redirect_to):
        return JsonResponse({"error": "redirect_to must be a URL on this site."}, status=400)

    target = None
    ctx = {"url": redirect_to}

    if request.POST.get("obj_ct_pk") and request.POST.get("obj_pk"):
        try:
            ct = ContentType.objects.get(pk=request.POST.get("obj_ct_pk"))
            target = ct.get_object_for_this_type(pk=request.POST.get("obj_pk"))
        except (ObjectDoesNotExist, ValueError):
            return JsonResponse({"error": "obj_ct_pk and obj_pk must identify an existing object."}, status=400)
        ctx["obj"] = target
        ctx["obj_ct"] = ct

    referral = Referral.create(
        user=request.user,
        redirect_to=redirect_to,
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
    next_url = _redirect_url(
        request,
        request.GET.get(getattr(settings, "PINAX_REFERRALS_REDIRECT_ATTRIBUTE", "redirect_to")),
        referral.redirect_to,
    )
    response = HttpResponseRedirect(next_url)
    if not referral.is_active():
        return response

    session_key = ensure_session_key(request)
    referral.respond(request, "RESPONDED")
    max_age = getattr(settings, "PINAX_COOKIE_MAX_AGE", None)
    if request.user.is_anonymous:
        response.set_cookie(
            "pinax-referral",
            f"{code}:{session_key}",
            max_age=max_age,
            secure=request.is_secure(),
            httponly=True,
            samesite="Lax",
        )
    else:
        response.delete_cookie("pinax-referral")

    return response
