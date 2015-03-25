# Usage

## Referral.create

This is the factory method that the `create_referral` view calls but can
be called directly in case you needed to integrate in a different way with
pinax-referrals.

For example, you might want to automatically give every user a referral code
that is emailed to them upon signup. In this case, you could created a one
to one relationshiop between their `Profile` and pinax-referrals' `Referral` and
create a signal receiver for when the `Profile` is created that calls:

    referral = Referral.create(
        user=profile.user,
        redirect_to=reverse("home")
    )
    profile.referral = referral
    profile.save()

Then you could, in the welcome email that you send them upon signup render
their referral url that they could forward on to other users:

    {{ user.get_profile.referral.url }}

The only required parameter for `Referral.create` is `redirect_to`. If
you don't specify a user it will be recorded as `None`. This can be useful
if you wanted to attach a relationship between some object in your system
to a referral that might not have a user associated with it.

You can also pass in an optional `label` kwarg to `Referral.create` if
you wanted to allow your users to create and manage multiple referrals so
that labeling them became important to keep track of them.

At runtime, you can append the `redirect_to` URL parameter to your referral
URL to dynamically redirect to an alternate destination.

    {{ user.get_profile.referral.url }}?redirect_to=/special/

The URL parameter used can be altered in your [settings](settings.md) file.


## Referral.record_response

The classmethod `record_response` will attempt to see if the current user or
session has any previous responses to an initial referral and if so will then
proceed to record the response action.

For example, say you want to record the fact that the user did some site activity
after clicking on the referral link you tweeted and subsequently decided
to register and login to the site:

    from pinax.referrals.models import Referral
    
    
    def my_view(request, **kwargs):
        ...
        referral_response = Referral.record_response(request, "SOME_ACTION")
        ...

In this case the `referral_response` will be None if the user on the request
doesn't have any previously recorded referral responses. In addition, if the user
has responded to more than one Referral code, then this will associate the
activity with the most recent response.

In addition, this supports passing an options `target` keyward argument, if
you wanted to record associations with specific objects. For example:

    Referral.record_response(request, "SOME_ACTION", target=some_object)

This will record a generic foreign key to `some_object` that you can use elsewhere
to identify activity from your referral at a deeper level than just based on
the action label.


## Referral.referral_for_request

This class method, will give you a referral object for the given request in
case you needed to apply any business logic in your project. For example, to
do any comparisons on the referral.target with another object you have in
context for segmenting permissions or authorizations to make your referral
system more fine grained.

