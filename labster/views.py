import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView

from labster.models import LabProxy


class BaseLabProxyLogView(APIView):
    form_class = None

    def post(self, request, **kwargs):
        assert self.form_class is not None

        user_id = request.GET.get('user_id')
        lab_proxy_id = kwargs.get('lab_proxy_id')

        user = get_object_or_404(User, id=user_id)
        lab_proxy = get_object_or_404(LabProxy, id=lab_proxy_id)

        form = self.form_class(request.POST, user=user, lab_proxy=lab_proxy)
        response_data = {'success': True}
        if form.is_valid():
            form.save()
        else:
            response_data.update({
                'success': False,
                'errors': [],
            })

        return HttpResponse(json.dumps(response_data), content_type="application/json")
