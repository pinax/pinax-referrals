![](http://pinaxproject.com/pinax-design/patches/pinax-referrals.svg)

# Pinax Referrals

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/) [![](https://img.shields.io/travis/pinax/pinax-referrals.svg)](https://travis-ci.org/pinax/pinax-referrals) [![](https://img.shields.io/coveralls/pinax/pinax-referrals.svg)](https://coveralls.io/r/pinax/pinax-referrals) [![](https://img.shields.io/pypi/dm/pinax-referrals.svg)](https://pypi.python.org/pypi/pinax-referrals/) [![](https://img.shields.io/pypi/v/pinax-referrals.svg)](https://pypi.python.org/pypi/pinax-referrals/) [![](https://img.shields.io/badge/license-MIT-blue.svg)](https://pypi.python.org/pypi/pinax-referrals/)

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


## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Settings](#settings)
* [Signals](#signals)
* [Templates](#templates)
* [Development](#development)
* [Change Log](#change-log)
* [Project History](#history)
* [About Pinax](#about-pinax)

## Installation

To install pinax-referrals:

```
 pip install pinax-referrals
```

Add `pinax.referrals` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = (
    # other apps
    "pinax.referrals",
)
```

See the list of [settings](#settings) to modify `pinax-referrals`'s default
behavior and make adjustments for your website.

Add `pinax.referrals.middleware.SessionJumpingMiddleware` in order to link up a
user who registers and authenticate after hitting the initial referral link.
Make sure that it comes after the `django.contrib.auth.middleware.AuthenticationMiddleware`:

```python
MIDDLEWARE = [
    ...
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    ...
    "pinax.referrals.middleware.SessionJumpingMiddleware",
    ...
]
```

*Note: use `MIDDLEWARE_CLASSES` instead in case you're still using Django 1.8 or 1.9*

Lastly you will want to add `pinax.referrals.urls` to your urls definition:

```python
url(r"^referrals/", include("pinax.referrals.urls")),
```

## Usage

### `Referral.create`

This is the factory method that the `create_referral` view calls but it can
be called directly in case you needed to integrate with pinax-referrals in
a different way.

For example, you might want to automatically give every user a referral code
that is emailed to them upon signup. In this case, you could created a one-to-one
relationshiop between their `Profile` and pinax-referrals' `Referral` and
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


### `Referral.record_response`

The classmethod `record_response` will attempt to see if the current user or
session has any previous responses to an initial referral and, if so, will then
proceed to record the response action.

For example, say you want to record the fact that the user did some site activity
after clicking on the referral link you tweeted and subsequently decided
to register and login to the site:

```python
from pinax.referrals.models import Referral


def my_view(request, **kwargs):
    ...
    referral_response = Referral.record_response(request, "SOME_ACTION")
    ...
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


### `Referral.referral_for_request`

This class method will give you a referral object for the given request in
case you need to apply any business logic in your project. For example, to
do any comparisons on the referral.target with another object you have in
context for segmenting permissions or authorizations to make your referral
system more fine grained.



## Settings

### `PINAX_REFERRALS_IP_ADDRESS_META_FIELD`

Defaults to `"HTTP_X_FORWARDED_FOR"`

This is the header value that is retrieved from `request.META` to record
the ip address of the the respondent.


### `PINAX_REFERRALS_SECURE_URLS`

Defaults to `False`

Setting this to `True` will produce urls with `https` instead of `http`.


### `PINAX_REFERRALS_CODE_GENERATOR_CALLBACK`

Defaults to `"pinax.referrals.utils.generate_code"`

Externalizes the logic that generates the referral code. `pinax-referrals` ships
with a default that will generate a random 40-character alpha-numeric
string that can also be used as a reference implementation. The callable
defined by the fully qualified path is passed a single parameter that is
the class of the referral model, or `Referral`. This is done as a pure
convenience so as to alleviate the need for you to have to import it
should you need it (and you most likely will if you want to be
certain of uniqueness).


### `PINAX_REFERRALS_ACTION_DISPLAY`

Defaults to `{"RESPONDED": "Clicked on referral link"}`

Defines a dictionary mapping action codes for responses to user-friendly
display text. Used by the `action_display` template filter.


### `PINAX_REFERRALS_REDIRECT_ATTRIBUTE`

Defaults to `redirect_to`

Defines the URL attribute to retrieve dynamic referral redirection URLs from.

## Signals

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

## Templates

`pinax-referrals` comes with a single template fragment for rendering a simple
form that is used in creating a referral link.


### `_create_referral_form.html`

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


## Template Tags and Filters

### `create_referral`

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

### `referral_responses`

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

### `action_display`

This filter converts a response code into a user friendly display of what that
code means. The definitions exist in the setting `PINAX_REFERRALS_ACTION_DISPLAY`.

```django
{% load pinax_referrals_tags %}

<p>
    {{ response.action|action_display }}
</p>
```


## Development

### Migrations

If you need to make migrations for pinax-referrals, run:

```
python manage.py makemigrations referrals
```

You may need to do this if you use a custom user model and upgrade
Django.


### Contribute

See the [Recap of February Pinax Hangout](http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/) including a video, or our [How to Contribute](http://pinaxproject.com/pinax/how_to_contribute/) section for an overview on how contributing to Pinax works. For concrete contribution ideas, please see our [Ways to Contribute/What We Need Help With] (http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions, we recommend you join our [Pinax Slack team] (http://slack.pinaxproject.com) and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course also valid but we are usually able to help you faster if you ping us in Slack.

We also highly recommend reading our [Open Source and Self-Care](http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/)  blog post.

### Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a [code of conduct](http://pinaxproject.com/pinax/code_of_conduct/). We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Change Log

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

* ENHANCEMENT: Rewrote ``referral_responses`` to run on Django 1.3


### 0.6

* ENHANCEMENT: send full context to the ``create_referral`` template tag


### 0.5.2

* BUG: Fixed a stupid mistake


### 0.5.1

* BUG: fixed an issue with sessions in Django 1.4


### 0.5

* FEATURE: added ability to label referrals
* ENHANCEMENT: added support for bootstrap-ajax.js
* FEATURE: added a ``referral_responses`` assignment template tag
* FEATURE: added an ``activity_display`` template filter
* ENHANCEMENT: added a new classmethod on ``Referral`` for getting a referral
  object for a given ``request`` object.

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
``pinax-referrals``.


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.

The Pinax documentation is available at http://pinaxproject.com/pinax/. If you would like to help us improve our documentation or write more documentation, please join our Pinax Project Slack team and let us know!

For updates and news regarding the Pinax Project, please follow us on Twitter at @pinaxproject and check out our blog http://blog.pinaxproject.com.

