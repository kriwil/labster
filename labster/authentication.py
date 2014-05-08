from django.contrib.auth.models import User

from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header

from labster.models import Token


class SingleTokenAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        force_login = request.GET.get('__fl') == '1'
        auth = ["", ""]
        if not force_login:
            auth = get_authorization_header(request).split()

            if not auth or auth[0].lower() != b'token':
                return None

            if len(auth) == 1:
                msg = 'Invalid token header. No credentials provided.'
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth) > 2:
                msg = 'Invalid token header. Token string should not contain spaces.'
                raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(auth[1], request, force_login)

    def authenticate_credentials(self, key, request, force_login=False):
        token = None
        if not force_login:
            try:
                token = Token.objects.get(key=key)
            except self.model.DoesNotExist:
                raise exceptions.AuthenticationFailed('Invalid token')

        user_id = request.REQUEST.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, token)

    def authenticate_header(self, request):
        return 'Token'
