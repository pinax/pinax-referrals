import django.dispatch

# providing_args=["response"]
user_linked_to_response = django.dispatch.Signal()
