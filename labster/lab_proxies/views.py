import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView

from courseware.module_render import _invoke_xblock_handler

from labster.lab_proxies import LabProxyData
from labster.models import LabProxy


def invoke_xblock_handler(**kwargs):
    """
    Wrapper so it could be mocked
    """
    return _invoke_xblock_handler(**kwargs)


class LabProxyDetail(APIView):
    """
    Fetch all quizblocks for spesific lab,
    or answer a problem from quizblocks.
    """

    def _get_user(self, request, **kwargs):
        user_id = request.GET.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = User.objects.filter(is_superuser=True)[0]
        return user

    def _get_lab_proxy_data(self, request, **kwargs):
        lab_proxy_id = kwargs.get('lab_proxy_id')
        lab_proxy = get_object_or_404(LabProxy, id=lab_proxy_id)
        user = self._get_user(request, **kwargs)
        request.user = user
        lab_proxy_data = LabProxyData(user=user, lab_proxy=lab_proxy, request=request)
        return lab_proxy_data

    def get(self, request, **kwargs):
        lab_proxy_data = self._get_lab_proxy_data(request, **kwargs)
        template_name = "api/questions.xml"
        context = {
            'lab_proxy': lab_proxy_data.lab_proxy,
            'problemset': lab_proxy_data.get_problemset(),
        }
        return render(lab_proxy_data.request, template_name, context, content_type="text/xml")

    def post(self, request, **kwargs):
        lab_proxy_data = self._get_lab_proxy_data(request, **kwargs)

        # quizblock_id = request.POST.get('quizblock_id')
        problem_id = request.POST.get('problem_id')
        answer = request.POST.get('answer')

        module = lab_proxy_data.get_problem_by_id(problem_id)

        if 'multiplechoiceresponse' in module.data:
            answer = "choice_{}".format(answer)

        # input_i4x-Labster-CS101-problem-8113409652ee470bbfbfd7a4aeca2151_2_1:choice_peeler
        field_name = "input_{tag}-{org}-{course}-{category}-{name}_2_1"
        field_name = field_name.format(**module.location.dict())

        request.POST = request.POST.copy()
        del request.POST['quizblock_id']
        del request.POST['problem_id']
        del request.POST['answer']
        request.POST[field_name] = answer

        course_id = lab_proxy_data.course.id
        usage_id = module.location.url().replace('/', ';_')
        result = invoke_xblock_handler(
            request, course_id, usage_id, 'xmodule_handler', 'problem_check',
            lab_proxy_data.user)

        content = json.loads(result.content)
        success = content.get('success') == "correct"

        response_data = {
            'success': success,
        }

        return HttpResponse(json.dumps(response_data), content_type="application/json")


lab_proxy_detail = LabProxyDetail.as_view()