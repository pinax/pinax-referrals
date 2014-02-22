from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site

from anafero.conf import settings
from anafero.signals import user_linked_to_response


AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class Referral(models.Model):

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="referral_codes",
        null=True
    )
    label = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=40, unique=True)
    expired_at = models.DateTimeField(null=True)
    redirect_to = models.CharField(max_length=512)
    target_content_type = models.ForeignKey(ContentType, null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = generic.GenericForeignKey(
        ct_field="target_content_type",
        fk_field="target_object_id"
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        if self.user:
            return u"{0} ({1})".format(self.user, self.code)
        else:
            return self.code

    def is_active(self):
        return self.expired_at is None or self.expired_at > timezone.now()

    @classmethod
    def for_request(cls, request):
        cookie = request.COOKIES.get("anafero-referral")
        if cookie:
            code, session_key = cookie.split(":")
            try:
                return Referral.objects.get(code=code)
            except Referral.DoesNotExist:
                pass

    @property
    def url(self):
        path = reverse("anafero_process_referral", kwargs={"code": self.code})
        domain = Site.objects.get_current().domain
        protocol = "https" if settings.ANAFERO_SECURE_URLS else "http"
        return "{0}://{1}{2}".format(protocol, domain, path)

    @property
    def response_count(self):
        return self.responses.filter(action="RESPONDED").count()

    @classmethod
    def create(cls, redirect_to, user=None, label="", target=None):
        code = settings.ANAFERO_CODE_GENERATOR_CALLBACK(cls)

        if target:
            obj, _ = cls.objects.get_or_create(
                user=user,
                code=code,
                redirect_to=redirect_to,
                label=label,
                target_content_type=ContentType.objects.get_for_model(target),
                target_object_id=target.pk
            )
        else:
            obj, _ = cls.objects.get_or_create(
                user=user,
                code=code,
                label=label,
                redirect_to=redirect_to,
            )

        return obj

    @classmethod
    def record_response(cls, request, action_string, target=None):
        referral = cls.referral_for_request(request)
        if referral:
            return referral.respond(request, action_string, target=target)

    @classmethod
    def referral_for_request(cls, request):
        if request.user.is_authenticated():
            qs = ReferralResponse.objects.filter(user=request.user)
        else:
            qs = ReferralResponse.objects.filter(session_key=request.session.session_key)

        try:
            return qs.order_by("-created_at")[0].referral
        except IndexError:
            pass

    def link_responses_to_user(self, user, session_key):
        for response in self.responses.filter(session_key=session_key, user__isnull=True):
            response.user = user
            response.save()
            user_linked_to_response.send(sender=self, response=response)

    def respond(self, request, action_string, user=None, target=None):
        if user is None:
            if request.user.is_authenticated():
                user = request.user
            else:
                user = None

        ip_address = request.META.get(
            settings.ANAFERO_IP_ADDRESS_META_FIELD,
            ""
        )

        kwargs = dict(
            referral=self,
            session_key=request.session.session_key,
            ip_address=ip_address,
            action=action_string,
            user=user
        )
        if target:
            kwargs.update({"target": target})

        return ReferralResponse.objects.create(**kwargs)

    def filtered_responses(self):
        return settings.ANAFERO_RESPONSES_FILTER_CALLBACK(
            referral=self
        )


class ReferralResponse(models.Model):

    referral = models.ForeignKey(Referral, related_name="responses")
    session_key = models.CharField(max_length=40)
    user = models.ForeignKey(AUTH_USER_MODEL, null=True)
    ip_address = models.CharField(max_length=45)
    action = models.CharField(max_length=128)

    target_content_type = models.ForeignKey(ContentType, null=True)
    target_object_id = models.PositiveIntegerField(null=True)
    target = generic.GenericForeignKey(
        ct_field="target_content_type",
        fk_field="target_object_id"
    )

    created_at = models.DateTimeField(default=timezone.now)
