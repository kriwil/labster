import requests

from django.contrib.auth.decorators import login_required
from django.http import Http404

from edxmako.shortcuts import render_to_response


def get_labs(format='json'):
    from django.conf import settings

    BASE_URL = settings.LABSTER_BACKOFFICE_BASE_URL
    LAB_LIST_URL = '{}/api/products/'.format(BASE_URL)

    resp = requests.get(LAB_LIST_URL)
    assert resp.status_code == 200

    if format == 'string':
        return resp.content
    return resp.json


@login_required
def home(request):
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404

    template_name = 'labster/backoffice.html'
    context = {
        'lab_list': get_labs(format='string'),
    }
    return render_to_response(template_name, context)
