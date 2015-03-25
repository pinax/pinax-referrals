# Templates

`pinax-referrals` comes with a single template fragment for rendering a simple
form that is used in creating a referral link.


## _create_referral_form.html

This is a snippet that renders the form that upon submission will create the
referral link. By default it is rendered with the class `referral` with the
following context variables:

    {
        "url": url,
        "obj": obj,
        "obj_ct": ContentType.objects.get_for_model(obj)
    }

or if no object was passed into the `create_referral` template tag then
the context would simply blank for `obj` and `obj_ct`.
