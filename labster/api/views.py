from rest_framework.generics import ListAPIView, RetrieveAPIView

from labster.api.serializers import LabSerializer
from labster.models import Lab, QuizBlock, Problem


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
