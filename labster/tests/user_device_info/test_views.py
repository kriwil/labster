import json
import unittest

from django.test.client import RequestFactory

from labster.user_device_info.views import log_device
from labster.tests.factories import UserFactory, LabFactory, LabProxyFactory


class LogDeviceTest(unittest.TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.lab_proxy = LabProxyFactory(lab=self.lab)
        self.user = UserFactory(is_superuser=True)
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get('/', data={'user_id': self.user.id})
        response = log_device(request, lab_proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 405)

    def test_post(self):
        post_data = {
            'device_id': "device_id",
            'frame_rate': "frame_rate",
            'type': "type",
            'os': "os",
            'ram': "ram",
            'processor': "processor",
            'cores': "cores",
            'gpu': "gpu",
            'memory': "memory",
            'fill_rate': "fill_rate",
            'shader_level': "shader_level",
            'quality': "quality",
            'misc': "misc",
        }
        request = self.factory.post('/', data=post_data)
        request.GET = {'user_id': self.user.id}
        response = log_device(request, lab_proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 201)

        content_type = response.get('Content-Type')
        self.assertEqual(content_type, "application/json")

        content = json.loads(response.content)
        self.assertTrue(content['success'])

    def test_post_invalid(self):
        post_data = {}
        request = self.factory.post('/', data=post_data)
        request.GET = {'user_id': self.user.id}
        response = log_device(request, lab_proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 400)

        content_type = response.get('Content-Type')
        self.assertEqual(content_type, "application/json")

        content = json.loads(response.content)
        self.assertFalse(content['success'])
