from datetime import timedelta

from django.db import connection
from django.test import RequestFactory, TestCase
from django.test.utils import CaptureQueriesContext, override_settings
from django.utils import timezone

from model_bakery import baker
from pinax.referrals.models import Referral


def generate_code_callback(referral_class, referral):
    return f"recommended-by-{referral.user.username}"


def legacy_generate_code_callback(referral_class):
    return "some-generated-code"


class ReferralTests(TestCase):
    def test_referral_responses_for_request_no_user(self):
        # Create a referral with a blank user
        request = RequestFactory().get("/referral/")
        request.session = self.client.session
        baker.make("ReferralResponse", session_key=request.session.session_key, target=None, referral__target=None)
        baker.make("ReferralResponse", user=baker.make("User"), target=None, referral__target=None)
        queryset = Referral.referral_responses_for_request(request)
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.get().session_key, request.session.session_key)
        self.assertEqual(queryset.get().user, None)

    def test_referral_responses_for_request_user(self):
        # Create a referral with a user
        request = RequestFactory().get("/referral/")
        request.session = self.client.session
        request.user = baker.make("User")
        baker.make("ReferralResponse", user=request.user, session_key="foo_bar", target=None, referral__target=None)
        baker.make("ReferralResponse", session_key="session_key", target=None, referral__target=None)
        queryset = Referral.referral_responses_for_request(request)
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.get().user, request.user)
        self.assertEqual(queryset.get().session_key, "foo_bar")

    @override_settings(PINAX_REFERRALS_CODE_GENERATOR_CALLBACK=generate_code_callback)
    def test_code_generator_callback(self):
        user = baker.make("User", username="joe")
        referral = baker.make("Referral", user=user, code=None, target=None)
        # the callback function is being called in the save() method, inside baker.make
        self.assertEqual(referral.code, "recommended-by-joe")

    @override_settings(PINAX_REFERRALS_CODE_GENERATOR_CALLBACK=legacy_generate_code_callback)
    def test_legacy_code_generator_callback(self):
        # the new callback signature accepts two parameters, but the old callback signature
        # with just the referral_class as parameter should still work
        referral = baker.make("Referral", code=None, target=None)
        # the callback function is being called in the save() method, inside baker.make
        self.assertEqual(referral.code, "some-generated-code")

    def test_is_active_without_expiry(self):
        self.assertTrue(baker.make("Referral", expired_at=None, target=None).is_active())

    def test_is_active_before_expiry(self):
        referral = baker.make("Referral", expired_at=timezone.now() + timedelta(days=1), target=None)
        self.assertTrue(referral.is_active())

    def test_is_not_active_after_expiry(self):
        referral = baker.make("Referral", expired_at=timezone.now() - timedelta(seconds=1), target=None)
        self.assertFalse(referral.is_active())

    def test_referral_for_request_fetches_only_the_latest_response(self):
        request = RequestFactory().get("/referral/")
        request.session = self.client.session
        older, newer = baker.make("Referral", target=None, _quantity=2)
        session_key = request.session.session_key
        now = timezone.now()
        baker.make("ReferralResponse", referral=older, session_key=session_key, created_at=now - timedelta(days=1), target=None)
        baker.make("ReferralResponse", referral=newer, session_key=session_key, created_at=now, target=None)
        with CaptureQueriesContext(connection) as queries:
            self.assertEqual(Referral.referral_for_request(request), newer)
        self.assertIn("LIMIT 1", queries.captured_queries[0]["sql"])

    def test_referral_for_request_without_responses(self):
        request = RequestFactory().get("/referral/")
        request.session = self.client.session
        self.assertIsNone(Referral.referral_for_request(request))
