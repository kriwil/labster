import json

from django.forms import ModelForm
from django.http import HttpResponse

from labster.models import GameErrorInfo


class GameErrorInfoForm(ModelForm):
    class Meta:
        model = GameErrorInfo
        field = ['user', 'lab', 'browser', 'os', 'message']


def game_error_info_post(game_user_info_data):
    """
    POST:
        user
        lab
        browser
        os
        message
    """
    request = game_user_info_data.request
    form = GameErrorInfoForm(request.POST)
    if form.is_valid():
        form.save()

    response_data = {
        'success': 'success',
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")
