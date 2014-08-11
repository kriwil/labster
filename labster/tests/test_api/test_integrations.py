from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework.authtoken.models import Token

from labster.models import ErrorInfo, DeviceInfo, UserSave, UserAttempt
from labster.tests.factories import (
    DeviceInfoFactory,
    DummyProblemLocator,
    DummyXblockResult,
    ErrorInfoFactory,
    LabFactory,
    UserFactory,
    UserSaveFactory,
    UserAttemptFactory,
    create_lab_proxy,
)


def get_auth_header(user):
    token, _ = Token.objects.get_or_create(user=user)
    return {
        'HTTP_AUTHORIZATION': "Token {}".format(token.key),
    }


class NoGetMixin(object):

    def test_get_not_allowed(self):
        response = self.client.get(self.url, **self.headers)
        self.assertEqual(response.status_code, 405)


class AuthPostOnlyMixin(object):

    def test_post_not_authentication(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)


class CreateErrorInfoTest(NoGetMixin, AuthPostOnlyMixin, TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.user = UserFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)
        self.url = reverse('labster-api-v2:error-info', args=[self.lab_proxy.location])

        self.headers = get_auth_header(self.user)

    def test_post_created(self):
        post_data = {
            'browser': 'Firefox',
            'os': 'Windows',
            'user_agent': 'user agent',
            'message': 'this is message',
        }
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 201)

        error_infos = ErrorInfo.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertTrue(error_infos.exists())

        error_info = error_infos[0]
        for key, value in post_data.items():
            self.assertEqual(getattr(error_info, key), value)

    def test_post_created_empty_data(self):
        post_data = {
            'browser': '',
            'os': '',
            'user_agent': '',
            'message': '',
        }

        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 201)

        error_infos = ErrorInfo.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertTrue(error_infos.exists())

        error_info = error_infos[0]
        for key, value in post_data.items():
            self.assertEqual(getattr(error_info, key), value)

    def test_post_created_without_initial_lab_proxy(self):
        self.url = reverse('labster-api-v2:error-info', args=['somerandomtext'])
        post_data = {
            'browser': 'Firefox',
            'os': 'Windows',
            'user_agent': 'user agent',
            'message': 'this is message',
        }
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 201)

        error_infos = ErrorInfo.objects.filter(user=self.user, lab_proxy__location='somerandomtext')
        self.assertTrue(error_infos.exists())

        error_info = error_infos[0]
        for key, value in post_data.items():
            self.assertEqual(getattr(error_info, key), value)

