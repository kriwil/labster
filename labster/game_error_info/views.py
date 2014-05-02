import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView

from labster.forms import ErrorInfoForm
from labster.models import LabProxy


class LogError(APIView):

    def post(self, request, **kwargs):
        user_id = request.GET.get('user_id')
        lab_proxy_id = kwargs.get('lab_proxy_id')

        user = get_object_or_404(User, id=user_id)
        lab_proxy = get_object_or_404(LabProxy, id=lab_proxy_id)

        form = ErrorInfoForm(request.POST, user=user, lab_proxy=lab_proxy)
        response_data = {'success': True}
        if form.is_valid():
            form.save()
        else:
            response_data.update({
                'success': False,
                'errors': [],
            })

        return HttpResponse(json.dumps(response_data), content_type="application/json")


log_error = LogError.as_view()
