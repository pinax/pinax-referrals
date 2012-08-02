.. _changelog:

ChangeLog
=========

0.5.1
-----

- BUG: fixed an issue with sessions in Django 1.4


0.5
---

- FEATURE: added ability to label referrals
- ENHANCEMENT: added support for bootstrap-ajax.js
- FEATURE: added a ``referral_responses`` assignment template tag
- FEATURE: added an ``activity_display`` template filter
- ENHANCEMENT: added a new classmethod on ``Referral`` for getting a referral
  object for a given ``request`` object.


0.4
---

- FEATURE: Add ability to define code generators external to anafero
- ENHANCEMENT: Add ability to pass in a user to `referral.respond` in
  cases when `request.user` isn't set yet (e.g. during signup)
- FEATURE: Add ability to get a referral object from a request


0.3
---

- FEATURE: changed user on Referral to be nullable, thus enabling anonymous or
  site administered referral codes


0.2.1
-----

- BUG: fixed target not being set in the `create_referral` ajax view

0.2
---

- DOC: fixed a typo in the docs
- ENHANCEMENT: added a response count property
- ENHANCEMENT: added the return of the referral code along with the URL in the
  ajax reponse of `create_referral`
- BUG: added the return of the proper mimetype in the `create_referral` ajax
  view
- ENHANCEMENT: moved the building of the URL for the referral code to a
  property on the Referral model
- FEATURE: added the ability to control referral code generation properties via
  settings at the site level
- BUG: fixed the url generation to include https if the site is configured to
  run SSL
- BUG: only delete cookies if user is present
- BUG: make sure to set a session value to prevent session key from changing
  with each request

0.1
---

- initial release
