from rest_framework.generics import ListAPIView, RetrieveAPIView

from labster.models import Lab


class LabList(ListAPIView):
    model = Lab
    queryset = Lab.objects.all()


class LabDetail(RetrieveAPIView):
    model = Lab
    queryset = Lab.objects.all()
