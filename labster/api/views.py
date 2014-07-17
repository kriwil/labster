import json

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.http import QueryDict
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.parsers import FormParser, XMLParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import XMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from labster.api.serializers import UserSaveSerializer, ErrorInfoSerializer, DeviceInfoSerializer
from labster.authentication import SingleTokenAuthentication
from labster.models import UserSave, ErrorInfo, DeviceInfo, LabProxy, get_or_create_lab_proxy


def invoke_xblock_handler(*args, **kwargs):
    from courseware.module_render import _invoke_xblock_handler

    """
    Wrapper so it could be mocked
    """
    return _invoke_xblock_handler(*args, **kwargs)


def get_usage_key():
    from opaque_keys.edx.keys import UsageKey
    return UsageKey


def get_modulestore():
    from xmodule.modulestore.django import modulestore
    return modulestore


def get_lab_by_location(location):
    UsageKey = get_usage_key()
    modulestore = get_modulestore()

    locator = UsageKey.from_string(location)
    descriptor = modulestore().get_item(locator)
    lab_id = descriptor.lab_id
    lab = {}

    quiz_blocks = []
    for _quiz_block in descriptor.get_children():
        problems = []
        for _problem in _quiz_block.get_children():
            problem = {
                'id': unicode(_problem.location),
                'content': _problem.data,
            }

            problems.append(problem)

        quiz_block = {
            'id': unicode(_quiz_block.location),
            'slug': _quiz_block.display_name,
            'problems': problems,
        }

        quiz_blocks.append(quiz_block)

    lab.update({
        'lab': {
            'id': int(lab_id),
            'quiz_blocks': quiz_blocks,
        }
    })

    return lab


class RendererMixin:
    renderer_classes = (XMLRenderer, JSONRenderer)


class ParserMixin:
    parser_classes = (FormParser, MultiPartParser, XMLParser, JSONParser)


