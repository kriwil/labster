from django.contrib.auth.models import User
from django.shortcuts import render

from courseware.courses import get_course
from courseware.model_data import FieldDataCache
# from courseware.module_render import get_module_for_descriptor
from xmodule.modulestore.django import modulestore


def questions(request):
    course_id = "TheOrganization/CN101/2014_RUN"
    chapter = "2f85b01abbfd42e28e9e40e7b165bd1b"
    section = "f67f1514023f4be68c6171b37066c366"
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

    questions = []
    for each in section_field_data_cache.descriptors:
        if each.plugin_name == 'problem':
            xml = each.data
            if xml:
                questions.append(xml)

    template_name = "api/questions.xml"
    context = {
        'questions': questions,
    }
    return render(request, template_name, context, content_type="text/xml")
