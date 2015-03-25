# pinax-referrals

!!! note "Pinax Ecosystem"
    This app was developed as part of the Pinax ecosystem but is just a Django app
    and can be used independently of other Pinax apps.
    
    To learn more about Pinax, see <http://pinaxproject.com/>

Provides a site with the ability for users to publish referral links to
specific pages or objects and then record any responses to those links
for subsequent use by the site.

For example, on an object detail page, the site builder would use a
template tag from `pinax-referrals` to display a referral link that the user of the
site can send out in a Tweet. Upon clicking that link, a response to that
referral code will be recorded as well as any other activity that the site
builder wants to track for that session.

It is also possible for anonymous referral links/codes to be generated
which is useful in marketing promotions and the like.


## Development

The source repository can be found at https://github.com/pinax/pinax-referrals
