import json
import random

from factory.django import DjangoModelFactory

from django.contrib.auth.models import User

from labster.models import Lab, ErrorInfo, DeviceInfo, UserSave, Token, LabProxy


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


class ErrorInfoFactory(DjangoModelFactory):
    FACTORY_FOR = ErrorInfo


class DeviceInfoFactory(DjangoModelFactory):
    FACTORY_FOR = DeviceInfo


class UserSaveFactory(DjangoModelFactory):
    FACTORY_FOR = UserSave


class DummyUsageKey:
    pass


class DummyModulestore:
    pass


class DummyXblockResult:
    content = json.dumps({'correct': True})


class DummyProblemLocator:
    category = 'category'
    course = 'course'
    name = 'name'
    org = 'org'
    tag = 'tag'


def create_lab_proxy(**kwargs):
    if 'location' not in kwargs:
        kwargs['location'] = '%030x' % random.randrange(16**30)
    return LabProxyFactory(**kwargs)
