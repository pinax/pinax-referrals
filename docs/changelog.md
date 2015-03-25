# Change Log

## 2.0.0

* Renamed from `anafero` to `pinax-referrals`
* Brought up to date with latest Pinax app standards


## 1.0.1

* Fix deprecation warning in urls


## 1.0

* ENHANCEMENT: made GFK fields on `Referral` blankable


## 0.10.0

* ENHANCEMENT: added a signal to provide notifications of when a referred user authenticates


## 0.9.1

* BUG: Fix issue where target response is None


## 0.9

* FEATURE: added ability to record a specific object in reference to each response

### Migration from 0.8.1

    ALTER TABLE "anafero_referralresponse"
     ADD COLUMN "target_content_type_id" integer REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
     ADD COLUMN "target_object_id" integer;


## 0.8.1

* ENHANCEMENT: switched over to use `django.utils.timezone.now` instead of `datetime.datetime.now`


## 0.8

* FEATURE: added ability to override filtering of responses


## 0.7

* ENHANCEMENT: Made admin a bit more usable


## 0.6.1

* ENHANCEMENT: Rewrote ``referral_responses`` to run on Django 1.3


## 0.6

* ENHANCEMENT: send full context to the ``create_referral`` template tag


## 0.5.2

* BUG: Fixed a stupid mistake


## 0.5.1

* BUG: fixed an issue with sessions in Django 1.4


## 0.5

* FEATURE: added ability to label referrals
* ENHANCEMENT: added support for bootstrap-ajax.js
* FEATURE: added a ``referral_responses`` assignment template tag
* FEATURE: added an ``activity_display`` template filter
* ENHANCEMENT: added a new classmethod on ``Referral`` for getting a referral
  object for a given ``request`` object.

### Migration from 0.4

    ALTER TABLE "anafero_referral" ADD COLUMN "label" varchar(100) NOT NULL DEFAULT '';


## 0.4

* FEATURE: Add ability to define code generators external to anafero
* ENHANCEMENT: Add ability to pass in a user to `referral.respond` in
  cases when `request.user` isn't set yet (e.g. during signup)
* FEATURE: Add ability to get a referral object from a request


## 0.3

* FEATURE: changed user on Referral to be nullable, thus enabling anonymous or
  site administered referral codes


## 0.2.1

* BUG: fixed target not being set in the `create_referral` ajax view


## 0.2

* DOC: fixed a typo in the docs
* ENHANCEMENT: added a response count property
* ENHANCEMENT: added the return of the referral code along with the URL in the
  ajax reponse of `create_referral`
* BUG: added the return of the proper mimetype in the `create_referral` ajax
  view
* ENHANCEMENT: moved the building of the URL for the referral code to a
  property on the Referral model
* FEATURE: added the ability to control referral code generation properties via
  settings at the site level
* BUG: fixed the url generation to include https if the site is configured to
  run SSL
* BUG: only delete cookies if user is present
* BUG: make sure to set a session value to prevent session key from changing
  with each request


## 0.1

* initial release
