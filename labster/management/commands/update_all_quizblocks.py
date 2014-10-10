from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from courseware.courses import get_course_by_id
from opaque_keys.edx.keys import UsageKey
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from xmodule.modulestore.django import modulestore

from labster.constants import ADMIN_USER_ID
from labster.quiz_blocks import update_course_lab
from labster.models import LabProxy


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.get(id=ADMIN_USER_ID)

        # course_id = args[0]
        # section_name = args[1]
        # sub_section_name = args[2]

        # org, number, run = course_id.split('/')

        # course_key = SlashSeparatedCourseKey(org, number, run)
        # course = get_course_by_id(course_key)

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

            section_name = sub_section_name = ''
            for section in course.get_children():
                for sub_section in section.get_children():
                    if str(sub_section.location) == lab_proxy.location:
                        section_name = section.display_name
                        sub_section_name = sub_section.display_name

            if not all([section_name, sub_section_name]):
                self.stdout.write('skipping {} - {} - {}\n'.format(lab_proxy.id, section_name, sub_section_name))
                continue

            update_course_lab(user, course, section_name, sub_section_name,
                              command=self, force_update=True)
