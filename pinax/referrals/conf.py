from django.conf import settings  # noqa

from appconf import AppConf

from .utils import load_path_attr


class PinaxReferralsAppConf(AppConf):

    IP_ADDRESS_META_FIELD = "HTTP_X_FORWARDED_FOR"
    SECURE_URLS = False
    ACTION_DISPLAY = {"RESPONDED": "Clicked on referral link"}
    CODE_GENERATOR_CALLBACK = "pinax.referrals.callbacks.generate_code"
    RESPONSES_FILTER_CALLBACK = "pinax.referrals.callbacks.filter_responses"
    GET_CLIENT_IP_CALLBACK = "pinax.referrals.callbacks.get_client_ip"

    def configure_get_client_ip_callback(self, value):
        return load_path_attr(value)

    def configure_code_generator_callback(self, value):
        return load_path_attr(value)

    def configure_responses_filter_callback(self, value):
        return load_path_attr(value)

    class Meta:
        prefix = "pinax_referrals"
