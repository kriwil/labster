import json

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from courseware.module_render import _invoke_xblock_handler
from opaque_keys.edx.keys import UsageKey
from xmodule.modulestore.django import modulestore

from labster.api.serializers import LabSerializer, LabProxySerializer, ProblemSerializer, UserSaveSerializer, ErrorInfoSerializer, DeviceInfoSerializer
from labster.models import Lab, QuizBlock, Problem, LabProxy, UserSave, ErrorInfo, DeviceInfo
from labster.models import create_lab_proxy, update_lab_proxy, UserLabProxy


def invoke_xblock_handler(*args, **kwargs):
    """
    Wrapper so it could be mocked
    """
    return _invoke_xblock_handler(*args, **kwargs)


class LabList(ListAPIView):
    model = Lab
    queryset = Lab.objects.all()
    serializer_class = LabSerializer


class LabDetail(RetrieveAPIView):
    model = Lab
    queryset = Lab.objects.all()
    serializer_class = LabSerializer


class QuizBlockList(ListAPIView):
    model = QuizBlock
    queryset = QuizBlock.objects.all()


class QuizBlockDetail(RetrieveAPIView):
    model = QuizBlock
    queryset = QuizBlock.objects.all()


class ProblemList(ListCreateAPIView):
    model = Problem
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class ProblemDetail(RetrieveUpdateDestroyAPIView):
    model = Problem
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class LabProxyList(ListCreateAPIView):
    model = LabProxy
    queryset = LabProxy.objects.all()
    serializer_class = LabProxySerializer

    def create(self, request, *args, **kwargs):
        lab_id = request.DATA.get('lab')
        location_id = request.DATA.get('location_id')
        lab_proxy_id = request.DATA.get('lab_proxy')

        if not all([lab_id, location_id]):
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        if lab_proxy_id:
            lab_proxy = update_lab_proxy(lab_proxy_id, lab_id)
        else:
            lab_proxy = create_lab_proxy(lab_id, location_id)

        serializer = LabProxySerializer(lab_proxy)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LabProxyDetail(RetrieveAPIView):
    model = LabProxy
    queryset = LabProxy.objects.all()
    serializer_class = LabProxySerializer


class CreateUserLabProxy(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user')
        lab_proxy_id = request.GET.get('lab_proxy')

        user_lab_proxy = get_object_or_404(UserLabProxy, lab_proxy_id=lab_proxy_id, user_id=user_id)
        response = {
            'id': user_lab_proxy.id,
            'completed': user_lab_proxy.completed,
        }
        return Response(response)

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user_id = data.get('user')
        lab_proxy_id = data.get('lab_proxy')
        completed = data.get('completed', False)

        user = get_object_or_404(User, id=user_id)
        lab_proxy = get_object_or_404(LabProxy, id=lab_proxy_id)

        user_lab_proxy, created = UserLabProxy.objects.get_or_create(
            user=user, lab_proxy=lab_proxy, defaults={'completed': completed})

        if not user_lab_proxy.completed:
            user_lab_proxy.completed = True
            user_lab_proxy.save()

        response = {
            'user_lab_proxy': user_lab_proxy.id,
            'completed': user_lab_proxy.completed,
        }

        http_status = status.HTTP_201_CREATED if created else status.HTTP_204_NO_CONTENT
        return Response(response, status=http_status)


class CreateUserSave(ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user')
        lab_proxy_id = request.GET.get('lab_proxy')

        user_save = get_object_or_404(UserSave, lab_proxy_id=lab_proxy_id, user_id=user_id)
        serializer = UserSaveSerializer(user_save)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user_id = data.get('user')
        lab_proxy_id = data.get('lab_proxy')

        user = get_object_or_404(User, id=user_id)
        lab_proxy = get_object_or_404(LabProxy, id=lab_proxy_id)

        try:
            user_save = UserSave.objects.get(user=user, lab_proxy=lab_proxy)
            serializer = UserSaveSerializer(instance=user_save, data={"user": user_id, "lab_proxy": lab_proxy_id}, files=request.FILES)
        except ObjectDoesNotExist:
            serializer = UserSaveSerializer(data={"user": user_id, "lab_proxy": lab_proxy_id}, files=request.FILES)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CreateErrorInfo(CreateAPIView):
    model = ErrorInfo
    serializer_class = ErrorInfoSerializer


class CreateDeviceInfo(CreateAPIView):
    model = DeviceInfo
    serializer_class = DeviceInfoSerializer


def get_lab_by_location(location):
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
    return


class CourseLab(APIView):

    def get(self, request, *args, **kwargs):
        response_data = {}
        location = kwargs.get('location')
        if location:
            response_data = get_lab_by_location(location)
        return Response(response_data)


class AnswerProblem(APIView):

    def post(self, request, *args, **kwargs):
        response_data = {}

        location = kwargs.get('location')
        locator = UsageKey.from_string(location)
        problem_id = request.DATA.get('problem')
        answer = request.DATA.get('answer')
        problem_locator = UsageKey.from_string(problem_id)
        problem_descriptor = modulestore().get_item(problem_locator)

        course_id = locator.course_key.to_deprecated_string()
        usage_id = problem_locator.to_deprecated_string()
        usage_id = usage_id.replace('/', ';_')
        handler = 'xmodule_handler'
        suffix = 'problem_check'
        user = request.user

        request.POST = request.POST.copy()
        field_name = "input_{tag}-{org}-{course}-{category}-{name}_2_1"
        field_key = {
            'tag': problem_locator.tag,
            'org': problem_locator.org,
            'course': problem_locator.course,
            'category': problem_locator.category,
            'name': problem_locator.name,
        }

        if 'multiplechoiceresponse' in problem_descriptor.data:
            answer = "choice_{}".format(answer)

        field = field_name.format(**field_key)
        post_data = QueryDict('', mutable=True)
        post_data[field] = answer

        request.POST = post_data
        result = invoke_xblock_handler(request, course_id, usage_id, handler, suffix, user)
        content = json.loads(result.content)
        response_data = {
            'correct': content.get('success') == 'correct',
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
