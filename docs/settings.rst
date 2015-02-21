.. _settings:

Settings
========

.. _pinax_referrals_ip_address_meta_field:

PINAX_REFERRALS_IP_ADDRESS_META_FIELD
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Default: "HTTP_X_FORWARDED_FOR"

This is the header value that is retrieved from `request.META` to record
the ip address of the the respondent.


PINAX_REFERRALS_SECURE_URLS
^^^^^^^^^^^^^^^^^^^

:Default: ``False``

Setting this to ``True`` will enable produce urls with ``https`` instead
of ``http``.


PINAX_REFERRALS_CODE_GENERATOR_CALLBACK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Default: "pinax.referrals.utils.generate_code"

Externalizes the logic that generates the referral code. `pinax-referrals` ships
with a default that will generate a random 40-character alpha-numeric
string that can also be used as a reference implementation. The callable
defined by the fully qualified path is passed a single parameter that is
the class of the referral model, or `Referral`, this is done as a pure
convenience so as to alleviate the need for you to have to import it
should you need it (and you most likely will if you want to be
certain of uniqueness).


PINAX_REFERRALS_ACTION_DISPLAY
^^^^^^^^^^^^^^^^^^^^^^

:Default: ``{"RESPONDED": "Clicked on referral link"}``

Defines a dictionary mapping action codes for responses to user-friendly
display text. Used by the ``action_display`` template filter.


PINAX_REFERRALS_REDIRECT_ATTRIBUTE
^^^^^^^^^^^^^^^^^^^^^^^^^^

:Default: ``redirect_to``

Defines the URL attribute to retrieve dynamic referral redirection URLs from.
