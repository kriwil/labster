import json
import unittest

from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory

from labster.api.views import LabList, LabDetail
from labster.api.views import QuizBlockList, QuizBlockDetail
from labster.api.views import ProblemList, ProblemDetail
from labster.models import Lab, QuizBlock, Problem
from labster.tests.factories import LabFactory, QuizBlockFactory, ProblemFactory


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


class QuizBlockListTest(unittest.TestCase):

    def setUp(self):
        self.view = QuizBlockList.as_view()
        self.factory = APIRequestFactory()
        self.quiz_block = QuizBlockFactory(lab=LabFactory())
        self.url = reverse('labster-api-v2:quiz-block-list')

    def test_get(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        response.render()

        # HTTP 200
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)

        quiz_blocks = QuizBlock.objects.all()
        self.assertEqual(len(content), quiz_blocks.count())

    def test_post(self):
        request = self.factory.post(self.url)
        response = self.view(request)
        response.render()

        # HTTP 405
        self.assertEqual(response.status_code, 405)


class QuizBlockDetailTest(unittest.TestCase):

    def setUp(self):
        self.view = QuizBlockDetail.as_view()
        self.factory = APIRequestFactory()
        self.quiz_block = QuizBlockFactory(lab=LabFactory())
        self.url = reverse('labster-api-v2:quiz-block-detail', kwargs={'pk': self.quiz_block.id})

    def test_get(self):
        request = self.factory.get(self.url)
        response = self.view(request, pk=self.quiz_block.id)
        response.render()

        # HTTP 200
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        request = self.factory.post(self.url)
        response = self.view(request)
        response.render()

        # HTTP 405
        self.assertEqual(response.status_code, 405)


class ProblemListTest(unittest.TestCase):

    def setUp(self):
        self.view = ProblemList.as_view()
        self.factory = APIRequestFactory()
        self.quiz_block = QuizBlockFactory(lab=LabFactory())
        self.problem = ProblemFactory(quiz_block=self.quiz_block)
        self.url = reverse('labster-api-v2:problem-list')

    def test_get(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        response.render()

        # HTTP 200
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)

        problems = Problem.objects.all()
        self.assertEqual(len(content), problems.count())

    def test_post_invalid(self):
        request = self.factory.post(self.url)
        response = self.view(request)
        response.render()

        # HTTP 400
        self.assertEqual(response.status_code, 400)

    def test_post_valid(self):
        post_data = {
            'quiz_block': self.quiz_block.id,
            'content_markdown': "test",
        }
        request = self.factory.post(self.url, post_data)
        response = self.view(request)
        response.render()

        # HTTP 201
        self.assertEqual(response.status_code, 201)


class ProblemDetailTest(unittest.TestCase):

    def setUp(self):
        self.view = ProblemDetail.as_view()
        self.factory = APIRequestFactory()
        self.quiz_block = QuizBlockFactory(lab=LabFactory())
        self.problem = ProblemFactory(quiz_block=self.quiz_block)
        self.url = reverse('labster-api-v2:problem-detail', kwargs={'pk': self.problem.id})

    def test_get(self):
        request = self.factory.get(self.url)
        response = self.view(request, pk=self.problem.id)
        response.render()

        # HTTP 200
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        request = self.factory.post(self.url)
        response = self.view(request)
        response.render()

        # HTTP 405
        self.assertEqual(response.status_code, 405)

    def test_put(self):
        put_data = {
            'quiz_block': self.quiz_block.id,
            'content_markdown': "test",
        }
        request = self.factory.put(self.url, put_data)
        response = self.view(request, pk=self.problem.id)
        response.render()

        # HTTP 200
        self.assertEqual(response.status_code, 200)

        problem = Problem.objects.get(id=self.problem.id)
        self.assertEqual(problem.content_markdown, put_data['content_markdown'])

    def test_delete(self):
        request = self.factory.delete(self.url)
        response = self.view(request, pk=self.problem.id)
        response.render()

        # HTTP 204
        self.assertEqual(response.status_code, 204)

        self.assertFalse(
            Problem.objects.filter(id=self.problem.id).exists())
