import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase
from django.utils import timezone

from pinax.referrals.models import Referral, ReferralResponse


class Tests(TestCase):

    def test_create_referral(self):
        referring_user = get_user_model().objects.create_user("johndoe", "john@doe.com", "notsosecret")
        self.assertTrue(self.client.login(username=referring_user.username, password="notsosecret"))

        response = self.client.post("/", data={"redirect_to": "/landing/"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        json_response = json.loads(response.content.decode("utf-8"))
        self.assertSetEqual(set(json_response.keys()), {"url", "code", "html"})

        self.assertEqual(referring_user.referral_codes.count(), 1)
        referral = referring_user.referral_codes.first()
        self.assertEqual(referral.redirect_to, "/landing/")
        self.assertEqual(json_response["code"], referral.code)

    def test_create_referral_absolute_url_on_this_host(self):
        referring_user = get_user_model().objects.create_user("johndoe", "john@doe.com", "notsosecret")
        self.assertTrue(self.client.login(username=referring_user.username, password="notsosecret"))

        response = self.client.post("/", data={"redirect_to": "http://testserver/landing/"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(referring_user.referral_codes.get().redirect_to, "http://testserver/landing/")

    def test_create_referral_rejects_offsite_redirect_to(self):
        """A referral link must not become an open redirect to another site."""
        referring_user = get_user_model().objects.create_user("johndoe", "john@doe.com", "notsosecret")
        self.assertTrue(self.client.login(username=referring_user.username, password="notsosecret"))

        for redirect_to in ["https://example.com/", "//example.com/", "javascript:alert(1)", ""]:
            with self.subTest(redirect_to=redirect_to):
                response = self.client.post("/", data={"redirect_to": redirect_to})
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response["Content-Type"], "application/json")
                self.assertIn("error", json.loads(response.content.decode("utf-8")))
        self.assertFalse(Referral.objects.exists())

    def test_process_referral_authenticated(self):
        referral = Referral.create(redirect_to="/landing/")
        self.assertFalse(referral.responses.exists())
        referred_user = get_user_model().objects.create_user("janedoe", "jane@doe.com", "notsosecret")
        self.assertTrue(self.client.login(username=referred_user.username, password="notsosecret"))
        response = self.client.get(referral.url, HTTP_REFERER="https://referrer.com")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/landing/")
        self.assertEqual(referral.responses.count(), 1)
        referral_response = referral.responses.first()
        self.assertEqual(referral_response.user, referred_user)
        self.assertEqual(referral_response.http_referrer, "https://referrer.com")

    def test_process_referral_anonymous(self):
        referral = Referral.create(redirect_to="/landing/")
        self.assertFalse(referral.responses.exists())
        response = self.client.get(referral.url, HTTP_REFERER="https://referrer.com")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/landing/")
        self.assertEqual(referral.responses.count(), 1)
        referral_response = referral.responses.first()
        self.assertIsNone(referral_response.user)
        self.assertEqual(response.cookies["pinax-referral"].value, f"{referral.code}:{referral_response.session_key}")
        self.assertEqual(referral_response.http_referrer, "https://referrer.com")

    def test_process_referral_authenticated_next(self):
        """The process_referral view should redirect user to the url from redirect_to queryset parameter."""
        referral = Referral.create(redirect_to="/landing/")
        self.assertFalse(referral.responses.exists())
        referred_user = get_user_model().objects.create_user("janedoe", "jane@doe.com", "notsosecret")
        self.assertTrue(self.client.login(username=referred_user.username, password="notsosecret"))
        response = self.client.get(referral.url + "?redirect_to=/foo/bar/", HTTP_REFERER="https://referrer.com")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/foo/bar/")
        self.assertEqual(referral.responses.count(), 1)
        referral_response = referral.responses.first()
        self.assertEqual(referral_response.user, referred_user)
        self.assertEqual(referral_response.http_referrer, "https://referrer.com")

    def test_process_referral_authenticated_next_unsafe(self):
        """
        The process_referral view should redirect user to the url from redirect_to queryset parameter.
        If the url is not safe, it should redirect to the redirect_to url from the referral.
        """
        referral = Referral.create(redirect_to="/landing/")
        self.assertFalse(referral.responses.exists())
        referred_user = get_user_model().objects.create_user("janedoe", "jane@doe.com", "notsosecret")
        self.assertTrue(self.client.login(username=referred_user.username, password="notsosecret"))
        response = self.client.get(referral.url + "?redirect_to=https://www.google.com/", HTTP_REFERER="https://referrer.com")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/landing/")
        self.assertEqual(referral.responses.count(), 1)
        referral_response = referral.responses.first()
        self.assertEqual(referral_response.user, referred_user)
        self.assertEqual(referral_response.http_referrer, "https://referrer.com")

    def test_process_referral_slash_both_variants(self):
        referral = Referral.create(redirect_to="/landing/")
        self.assertFalse(referral.responses.exists())
        response = self.client.get(referral.url.rstrip("/"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/landing/")
        self.assertEqual(referral.responses.count(), 1)
        referral_response = referral.responses.first()
        self.assertIsNone(referral_response.user)
        self.assertEqual(response.cookies["pinax-referral"].value, f"{referral.code}:{referral_response.session_key}")

        ReferralResponse.objects.all().delete()

        response = self.client.get(referral.url.rstrip("/") + "/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/landing/")
        self.assertEqual(referral.responses.count(), 1)
        referral_response = referral.responses.first()
        self.assertIsNone(referral_response.user)
        self.assertEqual(response.cookies["pinax-referral"].value, f"{referral.code}:{referral_response.session_key}")

    def test_process_referral_absolute_url_on_this_host(self):
        referral = Referral.create(redirect_to="http://testserver/landing/")
        response = self.client.get(referral.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "http://testserver/landing/")

    def test_process_referral_offsite_redirect_to_falls_back_to_root(self):
        """
        A stored off-site redirect_to (e.g. created before create_referral validated it)
        is not followed; the response is still recorded.
        """
        referral = Referral.create(redirect_to="https://example.com/")
        response = self.client.get(referral.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")
        self.assertEqual(referral.responses.count(), 1)
        referral_response = referral.responses.first()
        self.assertEqual(response.cookies["pinax-referral"].value, f"{referral.code}:{referral_response.session_key}")

    def test_process_referral_offsite_redirect_to_and_unsafe_next_fall_back_to_root(self):
        referral = Referral.create(redirect_to="//example.com/")
        response = self.client.get(referral.url + "?redirect_to=https://www.google.com/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")


class ExpiredReferralTests(TestCase):

    def expire(self, referral):
        referral.expired_at = timezone.now() - timedelta(seconds=1)
        referral.save()

    def login(self):
        user = get_user_model().objects.create_user("janedoe", "jane@doe.com", "notsosecret")
        self.assertTrue(self.client.login(username=user.username, password="notsosecret"))
        return user

    def test_expired_referral_redirects_without_recording(self):
        referral = Referral.create(redirect_to="/landing/")
        self.expire(referral)
        response = self.client.get(referral.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/landing/")
        self.assertFalse(referral.responses.exists())
        self.assertNotIn("pinax-referral", response.cookies)

    def test_expired_referral_redirects_logged_in_user_without_recording(self):
        referral = Referral.create(redirect_to="/landing/")
        self.expire(referral)
        self.login()
        response = self.client.get(referral.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/landing/")
        self.assertFalse(referral.responses.exists())

    def test_referral_expiring_in_the_future_records_response(self):
        referral = Referral.create(redirect_to="/landing/")
        referral.expired_at = timezone.now() + timedelta(days=1)
        referral.save()
        response = self.client.get(referral.url)
        self.assertEqual(response["Location"], "/landing/")
        self.assertEqual(referral.responses.count(), 1)
        self.assertIn("pinax-referral", response.cookies)

    def test_middleware_links_active_referral_to_user_who_logs_in(self):
        referral = Referral.create(redirect_to="/landing/")
        self.client.get(referral.url)
        user = self.login()
        self.client.get("/")
        self.assertEqual(referral.responses.get().user, user)

    def test_middleware_does_not_link_referral_that_expired_before_login(self):
        referral = Referral.create(redirect_to="/landing/")
        self.client.get(referral.url)
        self.expire(referral)
        self.login()
        response = self.client.get("/")
        self.assertIsNone(referral.responses.get().user)
        self.assertEqual(response.cookies["pinax-referral"].value, "")

    def anonymous_request(self):
        request = RequestFactory().get("/")
        request.session = self.client.session
        request.user = AnonymousUser()
        return request

    def test_record_response_for_active_referral(self):
        referral = Referral.create(redirect_to="/landing/")
        self.client.get(referral.url)
        self.assertEqual(Referral.record_response(self.anonymous_request(), "SIGNED_UP").referral, referral)

    def test_record_response_ignores_referral_that_expired_after_the_click(self):
        referral = Referral.create(redirect_to="/landing/")
        self.client.get(referral.url)
        self.expire(referral)
        self.assertIsNone(Referral.record_response(self.anonymous_request(), "SIGNED_UP"))
        self.assertFalse(referral.responses.filter(action="SIGNED_UP").exists())


class RobustnessTests(TestCase):

    def login(self):
        user = get_user_model().objects.create_user("janedoe", "jane@doe.com", "notsosecret")
        self.assertTrue(self.client.login(username=user.username, password="notsosecret"))
        return user

    def test_unresolvable_redirect_to_parameter_falls_back_to_stored_redirect_to(self):
        referral = Referral.create(redirect_to="/landing/")
        response = self.client.get(referral.url, {"redirect_to": "foo"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/landing/")
        self.assertEqual(referral.responses.count(), 1)

    def test_url_name_in_redirect_to_parameter_still_resolves(self):
        referral = Referral.create(redirect_to="/landing/")
        response = self.client.get(referral.url, {"redirect_to": "pinax_referrals:create_referral"})
        self.assertEqual(response["Location"], "/")

    def test_unresolvable_stored_redirect_to_falls_back_to_root(self):
        referral = Referral.create(redirect_to="foo")
        response = self.client.get(referral.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")

    def test_referral_cookie_links_responses_to_user_who_logs_in(self):
        referral = Referral.create(redirect_to="/landing/")
        self.client.get(referral.url)
        user = self.login()
        response = self.client.get("/")
        self.assertEqual(referral.responses.get().user, user)
        self.assertEqual(response.cookies["pinax-referral"].value, "")

    def test_unusable_referral_cookie_is_dropped_for_logged_in_user(self):
        self.login()
        for cookie in ["no-colon", "unknown-code:some-session"]:
            with self.subTest(cookie=cookie):
                self.client.cookies["pinax-referral"] = cookie
                response = self.client.get("/")
                self.assertEqual(response.status_code, 405)
                self.assertEqual(response.cookies["pinax-referral"].value, "")

    def test_for_request_ignores_malformed_cookie(self):
        request = RequestFactory().get("/")
        request.COOKIES["pinax-referral"] = "no-colon"
        self.assertIsNone(Referral.for_request(request))

    def test_create_referral_with_target(self):
        user = self.login()
        response = self.client.post("/", data={
            "redirect_to": "/landing/",
            "obj_ct_pk": ContentType.objects.get_for_model(user).pk,
            "obj_pk": user.pk,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Referral.objects.get().target, user)

    def test_create_referral_rejects_unknown_target(self):
        user = self.login()
        user_ct_pk = ContentType.objects.get_for_model(user).pk
        missing_ct_pk = ContentType.objects.order_by("-pk").first().pk + 1
        for obj_ct_pk, obj_pk in [
            (missing_ct_pk, user.pk),
            ("abc", user.pk),
            (user_ct_pk, user.pk + 1),
            (user_ct_pk, "abc"),
        ]:
            with self.subTest(obj_ct_pk=obj_ct_pk, obj_pk=obj_pk):
                response = self.client.post("/", data={
                    "redirect_to": "/landing/",
                    "obj_ct_pk": obj_ct_pk,
                    "obj_pk": obj_pk,
                })
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", json.loads(response.content.decode("utf-8")))
        self.assertFalse(Referral.objects.exists())

    def test_referral_cookie_flags(self):
        referral = Referral.create(redirect_to="/landing/")
        cookie = self.client.get(referral.url).cookies["pinax-referral"]
        self.assertIs(cookie["httponly"], True)
        self.assertEqual(cookie["samesite"], "Lax")
        self.assertFalse(cookie["secure"])

    def test_referral_cookie_is_secure_over_https(self):
        referral = Referral.create(redirect_to="/landing/")
        cookie = self.client.get(referral.url, secure=True).cookies["pinax-referral"]
        self.assertIs(cookie["secure"], True)
