import mock
import os.path
import unittest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory, force_authenticate

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

        request = self.factory.get(self.url)
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location=self.lab_proxy.location)
        response.render()

        self.assertEqual(response.status_code, 405)

    def test_post_created(self):
        post_data = {
            'browser': 'Firefox',
            'os': 'Windows',
            'user_agent': 'user agent',
            'message': 'this is message',
        }
        request = self.factory.post(self.url, post_data)
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location=self.lab_proxy.location)
        response.render()

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            ErrorInfo.objects.filter(user=self.user, lab_proxy=self.lab_proxy).exists())

    def test_post_created_missing_data(self):
        post_data = {
            'browser': '',
            'os': '',
            'user_agent': '',
            'message': '',
        }
        request = self.factory.post(self.url, post_data)
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location=self.lab_proxy.location)
        response.render()

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            ErrorInfo.objects.filter(user=self.user, lab_proxy=self.lab_proxy).exists())

    def test_post_created_without_inital_lab_proxy(self):
        self.url = reverse('labster-api-v2:error-info', args=['somerandomtext'])

        post_data = {
            'browser': 'Firefox',
            'os': 'Windows',
            'user_agent': 'user agent',
            'message': 'this is message',
        }
        request = self.factory.post(self.url, post_data)
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location='somerandomtext')
        response.render()

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            ErrorInfo.objects.filter(user=self.user, lab_proxy__location='somerandomtext').exists())


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

        request = self.factory.get(self.url)
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location=self.lab_proxy.location)
        response.render()

        self.assertEqual(response.status_code, 405)

    def test_post_created(self):
        DeviceInfoFactory(user=self.user, lab_proxy=self.lab_proxy)

        post_data = {
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
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location=self.lab_proxy.location)
        response.render()

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            DeviceInfo.objects.filter(user=self.user, lab_proxy=self.lab_proxy).exists())

    def test_post_created_empty_data(self):
        DeviceInfoFactory(user=self.user, lab_proxy=self.lab_proxy)

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
        request = self.factory.post(self.url, post_data)
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location=self.lab_proxy.location)
        response.render()

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            DeviceInfo.objects.filter(user=self.user, lab_proxy=self.lab_proxy).exists())

    def test_post_created_without_intial_lab_proxy(self):
        self.url = reverse('labster-api-v2:device-info', args=['somerandomtext'])
        DeviceInfoFactory(user=self.user, lab_proxy=self.lab_proxy)

        post_data = {
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
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location='somerandomtext')
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
        self.user_save_file = SimpleUploadedFile("file.txt", "this is the content")
        self.url = reverse('labster-api-v2:user-save', args=[self.lab_proxy.location])

    def test_get_not_found(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location=self.lab_proxy.location)
        response.render()

        self.assertEqual(response.status_code, 404)

    def test_get_found(self):
        UserSaveFactory(user=self.user, lab_proxy=self.lab_proxy, save_file=self.user_save_file)

        request = self.factory.get(self.url)
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location=self.lab_proxy.location)
        response.render()

        self.assertEqual(response.status_code, 200)

    def test_post_invalid(self):
        post_data = {}
        request = self.factory.post(self.url, post_data)
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location=self.lab_proxy.location)
        response.render()

        self.assertEqual(response.status_code, 400)

    def test_post_created(self):
        post_data = {
            'save_file': self.user_save_file,
        }
        request = self.factory.post(self.url, post_data, format='multipart')
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location=self.lab_proxy.location)
        response.render()

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            UserSave.objects.filter(user=self.user, lab_proxy=self.lab_proxy).exists())

    def test_post_created_without_initial_lab_proxy(self):
        self.url = reverse('labster-api-v2:user-save', args=['somerandomtext'])
        post_data = {
            'save_file': self.user_save_file,
        }
        request = self.factory.post(self.url, post_data, format='multipart')
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location=self.lab_proxy.location)
        response.render()

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            UserSave.objects.filter(user=self.user, lab_proxy=self.lab_proxy).exists())

    def test_post_exists(self):
        x = UserSaveFactory(user=self.user, lab_proxy=self.lab_proxy, save_file=self.user_save_file)

        post_data = {
            'save_file': self.user_save_file,
        }
        request = self.factory.post(self.url, post_data, format='multipart')
        force_authenticate(request, user=UserFactory())
        response = self.view(request, location=self.lab_proxy.location)
        response.render()

        # whenever we post another user save, it will replace the old data
        self.assertEqual(response.status_code, 204)

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
        force_authenticate(request, user=UserFactory())
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 201)

    @mock.patch('labster.api.views.get_usage_key')
    @mock.patch('labster.api.views.get_modulestore')
    @mock.patch('labster.api.views.invoke_xblock_handler')
    def test_get_post_data(self, invoke_xblock_handler, modulestore, usage_key):
        request = self.factory.post(self.url)
        force_authenticate(request, user=UserFactory())
        problem_locator = DummyProblemLocator()
        answer = "1"
        AnswerProblem().get_post_data(request, problem_locator, answer)
