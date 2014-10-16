from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from labster.edx_bridge import duplicate_course


def get_course_meta(user):
    org = "LabsterX"
    number = user.email.replace('@', '.').upper()
    run = timezone.now().strftime("%Y_%m")

    return org, number, run


class CourseDuplicate(APIView):
    def post(self, request, *args, **kwargs):
        response_data = {}

        source = request.DATA.get('source')
        target = source
        course = duplicate_course(source, target, request.user)

        response_data = {'course_id': str(course.id)}

        return Response(response_data)
