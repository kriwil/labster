import json
import unittest
import urllib

from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory

from labster.api.views import LabList, LabDetail
from labster.api.views import QuizBlockList, QuizBlockDetail
from labster.api.views import ProblemList, ProblemDetail
from labster.api.views import LabProxyList, LabProxyDetail
from labster.api.views import CreateUserProblem, CreateUserLabProxy
from labster.models import Lab, QuizBlock, Problem, LabProxy, UserProblem,\
    UserLabProxy
from labster.tests.factories import UserFactory, LabFactory, QuizBlockFactory,\
    ProblemFactory, LabProxyFactory, UserLabProxyFactory


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


class LabProxyListTest(unittest.TestCase):

    def setUp(self):
        self.view = LabProxyList.as_view()
        self.factory = APIRequestFactory()
        self.lab = LabFactory()
        self.lab_proxy = LabProxyFactory(lab=self.lab)
        self.url = reverse('labster-api-v2:lab-proxy-list')

    def test_get(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        response.render()

        # HTTP 200
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)

        problems = LabProxy.objects.all()
        self.assertEqual(len(content), problems.count())

    def test_post_invalid(self):
        request = self.factory.post(self.url)
        response = self.view(request)
        response.render()

        # HTTP 400
        self.assertEqual(response.status_code, 400)

    def test_post_valid(self):
        post_data = {
            'lab': self.lab.id,
            'location_id': "location_id",
        }
        request = self.factory.post(self.url, post_data)
        response = self.view(request)
        response.render()

        # HTTP 201
        self.assertEqual(response.status_code, 201)


class LabProxyDetailTest(unittest.TestCase):

    def setUp(self):
        self.view = LabProxyDetail.as_view()
        self.factory = APIRequestFactory()
        self.lab = LabFactory()
        self.lab_proxy = LabProxyFactory(lab=self.lab)
        self.url = reverse('labster-api-v2:lab-proxy-detail', kwargs={'pk': self.lab_proxy.id})

    def test_get(self):
        request = self.factory.get(self.url)
        response = self.view(request, pk=self.lab_proxy.id)
        response.render()

        # HTTP 200
        self.assertEqual(response.status_code, 200)


class CreateUserProblemTest(unittest.TestCase):

    def setUp(self):
        self.view = CreateUserProblem.as_view()
        self.factory = APIRequestFactory()
        self.url = reverse('labster-api-v2:user-problem')
        self.lab = LabFactory()
        self.lab_proxy = LabProxyFactory(lab=self.lab)
        self.quiz_block = QuizBlockFactory(lab=self.lab, lab_proxy=self.lab_proxy)
        self.problem = ProblemFactory(quiz_block=self.quiz_block)
        self.user = UserFactory()

    def test_get(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 405)

    def test_post(self):
        post_data = {
            'user': self.user.id,
            'problem': self.problem.id,
        }
        request = self.factory.post(self.url, post_data)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            UserProblem.objects.filter(user=self.user, problem=self.problem).exists())


class CreateUserLabProxyTest(unittest.TestCase):

    def setUp(self):
        self.view = CreateUserLabProxy.as_view()
        self.factory = APIRequestFactory()
        self.url = reverse('labster-api-v2:user-lab-proxy')
        self.lab = LabFactory()
        self.lab_proxy = LabProxyFactory(lab=self.lab)
        self.quiz_block = QuizBlockFactory(lab=self.lab, lab_proxy=self.lab_proxy)
        self.problem = ProblemFactory(quiz_block=self.quiz_block)
        self.user = UserFactory()

    def test_get_not_found(self):
        url_params = {'user': self.user.id, 'lab_proxy': self.lab_proxy.id}
        self.url = "{}?{}".format(
            self.url, urllib.urlencode(url_params))
        request = self.factory.get(self.url)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 404)

    def test_get_found(self):
        UserLabProxyFactory(user=self.user, lab_proxy=self.lab_proxy)

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
        }
        request = self.factory.post(self.url, post_data)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 201)

        self.assertTrue(
            UserLabProxy.objects.filter(user=self.user, lab_proxy=self.lab_proxy).exists())

    def test_post_exists(self):
        UserLabProxyFactory(user=self.user, lab_proxy=self.lab_proxy)

        post_data = {
            'user': self.user.id,
            'lab_proxy': self.lab_proxy.id,
        }
        request = self.factory.post(self.url, post_data)
        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, 204)

        self.assertTrue(
            UserLabProxy.objects.filter(user=self.user, lab_proxy=self.lab_proxy).exists())

        self.assertEqual(
            UserLabProxy.objects.filter(user=self.user, lab_proxy=self.lab_proxy).count(), 1)
