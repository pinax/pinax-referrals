from django.test import RequestFactory, TestCase

from pinax.referrals.models import Referral

from model_bakery import baker


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
