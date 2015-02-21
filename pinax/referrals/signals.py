import django.dispatch


user_linked_to_response = django.dispatch.Signal(providing_args=["response"])
