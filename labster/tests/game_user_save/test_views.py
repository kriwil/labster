import json
import unittest

from django.test.client import RequestFactory

from labster.game_user_save.views import save_detail
from labster.models import UserSave
from labster.tests.factories import UserFactory, LabFactory, LabProxyFactory


class SaveDetailTest(unittest.TestCase):

    def setUp(self):
        self.lab = LabFactory()
        self.lab_proxy = LabProxyFactory(lab=self.lab)
        self.user = UserFactory(is_superuser=True)
        self.factory = RequestFactory()

    def test_get_user_save_exists(self):
        UserSave.objects.create(
            user=self.user, lab_proxy=self.lab_proxy)

        request = self.factory.get('/')
        request.GET = {'user_id': self.user.id}
        response = save_detail(request, lab_proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 200)

        content_type = response.get('Content-Type')
        self.assertEqual(content_type, "text/xml")

    def test_get_user_save_does_not_exist(self):
        request = self.factory.get('/')
        request.GET = {'user_id': self.user.id}
        response = save_detail(request, lab_proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 404)

    def test_post_user_save_exists(self):
        UserSave.objects.create(
            user=self.user, lab_proxy=self.lab_proxy)

        request = self.factory.post('/')
        request.GET = {'user_id': self.user.id}
        response = save_detail(request, lab_proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 200)

        content_type = response.get('Content-Type')
        self.assertEqual(content_type, "application/json")

        content = json.loads(response.content)
        self.assertTrue(content['success'])

    def test_post_user_save_does_not_exist(self):
        request = self.factory.post('/')
        request.GET = {'user_id': self.user.id}
        response = save_detail(request, lab_proxy_id=self.lab_proxy.id)
        self.assertEqual(response.status_code, 200)

        content_type = response.get('Content-Type')
        self.assertEqual(content_type, "application/json")

        content = json.loads(response.content)
        self.assertTrue(content['success'])

        queryset = UserSave.objects.filter(
            user=self.user, lab_proxy=self.lab_proxy)
        self.assertTrue(queryset.exists())
