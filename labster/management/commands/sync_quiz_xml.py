from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from courseware.courses import get_course_by_id
from opaque_keys.edx.locations import SlashSeparatedCourseKey

from labster.constants import ADMIN_USER_ID, COURSE_ID
from labster.models import LabProxy
from labster.quiz_blocks import sync_quiz_xml

from opaque_keys.edx.keys import UsageKey
from xmodule.modulestore.django import modulestore


class Command(BaseCommand):
    """
    Management command to sync master course

    Check cms/djangoapps/contentstore/views/course.py:_create_new_course()
    to see how course is created
    """

    def get_master_data(self):
        data = {}
        org, number, run = COURSE_ID.split('/')
        course_key = SlashSeparatedCourseKey(org, number, run)
        course = get_course_by_id(course_key)

        for section in course.get_children():
            if section.display_name != 'Labs':
                continue

            for sub_section in section.get_children():
                unit_data = {}

                for unit in sub_section.get_children():
                    problem_data = {}

                    for problem in unit.get_children():
                        problem_data[problem.display_name] = problem

                    unit_data[unit.display_name] = problem_data
                data[sub_section.display_name] = unit_data

        return data

    def handle(self, *args, **options):
        user = User.objects.get(id=ADMIN_USER_ID)
        if args[0] == 'all':

            master_data = None
            try:
                args_1 = args[1]
            except IndexError:
                pass
            else:
                if args_1 == 'master':
                    self.stdout.write('fetching the master\n')
                    master_data = self.get_master_data()

            self.stdout.write('updating all quiz xml\n')

            lab_proxies = LabProxy.objects.all()
            for lab_proxy in lab_proxies:

                try:
                    locator = UsageKey.from_string(lab_proxy.location)
                    descriptor = modulestore().get_item(locator)
                    course_key = descriptor.location.course_key
                    course = get_course_by_id(course_key)
                except:
                    self.stdout.write('skipping {}\n'.format(lab_proxy.id))
                    continue

                self.stdout.write('... {} - {} - {}\n'.format(
                    lab_proxy.id, course_key, lab_proxy.lab.name))

                for section in course.get_children():
                    for sub_section in section.get_children():
                        if not sub_section.lab_id:
                            continue

                        sync_quiz_xml(
                            course, user, command=self,
                            section_name=section.display_name,
                            sub_section_name=sub_section.display_name,
                            master_data=master_data, lab_name=lab_proxy.lab.name)

        else:
            course_id = args[0]
            try:
                section_name = args[1]
            except IndexError:
                section_name = ""
            try:
                sub_section_name = args[2]
            except IndexError:
                sub_section_name = ""

            org, number, run = course_id.split('/')

            course_key = SlashSeparatedCourseKey(org, number, run)
            course = get_course_by_id(course_key)

            sync_quiz_xml(course, user, command=self,
                        section_name=section_name,
                        sub_section_name=sub_section_name)
