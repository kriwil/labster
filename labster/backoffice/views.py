import requests

from django.contrib.auth.decorators import login_required
from django.http import Http404

from edxmako.shortcuts import render_to_response


def get_base_url():
    from django.conf import settings
    return settings.LABSTER_BACKOFFICE_BASE_URL


def get_labs(format='json'):
    lab_list_url = '{}/api/products/'.format(get_base_url())

    resp = requests.get(lab_list_url)
    assert resp.status_code == 200

    if format == 'string':
        return resp.content
    return resp.json


def create_user(user, format='json'):
    post_data = {
        'email': user.email,
        'username': user.username,
        'external_id': user.id,
    }
    create_user_url = '{}/api/users/create/'.format(get_base_url())

    resp = requests.post(create_user_url, data=post_data)
    assert resp.status_code == 200

    if format == 'string':
        return resp.content
    return resp.json()


def get_user(user, format='json'):
    user_detail_url = '{}'.format(get_base_url())
    resp = requests.get(user_detail_url)
    if format == 'string':
        return resp.content
    return resp.json()


@login_required
def home(request):
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404

    template_name = 'labster/backoffice.html'

    lab_list = get_labs(format='string')
    bo_user = create_user(request.user, format='json')
    token = bo_user['token']
    backoffice = {
        'user_id': bo_user['id']
    }

    base_url = "http://localhost:9000"  # get_base_url()
    backoffice_urls = {
        'buy_lab': '{}/api/payments/create/'.format(base_url)
    }

    context = {
        'lab_list': lab_list,
        'token': token,
        'backoffice': backoffice,
        'backoffice_urls': backoffice_urls,
    }
    return render_to_response(template_name, context)
