# Signals

`user_linked_to_response` is a signal that provides the single argument of a
`response` object that has just been linked to a user. You can use this to
provide further automatic processing within your site, such as adding
permissions, etc. to users that signup as a result of a referral.

For example:

    @receiver(user_linked_to_response)
    def handle_user_linked_to_response(sender, response, **kwargs):
        if response.action == "SOME_SPECIAL_ACTION":
            pass  # do something with response.user and response.referral.target (object that referral was linked to)
