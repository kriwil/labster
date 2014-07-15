from django.contrib.auth.models import User

from factory.django import DjangoModelFactory

from labster.models import Lab, ErrorInfo, DeviceInfo, UserSave, Token, CourseLab


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    username = 'testusername'


class LabFactory(DjangoModelFactory):
    FACTORY_FOR = Lab


class CourseLabFactory(DjangoModelFactory):
    FACTORY_FOR = CourseLab


class TokenFactory(DjangoModelFactory):
    FACTORY_FOR = Token


class ErrorInfoFactory(DjangoModelFactory):
	FACTORY_FOR = ErrorInfo


class DeviceInfoFactory(DjangoModelFactory):
    FACTORY_FOR = DeviceInfo


class UserSaveFactory(DjangoModelFactory):
    FACTORY_FOR = UserSave
