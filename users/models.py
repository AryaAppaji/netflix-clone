from django.contrib.auth.models import AbstractUser
from django.db import models
from finance.models import Subscription


class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15, unique=True)


class UserSubscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="subscription",
    )
    subscription = models.ForeignKey(
        Subscription,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="subscription_details",
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_current_subscription = models.BooleanField()

    class Meta:
        db_table = "user_subscriptions"
