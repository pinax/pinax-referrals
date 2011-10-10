import datetime

from django.db import models
from django.conf import settings
from django.utils.hashcompat import sha_constructor

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


IP_ADDRESS_FIELD = getattr(settings, "ANAFERO_IP_ADDRESS_META_FIELD", "HTTP_X_FORWARDED_FOR")


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
    
    @classmethod
    def create(cls, user, redirect_to, target=None):
        bits = [
            settings.SECRET_KEY,
            str(user.pk),
            redirect_to,
        ]
        if target:
            bits.append(str(target.pk))
            bits.append(str(target.__class__))
        
        code = sha_constructor("".join(bits)).hexdigest()
        
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

