.. _usage:

Usage
=====

.. _create_referral:

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
        $('form.referral').ajaxForm(function(data) {
            if (data.status == "OK") {
                $(this).html('<input type="text" value="' + data.url + '" />');
            } else {
                $(this).html('<div class="error">' + data.errors + '</div>');
            }
        });
    });
