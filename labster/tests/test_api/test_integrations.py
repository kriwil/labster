from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase

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


class AuthGetOnlyMixin(object):

    def test_get_not_found(self):
        response = self.client.get(self.url, **self.headers)
        self.assertEqual(response.status_code, 404)

    def test_get_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)


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


class CreateDeviceInfoTest(NoGetMixin, AuthPostOnlyMixin, TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.user = UserFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)
        self.url = reverse('labster-api-v2:device-info', args=[self.lab_proxy.location])

        self.headers = get_auth_header(self.user)

    def test_post_created(self):
        post_data = {
            'cores': 'quad core',
            'device_id': 'this is devicei id',
            'fill_rate': '45',
            'frame_rate': '60FPS',
            'gpu': 'NVidia',
            'machine_type': 'Intel',
            'memory': '64GB',
            'misc': 'this is misc',
            'os': 'Windows',
            'processor': 'intel dual core',
            'quality': 'best',
            'ram': '1GB',
            'shader_level': 'top',
        }

        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 201)

        device_infos = DeviceInfo.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertTrue(device_infos.exists())

        device_info = device_infos[0]
        for key, value in post_data.items():
            self.assertEqual(getattr(device_info, key), value)

    def test_post_empty_data(self):

        post_data = {
            'cores': '',
            'device_id': '',
            'fill_rate': '',
            'frame_rate': '',
            'gpu': '',
            'machine_type': '',
            'memory': '',
            'misc': '',
            'os': '',
            'processor': '',
            'quality': '',
            'ram': '',
            'shader_level': '',
        }

        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 201)

        device_infos = DeviceInfo.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertTrue(device_infos.exists())

        device_info = device_infos[0]
        for key, value in post_data.items():
            self.assertEqual(getattr(device_info, key), value)

    def test_post_created_without_initial_lab_proxy(self):
        self.url = reverse('labster-api-v2:device-info', args=['somerandomtext'])
        post_data = {
            'cores': 'quad core',
            'device_id': 'this is devicei id',
            'fill_rate': '45',
            'frame_rate': '60FPS',
            'gpu': 'NVidia',
            'machine_type': 'Intel',
            'memory': '64GB',
            'misc': 'this is misc',
            'os': 'Windows',
            'processor': 'intel dual core',
            'quality': 'best',
            'ram': '1GB',
            'shader_level': 'top',
        }
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 201)

        device_infos = DeviceInfo.objects.filter(user=self.user, lab_proxy__location='somerandomtext')
        self.assertTrue(device_infos.exists())

        device_info = device_infos[0]
        for key, value in post_data.items():
            self.assertEqual(getattr(device_info, key), value)


class CreateUserSaveTest(AuthGetOnlyMixin, AuthPostOnlyMixin, TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.user = UserFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)
        self.user_save_file = SimpleUploadedFile("file.txt", "this is the content")

        self.url = reverse('labster-api-v2:user-save', args=[self.lab_proxy.location])
        self.headers = get_auth_header(self.user)

    def test_get_found(self):
        UserSaveFactory(user=self.user, lab_proxy=self.lab_proxy,
                        save_file=self.user_save_file)
        response = self.client.get(self.url, **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_post_created_without_initial_lab_proxy(self):
        lab_proxy_location = 'somerandomtext'
        self.url = reverse('labster-api-v2:user-save', args=[lab_proxy_location])
        post_data = {
            'save_file': self.user_save_file,
        }
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 201)

        user_saves = UserSave.objects.filter(
            user=self.user, lab_proxy__location=lab_proxy_location)
        self.assertTrue(user_saves.exists())

        user_save = user_saves[0]
        self.assertIsNotNone(user_save.save_file)

    def test_post_exists(self):
        user_save = UserSaveFactory(
            user=self.user, lab_proxy=self.lab_proxy,
            save_file=self.user_save_file)

        post_data = {
            'save_file': self.user_save_file,
        }

        # whenever we post another user save, it will replace the old data
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 204)

        user_saves = UserSave.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertEqual(user_saves.count(), 1)

        self.assertEqual(user_saves[0].id, user_save.id)
