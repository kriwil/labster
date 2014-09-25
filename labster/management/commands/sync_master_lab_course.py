from django.core.management.base import BaseCommand

from labster.quiz_blocks import update_quizblocks


class Command(BaseCommand):
    """
    Management command to sync master course

    Check cms/djangoapps/contentstore/views/course.py:_create_new_course()
    to see how course is created
    """

    def handle(self, *args, **options):
        update_quizblocks(command=self, is_master=True)
