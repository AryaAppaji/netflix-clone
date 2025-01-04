from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import ExpiringToken


class ExpiringTokenAuthentication(TokenAuthentication):
    model = ExpiringToken

    def authenticate(self, request):
        """
        Override the authenticate method to ensure token is provided.
        """
        auth = request.META.get("HTTP_AUTHORIZATION", "").split()

        if not auth or len(auth) != 2:
            raise AuthenticationFailed(
                "Token was not provided, please provide one."
            )

        token = auth[1]  # Get token from the header

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        """
        Authenticate the token and ensure it has not expired.
        """
        if not key:
            raise AuthenticationFailed(
                "Token was not provided, please provide one."
            )

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
