import unittest

from django.contrib.auth.models import User
from django.test.client import RequestFactory

from factory.django import DjangoModelFactory

from labster.models import Lab, LabProxy
from labster.api.views import quizblocks


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    username = 'testusername'


class LabFactory(DjangoModelFactory):
    FACTORY_FOR = Lab


class LabProxyFactory(DjangoModelFactory):
    FACTORY_FOR = LabProxy


class QuizblocksViewTest(unittest.TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.lab_proxy = LabProxyFactory(lab=self.lab)
        self.user = UserFactory(is_superuser=True)

    def test_get(self):
        request = RequestFactory().get('/')
        response = quizblocks(request, proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 200)
