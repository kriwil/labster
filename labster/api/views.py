import json

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.http import QueryDict
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.renderers import XMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from labster.api.serializers import UserSaveSerializer, ErrorInfoSerializer, DeviceInfoSerializer
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


class CreateUserSave(ListCreateAPIView):

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user')
        location = kwargs.get('location')

        lab_proxy = get_object_or_404(LabProxy, location=location)
        user_save = get_object_or_404(UserSave, lab_proxy_id=lab_proxy.id, user_id=user_id)

        serializer = UserSaveSerializer(user_save)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user_id = data.get('user')
        location = kwargs.get('location')
        lab_proxy = get_or_create_lab_proxy(location=location)

        user = get_object_or_404(User, id=user_id)

        try:
            user_save = UserSave.objects.get(user=user, lab_proxy=lab_proxy)
            serializer = UserSaveSerializer(instance=user_save, data={"user": user_id, "lab_proxy": lab_proxy.id}, files=request.FILES)
        except ObjectDoesNotExist:
            serializer = UserSaveSerializer(data={"user": user_id, "lab_proxy": lab_proxy.id}, files=request.FILES)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CreateErrorInfo(CreateAPIView):
    model = ErrorInfo
    serializer_class = ErrorInfoSerializer

    def pre_save(self, obj):
        obj.lab_proxy = get_or_create_lab_proxy(location=self.kwargs.get('location'))


class CreateDeviceInfo(CreateAPIView):
    model = DeviceInfo
    serializer_class = DeviceInfoSerializer

    def pre_save(self, obj):
        obj.lab_proxy = get_or_create_lab_proxy(location=self.kwargs.get('location'))


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


class LabProxyView(APIView):

    def get(self, request, *args, **kwargs):
        response_data = {}
        location = kwargs.get('location')
        if location:
            response_data = get_lab_by_location(location)
        return Response(response_data)


class CourseWikiDetail(APIView):

    renderer_classes = (XMLRenderer,)
    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'

    def get(self, request, *args, **kwargs):
        from courseware.courses import get_course_by_id
        from course_wiki.utils import course_wiki_slug

        from wiki.models import URLPath, Article

        course_id = request.GET.get('course_id')

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


class AnswerProblem(APIView):

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
