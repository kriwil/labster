from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from labster.api.serializers import LabSerializer, LabProxySerializer, ProblemSerializer
from labster.models import Lab, QuizBlock, Problem, LabProxy, UserSave, ErrorInfo
from labster.models import create_lab_proxy, update_lab_proxy, UserProblem, UserLabProxy


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
        lab_id = request.DATA.get('lab_id')
        location_id = request.DATA.get('location_id')
        lab_proxy_id = request.DATA.get('lab_proxy_id')

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


class CreateUserProblem(APIView):

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user_id = data.get('user_id')
        problem_id = data.get('problem_id')
        answer = data.get('answer', "").strip()

        # user = User.objects.get(email='staff@example.com')
        user = get_object_or_404(User, id=user_id)
        problem = get_object_or_404(Problem, id=problem_id)

        user_problem = UserProblem.objects.create(problem=problem, user=user, answer=answer)
        user_lab_proxy, created = UserLabProxy.objects.get_or_create(
            user=user, lab_proxy=problem.quiz_block.lab_proxy)

        score = user_lab_proxy.get_user_score()

        response = {
            'is_correct': user_problem.is_correct,
            'score': score,
        }
        return Response(response, status=status.HTTP_201_CREATED)


class CreateUserLabProxy(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        lab_proxy_id = request.GET.get('lab_proxy_id')

        user_lab_proxy = get_object_or_404(UserLabProxy, lab_proxy_id=lab_proxy_id, user_id=user_id)
        response = {
            'id': user_lab_proxy.id,
            'completed': user_lab_proxy.completed,
        }
        return Response(response)

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user_id = data.get('user_id')
        lab_proxy_id = data.get('lab_proxy_id')
        completed = data.get('completed', False)

        user = get_object_or_404(User, id=user_id)
        lab_proxy = get_object_or_404(LabProxy, id=lab_proxy_id)

        user_lab_proxy, created = UserLabProxy.objects.get_or_create(
            user=user, lab_proxy=lab_proxy, defaults={'completed': completed})
        if not user_lab_proxy.completed:
            user_lab_proxy.completed = True
            user_lab_proxy.save()

        response = {
            'user_lab_proxy_id': user_lab_proxy.id,
            'completed': user_lab_proxy.completed,
        }

        http_status = status.HTTP_201_CREATED if created else status.HTTP_204_NO_CONTENT
        return Response(response, status=http_status)


class CreateUserSave(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        lab_proxy_id = request.GET.get('lab_proxy_id')

        user_save = get_object_or_404(UserSave, lab_proxy_id=lab_proxy_id, user_id=user_id)
        response = {
            'id': user_save.id,
            'save_file': user_save.save_file,
            'lab_proxy_id': user_save.lab_proxy.id,
        }
        return Response(response)

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user_id = data.get('user_id')
        lab_proxy_id = data.get('lab_proxy_id')
        save_file = request.FILES['save_file']

        user = get_object_or_404(User, id=user_id)
        lab_proxy = get_object_or_404(LabProxy, id=lab_proxy_id)

        user_save, created = UserSave.objects.get_or_create(
            user=user, lab_proxy=lab_proxy, save_file=save_file)        

        response = {
            'user_lab_proxy_id': user_save.lab_proxy.id,
            'id': user_save.id,
        }

        http_status = status.HTTP_201_CREATED if created else status.HTTP_204_NO_CONTENT
        return Response(response, status=http_status)


class CreateErrorInfo(APIView):

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        lab_proxy_id = request.GET.get('lab_proxy_id')

        error_info = get_object_or_404(UserSave, lab_proxy_id=lab_proxy_id, user_id=user_id)
        response = {
            'id': error_info.id,
            'user_lab_proxy_id': error_info.lab_proxy.id,
            'save_file': error_info.save_file,
            'browser': error_info.browser,
            'os' : error_info.os,
            'user_agent' : error_info.user_agent,
            'message' : error_info.message,
            'date_encountered' : error_info.date_encountered,
        }
        return Response(response)

    def post(self, request, *args, **kwargs):
        data = request.DATA

        user_id = data.get('user_id')
        lab_proxy_id = data.get('lab_proxy_id')
        browser = request.GET.get('browser')
        os = request.GET.get('os')
        user_agent = request.GET.get('user_agent')
        message = request.GET.get('message')

        user = get_object_or_404(User, id=user_id)
        lab_proxy = get_object_or_404(LabProxy, id=lab_proxy_id)

        error_info, created = UserSave.objects.get_or_create(
            user=user, lab_proxy=lab_proxy, save_file=None)        

        response = {
            'id': error_info.id,
            'user_lab_proxy_id': error_info.lab_proxy.id,
            'save_file': error_info.save_file,
            'browser': error_info.browser,
            'os' : error_info.os,
            'user_agent' : error_info.user_agent,
            'message' : error_info.message,
            'date_encountered' : error_info.date_encountered,
        }

        http_status = status.HTTP_201_CREATED if created else status.HTTP_204_NO_CONTENT
        return Response(response, status=http_status)