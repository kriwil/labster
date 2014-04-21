import json

from django.forms import ModelForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from labster.models import UserDeviceInfo


class UserDeviceInfoForm(ModelForm):
    class Meta:
        model = UserDeviceInfo
        fields = ['user', 'lab', 'device_id', 'frame_rate', 'type', 'os', 'ram', 'processor', 'cores', 'gpu', 'memory', 'fill_rate', 'shader_level', 'quality', 'misc']


@csrf_exempt
def user_device_info_post(request):
    """
    POST:
        user
        lab
        device_id
        frame_rate
        type
        os
        ram
        processor
        cores
        gpu
        memory
        fill_rate
        shader_level
        date
        quality
        misc
    """
    form = UserDeviceInfoForm(request.POST)
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
