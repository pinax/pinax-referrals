.. _usage:

Usage
=====

.. _create_referral:

create_referral
---------------

In order to use `anafero` in your project you will use the `create_referral`
template tag wherever you'd like a user to be able to get a referral link
to a page or a particular object::

    {% load anafero_tags %}
    
    {% create_referral object.get_absolute_url object %}

The use of `object` in this case is optional if you just want to record
referrals to a particular url. In that case you can just do::

    {% load anafero_tags %}
    
    {% url my_named_url as myurl %}
    
    {% create_referral myurl %}

This will render a form that is defined in `anafero/_create_referral_form.html`
which will POST to a view and return JSON. The intent of this form is that it
is to be used with an AJAX submission and handler.

The recommended way is to use `jquery.form` and to do the following::

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


.. _Referral.create

Referral.create
---------------

This is the factory method that the ``create_referral`` view calls but can
be called directly in case you needed to integrate in a different way with
anafero.

For example, you might want to automatically give every user a referral code
that is emailed to them upon signup. In this case, you could created a one
to one relationshiop between their ``Profile`` and anafero's ``Referral`` and
create a signal receiver for when the ``Profile`` is created that calls::

    referral = Referral.create(
        user=profile.user,
        redirect_to=reverse("home")
    )
    profile.referral = referral
    profile.save()

Then you could, in the welcome email that you send them upon signup render
their referral url that they could forward on to other users::

    {{ user.get_profile.referral.url }}

The only required parameter for ``Referral.create`` is ``redirect_to``. If
you don't specify a user it will be recorded as ``None``. This can be useful
if you wanted to attach a relationship between some object in your system
to a referral that might not have a user associated with it.


.. _Referral.record_response:

Referral.record_response
------------------------

The classmethod ``record_response`` will attempt to see if the current user or
session has any previous responses to an initial referral and if so will then
proceed to record the response action.

For example, say you want to record the fact that the user did some site activity
after clicking on the referral link you tweeted and subsequently decided
to register and login to the site::

    from anafero.models import Referral
    
    
    def my_view(request, **kwargs):
        ...
        referral_response = Referral.record_response(request, "SOME_ACTION")
        ...

In this case the ``referral_response`` will be None if the user on the request
doesn't have any previously recorded referral responses. In addition, if the user
has responded to more than one Referral code, then this will associate the
activity with the most recent response.
