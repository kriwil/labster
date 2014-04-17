import json

from django.forms import ModelForm
from django.http import HttpResponse

from labster.models import UserDeviceInfo


class UserDeviceInfoForm(ModelForm):
    class Meta:
        model = UserDeviceInfo
        field = ['user', 'lab', 'device_id', 'frame_rate', 'type', 'os', 'ram', 'processor', 'cores', 'gpu', 'memory', 'fill_rate', 'shader_level', 'quality', 'misc']


def user_device_info_post(user_device_info_data):
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
    request = user_device_info_data.request
    form = UserDeviceInfoForm(request.POST)
    if form.is_valid():
        form.save()

    response_data = {
        'success': 'success',
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")
