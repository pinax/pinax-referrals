.. _templatetags:

Template Tags and Filters
=========================

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


.. _referral_responses:

referral_responses
------------------

This template tag is an assignment tag that given a user sets an context
variable with a queryset all all responses for all referrals owned by the
user, in order of when they were created.

The use case for where this is useful is displaying all the activities
associated with the user's different labeled referrals. Example::

    {% load anafero_tags %}
    {% referral_responses user as responses %}
    
    {% for response in responses %}
        {# response is a ReferralResponse object #}
    {% endfor %}
