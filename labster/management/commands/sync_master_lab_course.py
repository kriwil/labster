from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from contentstore.views.course import _users_assign_default_role
from courseware.courses import get_course_by_id
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.exceptions import InvalidLocationError

from django_comment_common.utils import seed_permissions_roles

from student import auth
from student.models import CourseEnrollment
from student.roles import CourseInstructorRole, CourseStaffRole
from student.roles import CourseRole

from labster.constants import COURSE_ID, ADMIN_USER_ID


class Command(BaseCommand):
    """
    Management command to sync master course

    Check cms/djangoapps/contentstore/views/course.py:create_new_course()
    to see how course is created
    """

    def handle(self, *args, **options):
        try:
            user = User.objects.get(id=ADMIN_USER_ID)

            display_name = "LabsterX Master"
            org, number, run = COURSE_ID.split('/')

            course_key = SlashSeparatedCourseKey(org, number, run)

            metadata = {'display_name': display_name}

            wiki_slug = u"{0}.{1}.{2}".format(course_key.org, course_key.course, course_key.run)
            definition_data = {'wiki_slug': wiki_slug}

            if CourseRole.course_group_already_exists(course_key):
                raise InvalidLocationError()

            fields = {}
            fields.update(definition_data)
            fields.update(metadata)

            new_course = modulestore().create_course(
                course_key.org,
                course_key.offering,
                fields=fields,
            )

            CourseInstructorRole(new_course.id).add_users(user)
            auth.add_users(user, CourseStaffRole(new_course.id), user)

            seed_permissions_roles(new_course.id)

            CourseEnrollment.enroll(user, new_course.id)
            _users_assign_default_role(new_course.id)

            course_item = new_course

        except InvalidLocationError:
            self.stdout.write("course {} exists\n".format(COURSE_ID))
            course_item = get_course_by_id(course_key)

        self.stdout.write("name: {}\n".format(course_item.display_name))
        # for section in course_item.get_children():
        #     for sub_section in section.get_children():
        #         print sub_section
