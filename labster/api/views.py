from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from courseware.courses import get_course
from courseware.model_data import FieldDataCache
from xmodule.modulestore.django import modulestore

from labster.models import LabProxy


def questions(request):
    p_id = request.GET.get('p_id')
    lab_proxy = get_object_or_404(LabProxy, id=p_id)

    course_id = lab_proxy.course_id
    chapter = lab_proxy.chapter_id
    section = lab_proxy.section_id
    user = User.objects.get(email='staff@example.com')

    course = get_course(course_id=course_id)

    # field_data_cache = FieldDataCache.cache_for_descriptor_descendents(
    #     course.id, user, course, depth=2)
    # course_module = get_module_for_descriptor(user, request, course, field_data_cache, course.id)

    chapter_descriptor = course.get_child_by(lambda m: m.url_name == chapter)
    # chapter_module = course_module.get_child_by(lambda m: m.url_name == chapter)

    section_descriptor = chapter_descriptor.get_child_by(lambda m: m.url_name == section)
    section_descriptor = modulestore().get_instance(course.id, section_descriptor.location, depth=None)

    section_field_data_cache = FieldDataCache.cache_for_descriptor_descendents(
        course.id, user, section_descriptor, depth=2)

    problemset = quizblock = []
    for each in section_field_data_cache.descriptors:
        if each.plugin_name == 'quizblock':
            len(quizblock) and problemset.append(quizblock)
            print each.quizblock_id
            quizblock = []

        if each.plugin_name == 'problem':
            xml = each.data
            if xml:
                quizblock.append(xml)

    len(quizblock) and problemset.append(quizblock)

    template_name = "api/questions.xml"
    context = {
        'problemset': problemset,
    }
    return render(request, template_name, context, content_type="text/xml")
