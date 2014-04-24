import json

from django.forms import ModelForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from labster.models import GameErrorInfo


class GameErrorInfoForm(ModelForm):
    class Meta:
        model = GameErrorInfo
        fields = ['user', 'lab', 'browser', 'os', 'message']


@csrf_exempt
def game_error_post(request):
    """
    POST:
        user
        lab
        browser
        os
        message
    """
    form = GameErrorInfoForm(request.POST)
    if form.is_valid():
        form.save()
        response_data = {
            'message': 'success',
        }
    else:
        response_data = {
            'message': form.errors,
        }


    return HttpResponse(json.dumps(response_data), content_type="application/json")