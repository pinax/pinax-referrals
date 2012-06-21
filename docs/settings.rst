.. _settings:

Settings
========

.. _anafero_ip_address_meta_field:

ANAFERO_IP_ADDRESS_META_FIELD
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Default: "HTTP_X_FORWARDED_FOR"

This is the header value that is retrieved from `request.META` to record
the ip address of the the respondent.


ANAFERO_SECURE_URLS
^^^^^^^^^^^^^^^^^^^

:Default: ``False``

Setting this to ``True`` will enable produce urls with ``https`` instead
of ``http``.


ANAFERO_HASH_LENGTH
^^^^^^^^^^^^^^^^^^^

:Default: ``5``

This controls the length of the referral codes that are generated.
