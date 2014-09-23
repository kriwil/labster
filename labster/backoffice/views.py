import requests

from django.contrib.auth.decorators import login_required
from django.conf import settings

from edxmako.shortcuts import render_to_response


BASE_URL = settings.BACKOFFICE_BASE_URL
LAB_LIST_URL = '{}/api/products/'.format(BASE_URL)


def get_labs(format='json'):
    resp = requests.get(LAB_LIST_URL)
    assert resp.status_code == 200

    if format == 'string':
        return resp.content
    return resp.json


@login_required
def home(request):
    template_name = 'labster/backoffice.html'
    context = {
        'lab_list': get_labs(format='string'),
    }
    return render_to_response(template_name, context)
