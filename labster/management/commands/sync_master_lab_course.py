import json

from lxml import etree
import requests

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.test.client import RequestFactory

from contentstore.utils import (
    add_instructor,
    initialize_permissions,
)
from contentstore.views.item import _create_item, _save_xblock
from courseware.courses import get_course_by_id
from opaque_keys.edx.keys import UsageKey
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.exceptions import InvalidLocationError

from student.roles import CourseRole

from labster.constants import COURSE_ID, ADMIN_USER_ID
from labster.models import Lab


def get_request(user=None, data=None):
    factory = RequestFactory()
    request = factory.post('/', data=data, content_type='application/json',
                           HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    request.user = user
    return request


def create_xblock(user, category, parent_location, name=None, extra_post=None):
    post_data = {
        'parent_locator': parent_location,
        'category': category,
    }

    if name:
        post_data['display_name'] = name

    if extra_post:
        post_data.update(extra_post)

    request = get_request(user, json.dumps(post_data))
    response = _create_item(request)
    response_content = json.loads(response.content)
    section_location = response_content['locator']
    usage_key = UsageKey.from_string(section_location)
    store = modulestore()

    return store.get_item(usage_key)


def update_problem(user, xblock, data, name, platform_xml):
    nullout = ["markdown"]
    metadata = {
        'display_name': name,
        'platform_xml': platform_xml,
    }

    return _save_xblock(
        user,
        xblock,
        data=data,
        nullout=nullout,
        metadata=metadata,
    )


class Command(BaseCommand):
    """
    Management command to sync master course

    Check cms/djangoapps/contentstore/views/course.py:_create_new_course()
    to see how course is created
    """

    def handle(self, *args, **options):
        try:
            user = User.objects.get(id=ADMIN_USER_ID)

            display_name = "LabsterX Master"
            org, number, run = COURSE_ID.split('/')

            course_key = SlashSeparatedCourseKey(org, number, run)
            fields = {'display_name': display_name}

            wiki_slug = u"{0}.{1}.{2}".format(course_key.org, course_key.course, course_key.run)
            definition_data = {'wiki_slug': wiki_slug}
            fields.update(definition_data)

            if CourseRole.course_group_already_exists(course_key):
                raise InvalidLocationError()

            course = modulestore().create_course(
                course_key.org,
                course_key.course,
                course_key.run,
                user.id,
                fields=fields,
            )

            # Make sure user has instructor and staff access to the new course
            add_instructor(course.id, user, user)

            # Initialize permissions for user in the new course
            initialize_permissions(course.id, user)
            self.stdout.write("name: {}\n".format(course.display_name))

        except InvalidLocationError:
            # self.stdout.write("course {} exists\n".format(COURSE_ID))
            course = get_course_by_id(course_key)

        section_dicts = {section.display_name: section for section in course.get_children()}
        course_location = course.location.to_deprecated_string()

        # required_section_names = ['Labs']
        name = 'Labs'
        if name not in section_dicts:
            self.stdout.write("creating {}\n".format(name))
            section_dicts[name] = create_xblock(user, 'chapter', course_location, name=name)

        section = section_dicts[name]
        section_location = section.location.to_deprecated_string()
        sub_section_dicts = {sub.display_name: sub for sub in section.get_children()}

        labs = Lab.objects.all()
        for lab in labs:
            if lab.name not in sub_section_dicts:
                self.stdout.write("creating {}\n".format(lab.name))
                sub_section_dicts[lab.name] = create_xblock(user, 'sequential', section_location, name=lab.name)

            quizblock_xml = lab.engine_xml.replace('Engine_', 'QuizBlocks_')
            quizblock_xml = "https://s3-us-west-2.amazonaws.com/labster/uploads/{}".format(quizblock_xml)

            response = requests.get(quizblock_xml)
            if response.status_code != 200:
                return

            tree = etree.fromstring(response.content)
            sub_section = sub_section_dicts[lab.name]
            sub_section_location = sub_section.location.to_deprecated_string()

            unit_dicts = {qb.display_name: qb for qb in sub_section.get_children()}

            for quizblock in tree.getchildren():
                name = quizblock.attrib.get('Id')
                if name not in unit_dicts:
                    self.stdout.write("creating quizblock {}\n".format(name))
                    unit_dicts[name] = create_xblock(user, 'vertical', sub_section_location, name=name)

                unit = unit_dicts[name]
                unit_location = unit.location.to_deprecated_string()
                problem_dicts = {problem.display_name: problem for problem in unit.get_children()}

                for quiz in quizblock.getchildren():
                    name = quiz.attrib.get('Id')

                    if name not in problem_dicts:
                        self.stdout.write("creating problem {}\n".format(name))
                        extra_post = {'boilerplate': "multiplechoice.yaml"}
                        problem_dicts[name] = create_xblock(user, 'problem', unit_location, extra_post=extra_post)

                    problem_xblock = problem_dicts[name]
                    data = etree.tostring(quiz, pretty_print=True)
                    update_problem(user, problem_xblock, data, name=name, platform_xml=data)
