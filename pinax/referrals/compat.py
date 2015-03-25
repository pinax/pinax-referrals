try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey  # noqa

try:
    import importlib
except ImportError:
    from django.utils import importlib  # noqa
