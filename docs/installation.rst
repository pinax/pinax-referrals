.. _installation:

Installation
============

* To install anafero::

    pip install anafero

* Add ``anafero`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # other apps
        "anafero",
    )

* See the list of :ref:`settings` to modify anafero's
  default behavior and make adjustments for your website.

* Add ``anafero.middleware.SessionJumpingMiddleware`` in order to link up a user who
  registers and authenticate after hitting the initial referral link. Make sure
  that it comes after the ``django.contrib.auth.middleware.AuthenticationMiddleware``::

    MIDDLEWARE_CLASSES = [
        ...
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        ...
        "anafero.middleware.SessionJumpingMiddleware",
        ...
    ]

* Lastly you will want to add `kaleo.urls` to your urls definition::

    ...
    url(r"^referrals/", include("anafero.urls")),
    ...
