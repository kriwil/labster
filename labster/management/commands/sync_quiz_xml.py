from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from courseware.courses import get_course_by_id
from opaque_keys.edx.locations import SlashSeparatedCourseKey

from labster.constants import ADMIN_USER_ID
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

    def handle(self, *args, **options):
        user = User.objects.get(id=ADMIN_USER_ID)
        if args[0] == 'all':
            self.stdout.write('updating all quiz xml\n')

            lab_proxies = LabProxy.objects.all()
            for lab_proxy in lab_proxies:

                try:
                    locator = UsageKey.from_string(lab_proxy.location)
                    descriptor = modulestore().get_item(locator)
                    course_key = descriptor.location.course_key
                    course = get_course_by_id(course_key)
                except:
                    self.stdout.write('skipping {}'.format(lab_proxy.id))
                    continue

                self.stdout.write('... {} - {} - {}\n'.format(
                    lab_proxy.id, lab_proxy.location, lab_proxy.lab.name))

                for section in course.get_children():
                    for sub_section in section.get_children():
                        if not sub_section.lab_id:
                            continue

                        sync_quiz_xml(
                            course, user, command=self,
                            section_name=section.display_name,
                            sub_section_name=sub_section.display_name)

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
