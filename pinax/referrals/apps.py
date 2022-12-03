from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "pinax.referrals"
    verbose_name = _("Pinax Referrals")
    default_auto_field = "django.db.models.AutoField"
