from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token
from django.utils.timezone import now, timedelta


class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15, unique=True)


class ExpiringToken(Token):
    device = models.CharField(max_length=255, null=True, blank=True)
    expires_at = models.DateTimeField()

    def has_expired(self):
        return self.expires_at and now() > self.expires_at
