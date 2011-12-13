import datetime
import random

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site


IP_ADDRESS_FIELD = getattr(settings, "ANAFERO_IP_ADDRESS_META_FIELD", "HTTP_X_FORWARDED_FOR")
SECURE_URLS = getattr(settings, "ANAFERO_SECURE_URLS", False)
HASH_LENGTH = getattr(settings, "ANAFERO_HASH_LENGTH", 5)
if HASH_LENGTH > 40:
    HASH_LENGTH = 40


def generate_secret_id(length=HASH_LENGTH):
    t = "abcdefghijkmnopqrstuvwwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890"
    return "".join([random.choice(t) for i in range(length)])


class Referral(models.Model):
    
    user = models.ForeignKey(User, related_name="referral_codes")
    code = models.CharField(max_length=40, unique=True)
    redirect_to = models.CharField(max_length=512)
    target_content_type = models.ForeignKey(ContentType, null=True)
    target_object_id = models.PositiveIntegerField(null=True)
    target = generic.GenericForeignKey(
        ct_field="target_content_type",
        fk_field="target_object_id"
    )
    
    created_at = models.DateTimeField(default=datetime.datetime.now)
    
    @property
    def url(self):
        path = reverse("anafero_process_referral", kwargs={"code": self.code})
        domain = Site.objects.get_current().domain
        protocol = "https" if SECURE_URLS else "http"
        return "%s://%s%s" % (protocol, domain, path)
    
    @property
    def response_count(self):
        return self.responses.filter(action="RESPONDED").count()
    
    @classmethod
    def create(cls, user, redirect_to, target=None):
        code = generate_secret_id()
        while Referral.objects.filter(code=code).count() > 0:
            code = generate_secret_id()
        
        if target:
            obj, _ = cls.objects.get_or_create(
                user=user,
                code=code,
                redirect_to=redirect_to,
                target_content_type=ContentType.objects.get_for_model(target),
                target_object_id=target.pk
            )
        else: 
            obj, _ = cls.objects.get_or_create(
                user=user,
                code=code,
                redirect_to=redirect_to,
            )
        
        return obj
    
    @classmethod
    def record_response(cls, request, action_string):
        if request.user.is_authenticated():
            qs = ReferralResponse.objects.filter(user=request.user)
        else:
            qs = ReferralResponse.objects.filter(session_key=request.session.session_key)
        
        try:
            response = qs.order_by("-created_at")[0]
            return response.referral.respond(request, action_string)
        except IndexError:
            pass
    
    def respond(self, request, action_string):
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None
        
        ip_address = request.META.get(IP_ADDRESS_FIELD, "")
        
        return ReferralResponse.objects.create(
            referral=self,
            session_key=request.session.session_key,
            ip_address=ip_address,
            action=action_string,
            user=user
        )


class ReferralResponse(models.Model):
    
    referral = models.ForeignKey(Referral, related_name="responses")
    session_key = models.CharField(max_length=40)
    user = models.ForeignKey(User, null=True)
    ip_address = models.CharField(max_length=45)
    action = models.CharField(max_length=128)
    
    created_at = models.DateTimeField(default=datetime.datetime.now)

