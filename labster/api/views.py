from collections import OrderedDict
import json

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404

from courseware.courses import get_course
from courseware.model_data import FieldDataCache
from xmodule.modulestore.django import modulestore

from labster.models import LabProxy


class LabProxyData(object):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request')
        self.user = kwargs.get('user')
        self.lab_proxy = kwargs.get('lab_proxy')

        self.problemset = OrderedDict()

        course_id = self.lab_proxy.course_id
        chapter = self.lab_proxy.chapter_id
        section = self.lab_proxy.section_id
        course = get_course(course_id=course_id)

        chapter_descriptor = course.get_child_by(lambda m: m.url_name == chapter)

        section_descriptor = chapter_descriptor.get_child_by(lambda m: m.url_name == section)
        section_descriptor = modulestore().get_instance(course.id, section_descriptor.location, depth=None)

        self.section_field_data_cache = FieldDataCache.cache_for_descriptor_descendents(
            course.id, self.user, section_descriptor, depth=2)

    def get_problemset(self):
        """
        A better structured problemset
        quiz_block_id = {
            id: quizblock_id,
            module: quizblock_module,
            problems: [list, of, problem],
        }
        """

        if not self.problemset:
            problemset = OrderedDict()
            quizblock = None

            # descriptors store all the xmodule/xblock
            for each in self.section_field_data_cache.descriptors:
                if each.plugin_name == 'quizblock':
                    if quizblock and len(quizblock['problems']):
                        problemset[quizblock['id']] = quizblock
                        quizblock = None

                    quizblock = {
                        'id': each.quizblock_id,
                        'description': each.description,
                        'module': each,
                        'problems': [],
                    }

                if each.plugin_name == 'problem':
                    if each.data:
                        quizblock['problems'].append(each)

            self.problemset = problemset
        return self.problemset


def quizblock_get(lab_proxy_data):

    template_name = "api/questions.xml"
    context = {
        'lab_proxy': lab_proxy_data.lab_proxy,
        'problemset': lab_proxy_data.get_problemset(),
    }
    return render(lab_proxy_data.request, template_name, context, content_type="text/xml")


def quizblock_post(lab_proxy_data):
    """
    POST:
        quizblock_id
        problem_index
        answer
    """

    quizblock_id = 'csi-random-stuff'
    problem_index = 1
    problemset = lab_proxy_data.get_problemset()

    response_data = {
        'success': False,
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def quizblocks(request, proxy_id):
    lab_proxy = get_object_or_404(LabProxy, id=proxy_id)
    user = User.objects.get(email='staff@example.com')

    lab_proxy_data = LabProxyData(user=user, lab_proxy=lab_proxy, request=request)

    if request.method == 'GET':
        return quizblock_get(lab_proxy_data)
    elif request.method == 'POST':
        return quizblock_post(lab_proxy_data)

    return HttpResponseNotAllowed(['GET', 'POST'])
