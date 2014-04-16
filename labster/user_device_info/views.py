import json

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.http import HttpResponse

from labster.models import Lab, UserDeviceInfo


class UserDeviceInfoForm(ModelForm):
    class Meta:
        model = UserDeviceInfo
        field = ['user', 'lab', 'device_id', 'frame_rate', 'type', 'os', 'ram', 'processor', 'cores', 'gpu', 'memory', 'fill_rate', 'shader_level', 'quality', 'misc']


def user_device_info_post(user_device_info_data):
    """
    POST:
        user_id
        lab_id
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
    user_id = int(request.POST.get('user_id'))
    lab_id = int(request.POST.get('lab_id'))
    device_id = request.POST.get('device_id')
    frame_rate = request.POST.get('frame_rate')
    type = request.POST.get('type')
    os = request.POST.get('os')
    ram = request.POST.get('ram')
    processor = request.POST.get('processor')
    cores = request.POST.get('cores')
    gpu = request.POST.get('gpu')
    memory = request.POST.get('memory')
    fill_rate = request.POST.get('fill_rate')
    shader_level = request.POST.get('shader_level')
    quality = request.POST.get('quality')
    misc = request.POST.get('misc')

    lab = get_object_or_404(Lab, pk=lab_id)
    user = User.objects.get(id=user_id)

    user_device_info_object = UserDeviceInfo(user=user, lab=lab, device_id=device_id, frame_rate=frame_rate, type=type, os=os, ram=ram, processor=processor, cores=cores, gpu=gpu, memory=memory, fill_rate=fill_rate, shader_level=shader_level, quality=quality, misc=misc)
    form = UserDeviceInfoForm(instance=user_device_info_object)
    if form.is_valid():
        form.save()

    response_data = {
        'success': 'success',
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")
