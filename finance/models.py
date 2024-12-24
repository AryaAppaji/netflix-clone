from django.db import models
from users.models import CustomUser


# Create your models here.
class Subscription(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()
    validity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subscriptions"

    def __str__(self):
        return self.name


class PaymentMode(models.Model):
    name = models.CharField(max_length=30)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payment_modes"

    def __str__(self) -> str:
        return self.name


class Payment(models.Model):
    user = models.ForeignKey(
        CustomUser,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    subscription = models.ForeignKey(
        Subscription,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="subscription",
    )
    payment_mode = models.ForeignKey(
        PaymentMode,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="payment_mode",
    )
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payments"

    def __str__(self) -> str:
        return f"{self.user.username}-{self.date}-{self.amount}"


class UserSubscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        db_index=True,
        on_delete=models.CASCADE,
        related_name="user_subscription",
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
