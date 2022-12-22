from django.test import RequestFactory, TestCase
from django.test.utils import override_settings

from pinax.referrals.models import Referral

from model_bakery import baker


def generate_code_callback(referral_class, referral):
    return f"recommended-by-{referral.user.username}"


def legacy_generate_code_callback(referral_class):
    return "some-generated-code"


class ReferralTests(TestCase):
    def test_referral_responses_for_request_no_user(self):
        # Create a referral with a blank user
        request = RequestFactory().get("/referral/")
        request.session = self.client.session
        baker.make("ReferralResponse", session_key=request.session.session_key)
        baker.make("ReferralResponse", user=baker.make("User"))
        queryset = Referral.referral_responses_for_request(request)
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.get().session_key, request.session.session_key)
        self.assertEqual(queryset.get().user, None)

    def test_referral_responses_for_request_user(self):
        # Create a referral with a user
        request = RequestFactory().get("/referral/")
        request.session = self.client.session
        request.user = baker.make("User")
        baker.make("ReferralResponse", user=request.user, session_key="foo_bar")
        baker.make("ReferralResponse", session_key="session_key")
        queryset = Referral.referral_responses_for_request(request)
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.get().user, request.user)
        self.assertEqual(queryset.get().session_key, "foo_bar")

    @override_settings(PINAX_REFERRALS_CODE_GENERATOR_CALLBACK=generate_code_callback)
    def test_code_generator_callback(self):
        user = baker.make("User", username="joe")
        referral = baker.make("Referral", user=user, code=None)
        # the callback function is being called in the save() method, inside baker.make
        self.assertEqual(referral.code, "recommended-by-joe")

    @override_settings(PINAX_REFERRALS_CODE_GENERATOR_CALLBACK=legacy_generate_code_callback)
    def test_legacy_code_generator_callback(self):
        # the new callback signature accepts two parameters, but the old callback signature
        # with just the referral_class as parameter should still work
        referral = baker.make("Referral", code=None)
        # the callback function is being called in the save() method, inside baker.make
        self.assertEqual(referral.code, "some-generated-code")
