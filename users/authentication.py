from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import ExpiringToken


class ExpiringTokenAuthentication(TokenAuthentication):
    model = ExpiringToken

    def authenticate_credentials(self, key):
        """
        Authenticate the token and ensure it has not expired.
        """
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed("Invalid token. Please log in again.")

        if token.has_expired():
            # Silently delete the expired token
            token.delete()
            raise AuthenticationFailed(
                "Token has expired. Please log in again."
            )

        if not token.user.is_active:
            raise AuthenticationFailed("User is inactive or deleted.")

        return (token.user, token)
