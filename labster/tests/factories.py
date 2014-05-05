from django.contrib.auth.models import User

from factory.django import DjangoModelFactory

from labster.models import Lab, LabProxy, Token


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    username = 'testusername'


class LabFactory(DjangoModelFactory):
    FACTORY_FOR = Lab


class LabProxyFactory(DjangoModelFactory):
    FACTORY_FOR = LabProxy


class TokenFactory(DjangoModelFactory):
    FACTORY_FOR = Token
