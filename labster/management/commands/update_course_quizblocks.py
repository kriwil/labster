from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from courseware.courses import get_course_by_id
from opaque_keys.edx.locations import SlashSeparatedCourseKey

from labster.constants import ADMIN_USER_ID
from labster.quiz_blocks import update_course_lab


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.get(id=ADMIN_USER_ID)

        course_id = args[0]
        section_name = args[1]
        sub_section_name = args[2]

        org, number, run = course_id.split('/')

        course_key = SlashSeparatedCourseKey(org, number, run)
        course = get_course_by_id(course_key)

        update_course_lab(user, course, section_name, sub_section_name,
                          command=self, force_update=True)