class AuthMixin:
    authentication_classes = (SingleTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class APIRoot(RendererMixin, AuthMixin, APIView):

    def get(self, request, *args, **kwargs):
        format = kwargs.get('format')
        lab_proxy_detail_url = reverse(
            'labster-api-v2:lab-proxy-detail',
            request=request,
            kwargs={'location': 'EDX-COURSE-LOCATION'},
            format=format)

        answer_problem_url = reverse(
            'labster-api-v2:answer-problem',
            request=request,
            kwargs={'location': 'EDX-COURSE-LOCATION'},
            format=format)

        user_save_url = reverse(
            'labster-api-v2:user-save',
            request=request,
            kwargs={'location': 'EDX-COURSE-LOCATION'},
            format=format)

        error_info_url = reverse(
            'labster-api-v2:error-info',
            request=request,
            kwargs={'location': 'EDX-COURSE-LOCATION'},
            format=format)

        device_info_url = reverse(
            'labster-api-v2:device-info',
            request=request,
            kwargs={'location': 'EDX-COURSE-LOCATION'},
            format=format)

        return Response({
            'lab-proxy-detail': lab_proxy_detail_url,
            'answer-problem': answer_problem_url,
            'user-save': user_save_url,
            'error-info': error_info_url,
            'device-info': device_info_url,
        })


class CreateUserSave(RendererMixin, ParserMixin, AuthMixin, ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        location = kwargs.get('location')

        lab_proxy = get_object_or_404(LabProxy, location=location)
        user_save = get_object_or_404(UserSave, lab_proxy_id=lab_proxy.id, user_id=user.id)

        serializer = UserSaveSerializer(user_save)
        return Response(serializer.data)

    def pre_save(self, obj):
        obj.user = self.request.user
        obj.lab_proxy = get_or_create_lab_proxy(location=self.kwargs.get('location'))

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user = request.user
        location = kwargs.get('location')
        lab_proxy = get_or_create_lab_proxy(location=location)

        user = get_object_or_404(User, id=user.id)

        try:
            user_save, new_object = UserSave.objects.get(user=user, lab_proxy=lab_proxy), False
        except ObjectDoesNotExist:
            user_save, new_object = None, True

        serializer = UserSaveSerializer(instance=user_save, data=data, files=request.FILES)
        if serializer.is_valid():
            self.pre_save(serializer.object)
            serializer.save()
            http_status = status.HTTP_201_CREATED if new_object else status.HTTP_204_NO_CONTENT
            return Response(serializer.data, status=http_status)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateErrorInfo(RendererMixin, AuthMixin, CreateAPIView):
    model = ErrorInfo
    serializer_class = ErrorInfoSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
        obj.lab_proxy = get_or_create_lab_proxy(location=self.kwargs.get('location'))


class CreateDeviceInfo(RendererMixin, AuthMixin, CreateAPIView):
    model = DeviceInfo
    serializer_class = DeviceInfoSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
        obj.lab_proxy = get_or_create_lab_proxy(location=self.kwargs.get('location'))


class LabProxyView(RendererMixin, AuthMixin, APIView):

    def get(self, request, format=None, *args, **kwargs):
        response_data = {}
        location = kwargs.get('location')
        if location:
            response_data = get_lab_by_location(location)
        return Response(response_data)


class CourseWiki(RendererMixin, AuthMixin, APIView):

    def get(self, request, course_id, *args, **kwargs):
        from courseware.courses import get_course_by_id
        from course_wiki.utils import course_wiki_slug

        from wiki.models import URLPath, Article

        try:
            course = get_course_by_id(course_id)
        except ValueError:
            raise Http404

        course_slug = course_wiki_slug(course)

        url_path = URLPath.get_by_path(course_slug, select_related=True)

        results = list(Article.objects.filter(id=url_path.article.id))
        if results:
            article = results[0]
        else:
            article = None

        response = {
            'title': course_slug,
            'content': article.get_cached_content(),
        }
        return Response(response)


class CourseWikiArticle(RendererMixin, AuthMixin, APIView):

    renderer_classes = (XMLRenderer,)
    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'

    def get(self, request, article_slug, *args, **kwargs):
        from wiki.models import URLPath, Article

        # since we already have article slug we don't need to search the course
        # article slug is unique
        try:
            url_path = URLPath.get_by_path(article_slug, select_related=True)
        except ObjectDoesNotExist:
            raise Http404

        # list all the articles
        results = list(Article.objects.filter(id=url_path.article.id))

        if results:
            article = results[0]
        else:
            article = None

        response = {
            'title': article_slug,
            'content': article.get_cached_content(),
        }
        return Response(response)


class AnswerProblem(RendererMixin, AuthMixin, APIView):

    def __init__(self, *args, **kwargs):
        self.usage_key = get_usage_key()
        self.modulestore = get_modulestore()
        super(AnswerProblem, self).__init__(*args, **kwargs)

    def get_problem_locator_descriptor(self, problem_id):
        locator = self.usage_key.from_string(problem_id)
        descriptor = self.modulestore().get_item(locator)

        return locator, descriptor

    def get_post_data(self, request, problem_locator, answer):

        request.POST = request.POST.copy()
        field_name = "input_{tag}-{org}-{course}-{category}-{name}_2_1"
        field_key = {
            'tag': problem_locator.tag,
            'org': problem_locator.org,
            'course': problem_locator.course,
            'category': problem_locator.category,
            'name': problem_locator.name,
        }

        field = field_name.format(**field_key)
        post_data = QueryDict('', mutable=True)
        post_data[field] = answer

        return post_data

    def call_xblock_handler(self, request, location, problem_locator, answer):

        locator = self.usage_key.from_string(location)
        course_id = locator.course_key.to_deprecated_string()
        usage_id = problem_locator.to_deprecated_string()
        usage_id = usage_id.replace('/', ';_')
        handler = 'xmodule_handler'
        suffix = 'problem_check'
        user = request.user
        request.POST = self.get_post_data(request, problem_locator, answer)

        return invoke_xblock_handler(request, course_id, usage_id, handler, suffix, user)

    def post(self, request, *args, **kwargs):
        response_data = {}

        location = kwargs.get('location')
        problem_id = request.DATA.get('problem')
        answer = request.DATA.get('answer')

        problem_locator, problem_descriptor = self.get_problem_locator_descriptor(problem_id)

        if 'multiplechoiceresponse' in problem_descriptor.data:
            answer = "choice_{}".format(answer)

        result = self.call_xblock_handler(request, location, problem_locator, answer)
        content = json.loads(result.content)
        response_data = {
            'correct': content.get('success') == 'correct',
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
