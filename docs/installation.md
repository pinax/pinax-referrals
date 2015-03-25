# Installation

To install pinax-referrals:

    pip install pinax-referrals


Add `pinax.referrals` to your `INSTALLED_APPS` setting:

    INSTALLED_APPS = (
        # other apps
        "pinax.referrals",
    )


See the list of [settings](settings.md) to modify `pinax-referrals`'s default
behavior and make adjustments for your website.

Add `pinax.referrals.middleware.SessionJumpingMiddleware` in order to link up a
user who registers and authenticate after hitting the initial referral link.
Make sure that it comes after the `django.contrib.auth.middleware.AuthenticationMiddleware`:

    MIDDLEWARE_CLASSES = [
        ...
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        ...
        "pinax.referrals.middleware.SessionJumpingMiddleware",
        ...
    ]

Lastly you will want to add `pinax.referrals.urls` to your urls definition:

    ...
    url(r"^referrals/", include("pinax.referrals.urls")),
    ...
