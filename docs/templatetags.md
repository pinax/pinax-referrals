# Template Tags and Filters

## create_referral

In order to use `pinax-referrals` in your project you will use the
`create_referral` template tag wherever you'd like a user to be able to get a
referral link to a page or a particular object:

    {% load pinax_referrals_tags %}
    
    {% create_referral object.get_absolute_url object %}

The use of `object` in this case is optional if you just want to record
referrals to a particular url. In that case you can just do:

    {% load pinax_referrals_tags %}
    
    {% url my_named_url as myurl %}
    
    {% create_referral myurl %}

This will render a form that is defined in `pinax/referrals/_create_referral_form.html`
which will POST to a view and return JSON. The intent of this form is that it
is to be used with an AJAX submission and handler.

The recommended way is to use `jquery.form` and to do the following:

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


## referral_responses

This template tag is an assignment tag that given a user sets an context
variable with a queryset all all responses for all referrals owned by the
user, in order of when they were created.

The use case for where this is useful is displaying all the activities
associated with the user's different labeled referrals.

Example:

    {% load pinax_referrals_tags %}
    {% referral_responses user as responses %}
    
    {% for response in responses %}
        {# response is a ReferralResponse object #}
    {% endfor %}


## action_display

This filter converts a response code into a user friendly display of what that
code means. The definitions exist in the setting `PINAX_REFERRALS_ACTION_DISPLAY`.

    {% load pinax_referrals_tags %}
    
    <p>
        {{ response.action|action_display }}
    </p>
