from django.contrib.auth.models import User

from factory.django import DjangoModelFactory

from labster.models import Lab, LabProxy, Token, QuizBlock, Problem, \
    UserLabProxy, ErrorInfo, DeviceInfo


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    username = 'testusername'


class LabFactory(DjangoModelFactory):
    FACTORY_FOR = Lab


class QuizBlockFactory(DjangoModelFactory):
    FACTORY_FOR = QuizBlock


class ProblemFactory(DjangoModelFactory):
    FACTORY_FOR = Problem


class LabProxyFactory(DjangoModelFactory):
    FACTORY_FOR = LabProxy


class TokenFactory(DjangoModelFactory):
    FACTORY_FOR = Token


class UserLabProxyFactory(DjangoModelFactory):
    FACTORY_FOR = UserLabProxy


class ErrorInfoFactory(DjangoModelFactory):
	FACTORY_FOR = ErrorInfo


class DeviceInfoFactory(DjangoModelFactory):
    FACTORY_FOR = DeviceInfo