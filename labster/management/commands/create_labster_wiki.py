import os
import os.path
import time

from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.management.base import BaseCommand
from django.test.client import RequestFactory

# from wiki.forms import CreateForm
from wiki.views.article import Create
from wiki.models import URLPath


def get_admin_user():
    return User.objects.filter(is_superuser=True, is_staff=True).order_by('id')[0]


def create_wiki(user, post_data):
    # form = CreateForm(post_data)
    # assert form.is_valid()

    URLPath.objects.filter(slug=post_data['slug']).delete()

    request = RequestFactory().post('/', post_data)
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    request.user = user

    view = Create.as_view()
    response = view(request, path='')

    return response.status_code


def fetch_wiki_markdown():
    for root, dirs, files in os.walk('markdown'):
        for each in files:
            if not each.endswith('.md'):
                continue

            yield each


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        _start = time.time()

        user = get_admin_user()
        # create_wiki(user, post_data)
        for each in fetch_wiki_markdown():
            __start = time.time()
            print(each)

            path = os.path.join('markdown', each)
            with open(path, 'rb') as f:
                content = f.read()
                slug = each.split('_', 1)[1].split('.')[0]
                title = slug.replace('_', ' ')

                post_data = {
                    'title': title,
                    'slug': slug,
                    'content': content,
                    'summary': "",
                }

                created = create_wiki(user, post_data)
                print("... {}".format(created == 302))

            __end = time.time()
            print("... {}".format(__end - __start))

        _end = time.time()
        print("... {}".format(_end - _start))
