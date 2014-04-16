import json

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.http import HttpResponse

from labster.models import Lab, GameErrorInfo


class GameErrorInfoForm(ModelForm):
    class Meta:
        model = GameErrorInfo
        field = ['user', 'lab', 'browser', 'os', 'message']


def game_error_info_post(game_user_info_data):
    """
    POST:
        user_id
        lab_id
        browser
        os
        message
    """
    request = game_user_info_data.request
    user_id = int(request.POST.get('user_id'))
    lab_id = int(request.POST.get('lab_id'))
    browser = request.POST.get('browser')
    os = request.POST.get('os')
    message = request.POST.get('message')

    lab = get_object_or_404(Lab, pk=lab_id)
    user = User.objects.get(id=user_id)

    game_error_object = GameErrorInfo(user=user, lab=lab, browser=browser, os=os, message=message)
    form = GameErrorInfoForm(instance=game_error_object)
    if form.is_valid():
        form.save()

    response_data = {
        'success': 'success',
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")
