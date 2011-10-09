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

* Lastly you will want to add `kaleo.urls` to your urls definition::

    ...
    url(r"^referrals/", include("anafero.urls")),
    ...
