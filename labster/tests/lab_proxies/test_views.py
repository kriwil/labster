import json
import mock
import unittest

from django.test.client import RequestFactory

from labster.lab_proxies.views import lab_proxy_detail
from labster.tests.factories import UserFactory, LabFactory, LabProxyFactory


class DummyLocation:

    def dict(self):
        return {
            'tag': "tag",
            'org': "org",
            'course': "course",
            'category': "category",
            'name': "name",
        }

    def url(self):
        return ""


class DummyModule:
    data = ""
    location = DummyLocation()


class DummyXBlockResult:
    content = json.dumps({'success': "correct"})


class DummyLabProxyData:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_problemset(self):
        return {}

    def get_problem_by_id(self, problem_id):
        return DummyModule()


class LabProxyDetailTest(unittest.TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.lab_proxy = LabProxyFactory(lab=self.lab)
        self.user = UserFactory(is_superuser=True)

    @mock.patch('labster.lab_proxies.LabProxyData')
    def test_get(self, mock_lab_proxy_data):
        request = RequestFactory().get('/')

        DummyLabProxyData(
            lab_proxy=self.lab_proxy, request=request)

        response = lab_proxy_detail(request, proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 200)

    @mock.patch('labster.lab_proxies.views.invoke_xblock_handler')
    @mock.patch('labster.lab_proxies.views.LabProxyData')
    def test_post(self, mock_lab_proxy_data, invoke_xblock_handler):
        request = RequestFactory().post('/')

        mock_lab_proxy_data.return_value.get_problem_by_id.return_value = DummyModule()
        mock_lab_proxy_data = DummyLabProxyData(
            lab_proxy=self.lab_proxy, request=request)

        invoke_xblock_handler.return_value = DummyXBlockResult()

        response = lab_proxy_detail(request, proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 200)
