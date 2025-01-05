from .models import Subscription


def seed_subscriptions():
    subscriptions = [
        {
            "name": "Trail",
            "price": 0,
            "validity": 15,
        },
        {
            "name": "Premium",
            "price": 10,
            "validity": 90,
        },
    ]

    for subscription in subscriptions:
        Subscription.objects.get_or_create(**subscription)
