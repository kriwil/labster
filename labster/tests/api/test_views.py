import json
import unittest

from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory

from labster.api.views import LabList, LabDetail
from labster.models import Lab
from labster.tests.factories import LabFactory


class LabListTest(unittest.TestCase):

    def setUp(self):
        self.view = LabList.as_view()
        self.factory = APIRequestFactory()
        self.lab = LabFactory()
        self.url = reverse('labster-api-v2:lab-list')

    def test_get(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        response.render()

        # HTTP 200
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)

        # all labs are returned
        labs = Lab.objects.all()
        self.assertEqual(len(content), labs.count())

    def test_post(self):
        request = self.factory.post(self.url)
        response = self.view(request)
        response.render()

        # HTTP 405
        self.assertEqual(response.status_code, 405)


class LabDetailTest(unittest.TestCase):

    def setUp(self):
        self.view = LabDetail.as_view()
        self.factory = APIRequestFactory()
        self.lab = LabFactory()
        self.url = reverse('labster-api-v2:lab-detail', kwargs={'pk': self.lab.id})

    def test_get(self):
        request = self.factory.get(self.url)
        response = self.view(request, pk=self.lab.id)
        response.render()

        # HTTP 200
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        request = self.factory.post(self.url)
        response = self.view(request)
        response.render()

        # HTTP 405
        self.assertEqual(response.status_code, 405)
