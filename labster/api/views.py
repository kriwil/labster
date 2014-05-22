from rest_framework.generics import ListAPIView, RetrieveAPIView

from labster.models import Lab, QuizBlock, Problem


class LabList(ListAPIView):
    model = Lab
    queryset = Lab.objects.all()


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
