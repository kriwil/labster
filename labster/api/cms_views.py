from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from contentstore.utils import add_instructor, initialize_permissions
from courseware.courses import get_course_by_id
from opaque_keys.edx.locations import SlashSeparatedCourseKey
from student.roles import CourseRole
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.exceptions import InvalidLocationError


def get_course_meta(user):
    org = "LabsterX"
    number = user.email.replace('@', '.').upper()
    run = timezone.now().strftime("%Y_%m")

    return org, number, run


def get_or_create_course(source_course, user):

    display_name = source_course.display_name
    org, number, run = get_course_meta(user)

    try:
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

    except InvalidLocationError:
        course = get_course_by_id(course_key)

    return course


class CourseDuplicate(APIView):
    def post(self, request, *args, **kwargs):
        response_data = {}

        source = request.DATA.get('source')
        source_course = get_course_by_id(SlashSeparatedCourseKey.from_deprecated_string(source))
        course = get_or_create_course(source_course=source_course, user=request.user)
        response_data = {'course_id': str(course.id)}

        return Response(response_data)
