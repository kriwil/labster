import json

from django.forms import ModelForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from labster.models import GameUserSave


class UserGameSaveForm(ModelForm):
    class Meta:
        model = GameUserSave
        fields = ['user', 'lab', 'game_save_file']


@csrf_exempt
def user_game_save_post(request):
    """
    POST:
        user
        lab
        game_save_file
    """
    form = UserGameSaveForm(request.POST, request.FILES)
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