![](http://pinaxproject.com/pinax-design/patches/pinax-referrals.svg)

# Pinax Referrals

[![](https://img.shields.io/pypi/v/pinax-referrals.svg)](https://pypi.python.org/pypi/pinax-referrals/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-referrals.svg)](https://circleci.com/gh/pinax/pinax-referrals)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-referrals.svg)](https://codecov.io/gh/pinax/pinax-referrals)
[![](https://img.shields.io/github/contributors/pinax/pinax-referrals.svg)](https://github.com/pinax/pinax-referrals/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-referrals.svg)](https://github.com/pinax/pinax-referrals/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-referrals.svg)](https://github.com/pinax/pinax-referrals/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
 
 
## Table of Contents

* [About Pinax](#about-pinax)
* [Important Links](#important-links)
* [Overview](#overview)
  * [Supported Django and Python Versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Settings](#settings)
  * [Signals](#signals)
  * [Templates](#templates)
  * [Template Tags and Filters](#template-tags-and-filters)
  * [Development](#development)
* [Change Log](#change-log)
* [History](#history)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.


## Important Links

Where you can find what you need:
* Releases: published to [PyPI](https://pypi.org/search/?q=pinax) or tagged in app repos in the [Pinax GitHub organization](https://github.com/pinax/)
* Global documentation: [Pinax documentation website](https://pinaxproject.com/pinax/)
* App specific documentation: app repos in the [Pinax GitHub organization](https://github.com/pinax/)
* Support information: [SUPPORT.md](https://github.com/pinax/.github/blob/master/SUPPORT.md) file in the [Pinax default community health file repo](https://github.com/pinax/.github/)
* Contributing information: [CONTRIBUTING.md](https://github.com/pinax/.github/blob/master/CONTRIBUTING.md) file in the [Pinax default community health file repo](https://github.com/pinax/.github/)
* Current and historical release docs: [Pinax Wiki](https://github.com/pinax/pinax/wiki/)


## pinax-referrals

### Overview

`pinax-referrals` provides a site with the ability for users to
publish referral links to specific pages or objects and then record
any responses to those links for subsequent use by the site.

For example, on an object detail page, the site builder would use a
template tag from `pinax-referrals` to display a referral link that the user of the
site can send out in a Tweet. Upon clicking that link, a response to that
referral code will be recorded as well as any other activity that the site
builder wants to track for that session.

It is also possible for anonymous referral links/codes to be generated
which is useful in marketing promotions and the like.

#### Supported Django and Python Versions

Django / Python | 3.6 | 3.7 | 3.8
--------------- | --- | --- | ---
2.2  |  *  |  *  |  *
3.0  |  *  |  *  |  *


## Documentation

### Installation

To install pinax-referrals:

```shell
    $ pip install pinax-referrals
```

Add `pinax.referrals` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    # other apps
    "pinax.referrals",
]
```

See the list of [settings](#settings) to modify `pinax-referrals`'s default
behavior and make adjustments for your website.

Add `pinax.referrals.middleware.SessionJumpingMiddleware` in order to link up a
user who registers and authenticate after hitting the initial referral link.
Make sure that it comes after the `django.contrib.auth.middleware.AuthenticationMiddleware`:

```python
MIDDLEWARE = [
    # other middleware
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "pinax.referrals.middleware.SessionJumpingMiddleware",
]
```

Lastly add `pinax.referrals.urls` to your urls definition:

```python
urlpatterns = [
    # other urls
    url(r"^referrals/", include("pinax.referrals.urls", namespace="pinax_referrals")),
]
```

### Usage

#### `Referral.create`

This is the factory method that the `create_referral` view calls but it can
be called directly in case you needed to integrate with pinax-referrals in
a different way.

For example, you might want to automatically give every user a referral code
that is emailed to them upon signup. In this case, you could created a one-to-one
relationship between their `Profile` and pinax-referrals' `Referral` and
create a signal receiver for when the `Profile` is created that calls:

```python
referral = Referral.create(
    user=profile.user,
    redirect_to=reverse("home")
)
profile.referral = referral
profile.save()
```

Then you could, in the welcome email that you send them upon signup, render
their referral url that they could forward on to other users:

```django
    {{ user.get_profile.referral.url }}
```

The only required parameter for `Referral.create` is `redirect_to`. If
you don't specify a user it will be recorded as `None`. This can be useful
if you want to attach a relationship between some object in your system
to a referral that might not have a user associated with it.

You can also pass in an optional `label` kwarg to `Referral.create` if
you want to allow your users to create and manage multiple referrals as
labeling them becomes important in order to keep track of them.

At runtime, you can append the `redirect_to` URL parameter to your referral
URL to dynamically redirect to an alternate destination.

```django
{{ user.get_profile.referral.url }}?redirect_to=/special/
```

The URL parameter used can be altered in your [settings](#settings) file.

#### `Referral.record_response`

The classmethod `record_response` will attempt to see if the current user or
session has any previous responses to an initial referral and, if so, will then
proceed to record the response action.

For example, say you want to record the fact that the user did some site activity
after clicking on the referral link you tweeted and subsequently decided
to register and login to the site:

```python
from pinax.referrals.models import Referral


def my_view(request, **kwargs):
    # other code
    referral_response = Referral.record_response(request, "SOME_ACTION")
```

In this case the `referral_response` will be None if the user on the request
doesn't have any previously recorded referral responses. In addition, if the user
has responded to more than one Referral code, then this will associate the
activity with the most recent response.

In addition, this supports passing an options `target` keyward argument, if
you wanted to record associations with specific objects. For example:

```python
Referral.record_response(request, "SOME_ACTION", target=some_object)
```

This will record a generic foreign key to `some_object` that you can use elsewhere
to identify activity from your referral at a deeper level than just based on
the action label.

#### `Referral.referral_for_request`

This class method will give you a referral object for the given request in
case you need to apply any business logic in your project. For example, to
do any comparisons on the referral.target with another object you have in
context for segmenting permissions or authorizations to make your referral
system more fine grained.

### Settings

#### `PINAX_COOKIE_MAX_AGE`

Defaults to `None`

The total amount of time (in seconds) the cookie lasts in the client's browser.

#### `PINAX_REFERRALS_IP_ADDRESS_META_FIELD`

Defaults to `"HTTP_X_FORWARDED_FOR"`

This is the header value that is retrieved from `request.META` to record
the ip address of the the respondent.

#### `PINAX_REFERRALS_SECURE_URLS`

Defaults to `False`

Setting this to `True` will produce urls with `https` instead of `http`.

#### `PINAX_REFERRALS_CODE_GENERATOR_CALLBACK`

Defaults to `"pinax.referrals.callbacks.generate_code"`

Externalizes the logic that generates the referral code. `pinax-referrals` ships
with a default that will generate a random 40-character alpha-numeric
string that can also be used as a reference implementation. The callable
defined by the fully qualified path is passed a single parameter that is
the class of the referral model, or `Referral`. This is done as a pure
convenience so as to alleviate the need for you to have to import it
should you need it (and you most likely will if you want to be
certain of uniqueness).

#### `PINAX_REFERRALS_ACTION_DISPLAY`

Defaults to `{"RESPONDED": "Clicked on referral link"}`

Defines a dictionary mapping action codes for responses to user-friendly
display text. Used by the `action_display` template filter.

#### `PINAX_REFERRALS_REDIRECT_ATTRIBUTE`

Defaults to `redirect_to`

Defines the URL attribute to retrieve dynamic referral redirection URLs from.

### Signals

`user_linked_to_response` is a signal that provides the single argument of a
`response` object that has just been linked to a user. You can use this to
provide further automatic processing within your site, such as adding
permissions, etc. to users that signup as a result of a referral.

For example:

```python
@receiver(user_linked_to_response)
def handle_user_linked_to_response(sender, response, **kwargs):
    if response.action == "SOME_SPECIAL_ACTION":
        pass  # do something with response.user and response.referral.target (object that referral was linked to)
```

### Templates

`pinax-referrals` comes with a single template fragment for rendering a simple
form that is used in creating a referral link.

#### `_create_referral_form.html`

This is a snippet that renders the form that upon submission will create the
referral link. By default it is rendered with the class `referral` with the
following context variables:

```python
{
    "url": url,
    "obj": obj,
    "obj_ct": ContentType.objects.get_for_model(obj)
}
```

or if no object was passed into the `create_referral` template tag then
the context would simply blank for `obj` and `obj_ct`.

### Template Tags and Filters

#### `create_referral`

In order to use `pinax-referrals` in your project you will use the
`create_referral` template tag wherever you'd like a user to be able to get a
referral link to a page or a particular object:

```django
{% load pinax_referrals_tags %}

{% create_referral object.get_absolute_url object %}
```

The use of `object` in this case is optional if you just want to record
referrals to a particular url. In that case you can just do:

```django
{% load pinax_referrals_tags %}

{% url my_named_url as myurl %}

{% create_referral myurl %}
```

This will render a form that is defined in `pinax/referrals/_create_referral_form.html`
which will POST to a view and return JSON. The intent of this form is that it
be used with an AJAX submission and handler.

The recommended way is to use `jquery.form` and to do the following:

```javascript
$(function () {
    $('form.referral').each(function(i, e) {
        var form = $(e);
        options = {
            dataType: "json",
            success: function(data) {
                form.html('<input type="text" value="' + data.url + '" />');
                form.find("input[type=text]").select();
            }
        }
        form.ajaxForm(options);
    });
});
```

#### `referral_responses`

This template tag is an assignment tag that, given a user, sets a context
variable with a queryset of all responses for all referrals owned by the
user, in order of when they were created.

The use case for this is displaying all the activities
associated with the user's different labeled referrals.

Example:

```django
{% load pinax_referrals_tags %}
{% referral_responses user as responses %}

{% for response in responses %}
    {# response is a ReferralResponse object #}
{% endfor %}
```

#### `action_display`

This filter converts a response code into a user friendly display of what that
code means. The definitions exist in the setting `PINAX_REFERRALS_ACTION_DISPLAY`.

```django
{% load pinax_referrals_tags %}

<p>
    {{ response.action|action_display }}
</p>
```

### Development

#### Migrations

If you need to make migrations for pinax-referrals, run:

```shell
    $ python manage.py makemigrations referrals
```

You may need to do this if you use a custom user model and upgrade Django.


## Change Log

### 4.0.2

* Added setting to set the cookie's max age in client's browser

### 4.0.1

* Changes to admin.py and models.py to increase overridability

### 4.0.0

* Drop Django 1.11, 2.0, and 2.1, and Python 2,7, 3.4, and 3.5 support
* Add Django 2.2 and 3.0, and Python 3.6, 3.7, and 3.8 support
* Update packaging configs
* Direct users to community resources

### 3.0.5

* Simple fix for [#46](https://github.com/pinax/pinax-referrals/issues/46). Increase the length of the ip_address, so IPv6 address array from HTTP_X_FORWARDED_FOR can be stored.

### 3.0.4

* Fixing search in referral admin against "user"

### 3.0.3

* Changes to setup.py

### 3.0.2

* Use Django 2.0 `reverse` import

### 3.0.1

* Change `is_authenticated` to property in models.py

### 3.0.0

* Add Django 2.0 compatibility testing
* Drop Django 1.9 and Python 3.3 support
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description
* Add URL namespacing
* Standardize documentation layout
* Drop Django v1.8, v1.10 support
* Update installation requirements for django>=1.11
* Remove unused doc build support

### 2.0.0

* Renamed from `anafero` to `pinax-referrals`
* Brought up to date with latest Pinax app standards

### 1.0.1

* Fix deprecation warning in urls

### 1.0

* ENHANCEMENT: made GFK fields on `Referral` blankable

### 0.10.0

* ENHANCEMENT: added a signal to provide notifications of when a referred user authenticates

### 0.9.1

* BUG: Fix issue where target response is None

### 0.9

* FEATURE: added ability to record a specific object in reference to each response

#### Migration from 0.8.1

    ALTER TABLE "anafero_referralresponse"
     ADD COLUMN "target_content_type_id" integer REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
     ADD COLUMN "target_object_id" integer;

### 0.8.1

* ENHANCEMENT: switched over to use `django.utils.timezone.now` instead of `datetime.datetime.now`

### 0.8

* FEATURE: added ability to override filtering of responses

### 0.7

* ENHANCEMENT: Made admin a bit more usable

### 0.6.1

* ENHANCEMENT: Rewrote `referral_responses` to run on Django 1.3

### 0.6

* ENHANCEMENT: send full context to the `create_referral` template tag

### 0.5.2

* BUG: Fixed a stupid mistake

### 0.5.1

* BUG: fixed an issue with sessions in Django 1.4

### 0.5

* FEATURE: added ability to label referrals
* ENHANCEMENT: added support for bootstrap-ajax.js
* FEATURE: added a `referral_responses` assignment template tag
* FEATURE: added an `activity_display` template filter
* ENHANCEMENT: added a new classmethod on `Referral` for getting a referral
  object for a given `request` object.

### Migration from 0.4

    ALTER TABLE "anafero_referral" ADD COLUMN "label" varchar(100) NOT NULL DEFAULT '';

### 0.4

* FEATURE: Add ability to define code generators external to anafero
* ENHANCEMENT: Add ability to pass in a user to `referral.respond` in
  cases when `request.user` isn't set yet (e.g. during signup)
* FEATURE: Add ability to get a referral object from a request

### 0.3

* FEATURE: changed user on Referral to be nullable, thus enabling anonymous or
  site administered referral codes

### 0.2.1

* BUG: fixed target not being set in the `create_referral` ajax view

### 0.2

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

### 0.1

* initial release


## History

This project was originally named `anafero` and was created by the team at Eldarion. It was later donated to Pinax and at that time renamed to
`pinax-referrals`.


## Contribute

[Contributing](https://github.com/pinax/.github/blob/master/CONTRIBUTING.md) information can be found in the [Pinax community health file repo](https://github.com/pinax/.github).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a [Code of Conduct](https://github.com/pinax/.github/blob/master/CODE_OF_CONDUCT.md). We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject) and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-present James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).
