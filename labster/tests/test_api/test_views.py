import mock
import os.path
import tempfile
import unittest
import urllib

from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory

from labster.api.views import CreateErrorInfo, CreateDeviceInfo, CreateUserSave, AnswerProblem
from labster.models import ErrorInfo, DeviceInfo, UserSave
from labster.tests.factories import (
    DeviceInfoFactory,
    DummyProblemLocator,
    DummyXblockResult,
    ErrorInfoFactory,
    LabFactory,
    UserFactory,
    UserSaveFactory,
    create_lab_proxy,
)


class CreateErrorInfoTest(unittest.TestCase):

    def setUp(self):
        self.view = CreateErrorInfo.as_view()
        self.factory = APIRequestFactory()
        self.lab = LabFactory()
        self.user = UserFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)
        self.url = reverse('labster-api-v2:error-info', args=[self.lab_proxy.location])

    def test_get_not_allowed(self):
        # get method is not allowed in ErrorInfoFactory
        ErrorInfoFactory(user=self.user, lab_proxy=self.lab_proxy)

        url_params = {'user': self.user.id, 'lab_proxy': self.lab_proxy.id}
        self.url = "{}?{}".format(
            self.url, urllib.urlencode(url_params))
        request = self.factory.get(self.url)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 405)

    def test_post_invalid(self):
        post_data = {}
        request = self.factory.post(self.url, post_data)
        response = self.view(request)
        response.render()

        # all required fields are empty so it returns 400
        self.assertEqual(response.status_code, 400)

    def test_post_created(self):
        post_data = {
            'user': self.user.id,
            'lab_proxy': self.lab_proxy.id,
            'browser': 'Firefox',
            'os': 'Windows',
            'user_agent': 'user agent',
            'message': 'this is message',
        }
        request = self.factory.post(self.url, post_data)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            ErrorInfo.objects.filter(user=self.user, lab_proxy=self.lab_proxy).exists())


class CreateDeviceInfoTest(unittest.TestCase):

    def setUp(self):
        self.view = CreateDeviceInfo.as_view()
        self.factory = APIRequestFactory()
        self.lab = LabFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)
        self.user = UserFactory()
        self.url = reverse('labster-api-v2:device-info', args=[self.lab_proxy.location])

    def test_get_not_allowed(self):
        # get method is not allowed in ErrorInfoFactory
        DeviceInfoFactory(user=self.user, lab_proxy=self.lab_proxy)

        url_params = {'user': self.user.id, 'lab_proxy': self.lab_proxy.id}
        self.url = "{}?{}".format(
            self.url, urllib.urlencode(url_params))
        request = self.factory.get(self.url)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 405)

    def test_post_invalid(self):
        post_data = {}
        request = self.factory.post(self.url, post_data)
        response = self.view(request)
        response.render()

        # all required fields are empty so it returns 400
        self.assertEqual(response.status_code, 400)

    def test_post_created(self):
        DeviceInfoFactory(user=self.user, lab_proxy=self.lab_proxy)

        post_data = {
            'user': self.user.id,
            'lab_proxy': self.lab_proxy.id,
            'device_id': 'this is devicei id',
            'os': 'Windows',
            'machine_type': 'Intel',
            'ram': '1GB',
            'processor': 'intel dual core',
            'cores': 'quad core',
            'gpu': 'NVidia',
            'memory': '64GB',
            'fill_rate': '45',
            'shader_level': 'top',
            'quality': 'best',
            'misc': 'this is misc',
            'frame_rate': '60FPS',
        }
        request = self.factory.post(self.url, post_data)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            DeviceInfo.objects.filter(user=self.user, lab_proxy=self.lab_proxy).exists())


class CreateUserSaveTest(unittest.TestCase):

    def setUp(self):
        self.view = CreateUserSave.as_view()
        self.factory = APIRequestFactory()
        self.lab = LabFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)
        self.user = UserFactory()
        self.temp_file_path = os.path.join(tempfile.gettempdir(), "temp-testfile")
        self.url = reverse('labster-api-v2:user-save', args=[self.lab_proxy.location])

    def test_get_not_found(self):
        url_params = {'user': self.user.id, 'lab_proxy': self.lab_proxy.id}
        self.url = "{}?{}".format(
            self.url, urllib.urlencode(url_params))
        request = self.factory.get(self.url)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 404)

    def test_get_found(self):
        UserSaveFactory(user=self.user, lab_proxy=self.lab_proxy, save_file=self.temp_file_path)

        url_params = {'user': self.user.id, 'lab_proxy': self.lab_proxy.id}
        self.url = "{}?{}".format(
            self.url, urllib.urlencode(url_params))
        request = self.factory.get(self.url)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 200)

    def test_post_invalid(self):
        post_data = {}
        request = self.factory.post(self.url, post_data)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 404)

    def test_post_created(self):
        post_data = {
            'user': self.user.id,
            'lab_proxy': self.lab_proxy.id,
            'save_file': self.temp_file_path,
        }
        request = self.factory.post(self.url, post_data)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            UserSave.objects.filter(user=self.user, lab_proxy=self.lab_proxy).exists())

    def test_post_exists(self):
        UserSaveFactory(user=self.user, lab_proxy=self.lab_proxy, save_file=self.temp_file_path)

        post_data = {
            'user': self.user.id,
            'lab_proxy': self.lab_proxy.id,
            'save_file': self.temp_file_path,
        }
        request = self.factory.post(self.url, post_data)
        response = self.view(request)
        response.render()

        # whenever we post another user save, it will replace the old data
        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            UserSave.objects.filter(user=self.user, lab_proxy=self.lab_proxy).exists())

        # this should be 1 because we are replacing the old data with the new one
        self.assertEqual(
            UserSave.objects.filter(user=self.user, lab_proxy=self.lab_proxy).count(), 1)


class AnswerProblemTest(unittest.TestCase):

    def setUp(self):

        self.view = AnswerProblem.as_view()
        self.factory = APIRequestFactory()
        self.lab = LabFactory()
        self.user = UserFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)
        self.url = reverse('labster-api-v2:answer-problem', args=[self.lab_proxy.location])

    @mock.patch('labster.api.views.get_usage_key')
    @mock.patch('labster.api.views.get_modulestore')
    @mock.patch('labster.api.views.invoke_xblock_handler')
    def test_post(self, invoke_xblock_handler, modulestore, usage_key):
        invoke_xblock_handler.return_value = DummyXblockResult()

        request = self.factory.post(self.url)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 201)

    @mock.patch('labster.api.views.get_usage_key')
    @mock.patch('labster.api.views.get_modulestore')
    @mock.patch('labster.api.views.invoke_xblock_handler')
    def test_get_post_data(self, invoke_xblock_handler, modulestore, usage_key):
        request = self.factory.post(self.url)
        problem_locator = DummyProblemLocator()
        answer = "1"
        AnswerProblem().get_post_data(request, problem_locator, answer)
