import json

from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404

from labster.models import GameUserSave


class GameUserSaveForm(ModelForm):
    class Meta:
        model = GameUserSave
        fields = ['user', 'lab', 'game_save_file']


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


def game_user_save_get(request):
    """
    GET:
        user
        lab
    """
    user_id = request.GET.get('user')
    lab_id = request.GET.get('lab')
    game_user_save = get_object_or_404(GameUserSave, user=user_id, lab=lab_id)

    template_name = "game_user_save/get_template.xml"
    context = {
        'game_user_save': game_user_save,
    }

    return render(request, template_name, context, content_type="text/xml")


@csrf_exempt
def game_user_save_block(request):
    if request.method == 'GET':
        return game_user_save_get(request)
    elif request.method == 'POST':
        return game_user_save_post(request)

    return HttpResponseNotAllowed(['GET', 'POST'])