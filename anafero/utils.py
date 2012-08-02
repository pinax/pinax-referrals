import random


def generate_code(referral_class):
    def _generate_code():
        t = "abcdefghijkmnopqrstuvwwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890"
        return "".join([random.choice(t) for i in range(40)])
    
    code = _generate_code()
    while referral_class.objects.filter(code=code).exists():
        code = _generate_code()
    return code


def ensure_session_key(request):
    """
    Given a request return a session key that will be used. There may already
    be a session key associated, but if there is not, we force the session to
    create itself and persist between requests for the client behind the given
    request.
    """
    key = request.session.session_key
    if key is None:
        # @@@ Django forces us to handle session key collision amongst
        # multiple processes (not handled)
        request.session.save()
        # force session to persist for client
        request.session.modified = True
        key = request.session.session_key
    return key
