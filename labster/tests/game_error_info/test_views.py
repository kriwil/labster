import json
import unittest

from django.test.client import RequestFactory

from labster.game_error_info.views import log_error
from labster.tests.factories import UserFactory, LabFactory, LabProxyFactory,\
    TokenFactory


class LogErrorTest(unittest.TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.lab_proxy = LabProxyFactory(lab=self.lab)
        self.user = UserFactory(is_superuser=True)
        self.factory = RequestFactory()
        self.token = TokenFactory()

    def test_get(self):
        request = self.factory.get('/', HTTP_AUTHORIZATION=self.token.for_header)
        request.user = self.user
        request.GET = {'user_id': self.user.id}
        response = log_error(request, lab_proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 405)

    def test_post(self):
        post_data = {
            'browser': "browser",
            'os': "os",
            'message': "message",
        }
        request = self.factory.post('/', data=post_data, HTTP_AUTHORIZATION=self.token.for_header)
        request.user = self.user
        request.GET = {'user_id': self.user.id}
        response = log_error(request, lab_proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 201)

        content_type = response.get('Content-Type')
        self.assertEqual(content_type, "application/json")

        content = json.loads(response.content)
        self.assertTrue(content['success'])

    def test_post_invalid(self):
        post_data = {}
        request = self.factory.post('/', data=post_data, HTTP_AUTHORIZATION=self.token.for_header)
        request.user = self.user
        request.GET = {'user_id': self.user.id}
        response = log_error(request, lab_proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 400)

        content_type = response.get('Content-Type')
        self.assertEqual(content_type, "application/json")

        content = json.loads(response.content)
        self.assertFalse(content['success'])
