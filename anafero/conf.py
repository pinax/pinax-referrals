from django.conf import settings  # noqa

from appconf import AppConf

from anafero.utils import load_path_attr


class AnaferoAppConf(AppConf):

    IP_ADDRESS_META_FIELD = "HTTP_X_FORWARDED_FOR"
    SECURE_URLS = False
    ACTION_DISPLAY = {"RESPONDED": "Clicked on referral link"}
    CODE_GENERATOR_CALLBACK = "anafero.callbacks.generate_code"
    RESPONSES_FILTER_CALLBACK = "anafero.callbacks.filter_responses"

    def configure_code_generator_callback(self, value):
        return load_path_attr(value)

    def configure_responses_filter_callback(self, value):
        return load_path_attr(value)
