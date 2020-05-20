import importlib

from django.core.exceptions import ImproperlyConfigured


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


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1:]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured(f"Error importing {module}: '{e}'")
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(f"Module '{module}' does not define a '{attr}'")
    return attr
