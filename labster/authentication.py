from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token


class GetTokenAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        key = request.GET.get('token')
        if not key:
            return None

        # cleanup key
        key = key.split('?')[0]

        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        return (token.user, token)
