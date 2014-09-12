from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from courseware.courses import get_course_by_id
from opaque_keys.edx.locations import SlashSeparatedCourseKey

from labster.constants import ADMIN_USER_ID, COURSE_ID
from labster.models import LabProxy
from labster.quiz_blocks import sync_surveys

from opaque_keys.edx.keys import UsageKey
from xmodule.modulestore.django import modulestore


class Command(BaseCommand):

    def get_master_survey(self):
        org, number, run = COURSE_ID.split('/')
        course_key = SlashSeparatedCourseKey(org, number, run)
        course = get_course_by_id(course_key)

        section = None
        for each in course.get_children():
            if each.display_name == 'Survey':
                section = each
                break

        return section

    def handle(self, *args, **options):
        user = User.objects.get(id=ADMIN_USER_ID)
        master_survey = self.get_master_survey()

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

            sync_surveys(course, user, master_survey=master_survey)
