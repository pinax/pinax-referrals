.. _changelog:

ChangeLog
=========

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
- ENHANCEMENT: added the return of the referral code along with the URL in the ajax reponse of `create_referral`
- BUG: added the return of the proper mimetype in the `create_referral` ajax view
- ENHANCEMENT: moved the building of the URL for the referral code to a property on the Referral model
- FEATURE: added the ability to control referral code generation properties via settings at the site level
- BUG: fixed the url generation to include https if the site is configured to run SSL
- BUG: only delete cookies if user is present
- BUG: make sure to set a session value to prevent session key from changing with each request

0.1
---

- initial release
