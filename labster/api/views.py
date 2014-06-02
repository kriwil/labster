from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response

from labster.api.serializers import LabSerializer, LabProxySerializer
from labster.models import Lab, QuizBlock, Problem, LabProxy
from labster.models import create_lab_proxy


class LabList(ListAPIView):
    model = Lab
    queryset = Lab.objects.all()
    serializer_class = LabSerializer


class LabDetail(RetrieveAPIView):
    model = Lab
    queryset = Lab.objects.all()


class QuizBlockList(ListAPIView):
    model = QuizBlock
    queryset = QuizBlock.objects.all()


class QuizBlockDetail(RetrieveAPIView):
    model = QuizBlock
    queryset = QuizBlock.objects.all()


class ProblemList(ListAPIView):
    model = Problem
    queryset = Problem.objects.all()


class ProblemDetail(RetrieveAPIView):
    model = Problem
    queryset = Problem.objects.all()


class LabProxyList(ListCreateAPIView):
    model = LabProxy
    queryset = LabProxy.objects.all()

    def create(self, request, *args, **kwargs):
        lab_id = request.DATA.get('lab_id')
        unit_id = request.DATA.get('unit_id')

        lab_proxy = create_lab_proxy(lab_id, unit_id)

        serializer = LabProxySerializer(lab_proxy)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LabProxyDetail(RetrieveAPIView):
    model = LabProxy
    queryset = LabProxy.objects.all()
