import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from labster.authentication import SingleTokenAuthentication
from labster.forms import UserSaveForm
from labster.models import UserSave


class SaveDetail(APIView):

    authentication_classes = (SingleTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        user_id = request.GET.get('user_id')
        lab_proxy_id = kwargs.get('lab_proxy_id')
        user_save = get_object_or_404(UserSave, user_id=user_id, lab_proxy_id=lab_proxy_id)

        template_name = "game_user_save/get_template.xml"
        context = {
            'user_save': user_save,
        }
        return render(request, template_name, context, content_type="text/xml")

    def post(self, request, **kwargs):
        user_id = request.GET.get('user_id')
        lab_proxy_id = kwargs.get('lab_proxy_id')

        form = UserSaveForm(request.POST, request.FILES,
                            user_id=user_id, lab_proxy_id=lab_proxy_id)
        response_data = {'success': True}
        status_code = 201
        if form.is_valid():
            form.save()
        else:
            status_code = 400
            response_data.update({
                'success': False,
                'errors': [],
            })

        return HttpResponse(
            json.dumps(response_data),
            status=status_code,
            content_type="application/json")


save_detail = SaveDetail.as_view()
