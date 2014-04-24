import json

from django.forms import ModelForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from labster.models import GameUserSave


class GameUserSaveForm(ModelForm):
    class Meta:
        model = GameUserSave
        fields = ['user', 'lab', 'game_save_file']


@csrf_exempt
def game_user_save_post(request):
    """
    POST:
        user
        lab
        game_save_file
    """
    user_id = request.POST.get('user')
    lab_id = request.POST.get('lab')
    try:
        game_user_save = GameUserSave.objects.get(user=user_id, lab=lab_id)
    except GameUserSave.DoesNotExist:
        game_user_save = None

    form = GameUserSaveForm(request.POST, request.FILES, instance=game_user_save)

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