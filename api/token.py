from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from api.models import Account


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            return Account.objects.get(email=validated_token['user_id'])
        except Account.DoesNotExist:
            raise InvalidToken('User not found')

    def authenticate(self, request):
        auth_header = self.get_header(request)
        if auth_header is None:
            return None

        raw_token = self.get_raw_token(auth_header)
        validated_token = self.get_validated_token(raw_token)

        user = self.get_user(validated_token)

        if user is None:
            raise AuthenticationFailed('User not found')

        user.is_authenticated = True
        request.user_id = validated_token['user_id']

        return (user, validated_token)