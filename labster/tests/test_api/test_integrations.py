import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from rest_framework.authtoken.models import Token

from labster.api.views import AnswerProblem
from labster.models import ErrorInfo, DeviceInfo, UserSave, UserAttempt
from labster.tests.factories import (
    DummyProblemLocator,
    DummyXblockResult,
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


class CreateErrorTest(NoGetMixin, AuthPostOnlyMixin, TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.user = UserFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)
        self.url = reverse('labster-api:log-error', args=[self.lab_proxy.id])

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


class CreateDeviceTest(NoGetMixin, AuthPostOnlyMixin, TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.user = UserFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)
        self.url = reverse('labster-api:log-device', args=[self.lab_proxy.id])

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


class CreateSaveTest(AuthGetOnlyMixin, AuthPostOnlyMixin, TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.user = UserFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)
        self.user_save_file = SimpleUploadedFile("file.txt", "this is the content")

        self.url = reverse('labster-api:save', args=[self.lab_proxy.id])
        self.headers = get_auth_header(self.user)

    def test_get_found(self):
        UserSaveFactory(user=self.user, lab_proxy=self.lab_proxy,
                        save_file=self.user_save_file)
        response = self.client.get(self.url, **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_post_new(self):
        post_data = {
            'file': self.user_save_file,
        }

        # whenever we post another user save, it will replace the old data
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 200)

        user_saves = UserSave.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertEqual(user_saves.count(), 1)

    def test_post_exists(self):
        user_save = UserSaveFactory(
            user=self.user, lab_proxy=self.lab_proxy,
            save_file=self.user_save_file)

        post_data = {
            'file': self.user_save_file,
        }

        # whenever we post another user save, it will replace the old data
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 200)

        user_saves = UserSave.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertEqual(user_saves.count(), 1)

        self.assertEqual(user_saves[0].id, user_save.id)


class PlayLabTest(AuthGetOnlyMixin, AuthPostOnlyMixin, TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.user = UserFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)

        self.url = reverse('labster-api:play-lab', args=[self.lab_proxy.id])
        self.headers = get_auth_header(self.user)

    def test_get_found(self):
        UserAttemptFactory(user=self.user, lab_proxy=self.lab_proxy)
        response = self.client.get(self.url, **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_post_invalid(self):
        post_data = {}
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_post_created(self):
        post_data = {
            'play': 1,
        }
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 201)

        user_attempts = UserAttempt.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertEqual(user_attempts.count(), 1)

        user_attempt = user_attempts[0]
        self.assertEqual(user_attempt.get_total_play_count(), 1)
        self.assertFalse(user_attempt.is_finished)

    def test_post_exists_not_finished(self):
        UserAttemptFactory(user=self.user, lab_proxy=self.lab_proxy)
        post_data = {
            'play': 1,
        }
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 201)

        user_attempts = UserAttempt.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertEqual(user_attempts.count(), 2)


class FinishLabTest(AuthGetOnlyMixin, AuthPostOnlyMixin, TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.user = UserFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)

        self.url = reverse('labster-api:finish-lab', args=[self.lab_proxy.id])
        self.headers = get_auth_header(self.user)

    def test_get_found(self):
        UserAttemptFactory(user=self.user, lab_proxy=self.lab_proxy)
        response = self.client.get(self.url, **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_post_not_found(self):
        post_data = {}
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 404)

    def test_post_invalid(self):
        UserAttemptFactory(user=self.user, lab_proxy=self.lab_proxy, is_finished=False)

        post_data = {}
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_post_exists(self):
        user_attempt = UserAttemptFactory(user=self.user, lab_proxy=self.lab_proxy, is_finished=False)
        post_data = {
            'is_finished': True,
        }
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 204)

        user_attempts = UserAttempt.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertEqual(user_attempts.count(), 1)

        self.assertEqual(user_attempts[0].id, user_attempt.id)
        self.assertEqual(user_attempts[0].is_finished, True)


class UnityPlayLabTest(NoGetMixin, AuthPostOnlyMixin, TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.user = UserFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)

        self.url = reverse('labster-api:play', args=[self.lab_proxy.id])
        self.headers = get_auth_header(self.user)

    def test_post_invalid(self):
        post_data = {}
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 400)

    def test_post_start_created(self):
        post_data = {
            'StartEndType': '1',
        }
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 204)

        user_attempts = UserAttempt.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertEqual(user_attempts.count(), 1)

        user_attempt = user_attempts[0]
        self.assertEqual(user_attempt.get_total_play_count(), 1)
        self.assertFalse(user_attempt.is_finished)

    def test_post_exists_not_finished(self):
        UserAttemptFactory(user=self.user, lab_proxy=self.lab_proxy)
        post_data = {
            'StartEndType': '1',
        }
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 204)

        user_attempts = UserAttempt.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertEqual(user_attempts.count(), 2)

    def test_post_finished(self):
        UserAttemptFactory(user=self.user, lab_proxy=self.lab_proxy)
        post_data = {
            'StartEndType': '2',
        }
        response = self.client.post(self.url, post_data, **self.headers)
        self.assertEqual(response.status_code, 204)

        user_attempts = UserAttempt.objects.filter(user=self.user, lab_proxy=self.lab_proxy)
        self.assertEqual(user_attempts.count(), 1)

        user_attempt = user_attempts[0]
        self.assertEqual(user_attempt.get_total_play_count(), 1)
        self.assertTrue(user_attempt.is_finished)


class AnswerProblemTest(TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.user = UserFactory()
        self.lab_proxy = create_lab_proxy(lab=self.lab)

        self.url = reverse('labster-api:answer-problem', args=[self.lab_proxy.id])
        self.headers = get_auth_header(self.user)

    @mock.patch('labster.api.views.get_usage_key')
    @mock.patch('labster.api.views.get_modulestore')
    @mock.patch('labster.api.views.invoke_xblock_handler')
    def test_post(self, invoke_xblock_handler, modulestore, usage_key):
        invoke_xblock_handler.return_value = DummyXblockResult()

        response = self.client.post(self.url, **self.headers)
        self.assertEqual(response.status_code, 201)

    @mock.patch('labster.api.views.get_usage_key')
    @mock.patch('labster.api.views.get_modulestore')
    @mock.patch('labster.api.views.invoke_xblock_handler')
    def test_get_post_data(self, invoke_xblock_handler, modulestore, usage_key):
        request = RequestFactory().request()
        problem_locator = DummyProblemLocator()
        answer = "1"
        time_spent = "10.13"
        post_data = AnswerProblem().get_post_data(request, problem_locator, answer, time_spent)
        self.assertIn('input_tag-org-course-category-name_2_1', post_data)
        self.assertEqual(post_data.get('input_tag-org-course-category-name_2_1'), '1')
        self.assertEqual(post_data.get('time_spent'), time_spent)
