from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from labster.api.serializers import LabSerializer, LabProxySerializer, ProblemSerializer
from labster.models import Lab, QuizBlock, Problem, LabProxy
from labster.models import create_lab_proxy, update_lab_proxy, UserProblem


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
        unit_id = request.DATA.get('unit_id')
        lab_proxy_id = request.DATA.get('lab_proxy_id')

        if lab_proxy_id:
            lab_proxy = update_lab_proxy(lab_proxy_id, lab_id)
        else:
            lab_proxy = create_lab_proxy(lab_id, unit_id)

        serializer = LabProxySerializer(lab_proxy)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LabProxyDetail(RetrieveAPIView):
    model = LabProxy
    queryset = LabProxy.objects.all()
    serializer_class = LabProxySerializer


class CreateUserProblem(APIView):

    def post(self, request, *args, **kwargs):
        data = request.DATA

        # FIXME: use real user
        # user = request.user
        user = User.objects.get(email='staff@example.com')

        problem_id = data.get('problem_id')
        answer = data.get('answer', "").strip()

        problem = get_object_or_404(Problem, id=problem_id)

        user_problem = UserProblem.objects.create(problem=problem, user=user, answer=answer)
        attempts = UserProblem.objects.filter(problem=problem, user=user).count()

        response = {
            'is_correct': user_problem.is_correct,
            'attempts': attempts,
            'score': 0,
        }
        return Response(response, status=status.HTTP_201_CREATED)
