from django.utils import timezone
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from labster.edx_bridge import duplicate_course, unregister_course


def get_course_meta(user):
    org = "LabsterX"
    number = user.email.replace('@', '.').upper()
    run = timezone.now().strftime("%Y_%m")

    return org, number, run


class CourseDuplicate(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request, *args, **kwargs):
        response_data = {}

        source = request.DATA.get('source')
        target = source
        extra_fields = {
            'invitation_only': True,
            'max_student_enrollments_allowed': 3,
        }
        scheme = 'https' if request.is_secure() else 'http'
        course = duplicate_course(source, target, request.user, extra_fields,
                                  http_protocol=scheme)

        unregister_course(request.user, source)

        response_data = {'course_id': str(course.id)}

        return Response(response_data)
