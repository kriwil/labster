from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from courseware.courses import get_course_by_id
from opaque_keys.edx.locations import SlashSeparatedCourseKey

from labster.constants import ADMIN_USER_ID
from labster.quiz_blocks import sync_quiz_xml


class Command(BaseCommand):
    """
    Management command to sync master course

    Check cms/djangoapps/contentstore/views/course.py:_create_new_course()
    to see how course is created
    """

    def handle(self, *args, **options):
        user = User.objects.get(id=ADMIN_USER_ID)
        course_id = args[0]
        org, number, run = course_id.split('/')

        course_key = SlashSeparatedCourseKey(org, number, run)
        course = get_course_by_id(course_key)

        sync_quiz_xml(course, user, command=self)
