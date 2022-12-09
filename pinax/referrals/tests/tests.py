import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from pinax.referrals.models import Referral


class Tests(TestCase):

    def test_create_referral(self):
        referring_user = get_user_model().objects.create_user("johndoe", "john@doe.com", "notsosecret")
        self.assertTrue(self.client.login(username=referring_user.username, password="notsosecret"))

        response = self.client.post("/", data={"redirect_to": "https://example.com/"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        json_response = json.loads(response.content.decode("utf-8"))
        self.assertSetEqual(set(json_response.keys()), {"url", "code", "html"})

        self.assertEqual(referring_user.referral_codes.count(), 1)
        referral = referring_user.referral_codes.first()
        self.assertEqual(referral.redirect_to, "https://example.com/")
        self.assertEqual(json_response["code"], referral.code)

    def test_process_referral_authenticated(self):
        referral = Referral.create(redirect_to="https://example.com/")
        self.assertFalse(referral.responses.exists())
        referred_user = get_user_model().objects.create_user("janedoe", "jane@doe.com", "notsosecret")
        self.assertTrue(self.client.login(username=referred_user.username, password="notsosecret"))
        response = self.client.get(referral.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://example.com/")
        self.assertEqual(referral.responses.count(), 1)
        referral_response = referral.responses.first()
        self.assertEqual(referral_response.user, referred_user)

    def test_process_referral_authenticated_anonomous(self):
        referral = Referral.create(redirect_to="https://example.com/")
        self.assertFalse(referral.responses.exists())
        response = self.client.get(referral.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://example.com/")
        self.assertEqual(referral.responses.count(), 1)
        referral_response = referral.responses.first()
        self.assertIsNone(referral_response.user)
        self.assertEqual(response.cookies["pinax-referral"].value, f"{referral.code}:{referral_response.session_key}")

    def test_process_referral_authenticated_next(self):
        """The process_referral view should redirect user to the url from redirect_to queryset parameter."""
        referral = Referral.create(redirect_to="https://example.com/")
        self.assertFalse(referral.responses.exists())
        referred_user = get_user_model().objects.create_user("janedoe", "jane@doe.com", "notsosecret")
        self.assertTrue(self.client.login(username=referred_user.username, password="notsosecret"))
        response = self.client.get(referral.url + "?redirect_to=/foo/bar/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/foo/bar/")
        self.assertEqual(referral.responses.count(), 1)
        referral_response = referral.responses.first()
        self.assertEqual(referral_response.user, referred_user)

    def test_process_referral_authenticated_next_unsafe(self):
        """
        The process_referral view should redirect user to the url from redirect_to queryset parameter.
        If the url is not safe, it should redirect to the redirect_to url from the referral.
        """
        referral = Referral.create(redirect_to="https://example.com/")
        self.assertFalse(referral.responses.exists())
        referred_user = get_user_model().objects.create_user("janedoe", "jane@doe.com", "notsosecret")
        self.assertTrue(self.client.login(username=referred_user.username, password="notsosecret"))
        response = self.client.get(referral.url + "?redirect_to=https://www.google.com/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://example.com/")
        self.assertEqual(referral.responses.count(), 1)
        referral_response = referral.responses.first()
        self.assertEqual(referral_response.user, referred_user)
