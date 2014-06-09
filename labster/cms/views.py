from edxmako.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

from labster.models import Lab, QuizBlock, Problem


def lab_list(self):
    template_name = "labster/lab_list.html"
    labs = Lab.objects.all()
    context = {
        'labs': labs,
    }
    return render_to_response(template_name, context)


def lab_detail(self, id):
    template_name = "labster/lab_detail.html"
    lab = get_object_or_404(Lab, id=id)
    quiz_blocks = QuizBlock.objects.filter(lab_id=id)

    context = {
        'lab': lab,
        'quiz_blocks': quiz_blocks,
    }
    return render_to_response(template_name, context)


def quiz_block_detail(self, id):
    template_name = "labster/quiz_block_detail.html"
    quiz_block = get_object_or_404(QuizBlock, id=id)
    problems = Problem.objects.filter(quiz_block_id=id)

    context = {
        'quiz_block': quiz_block,
        'problems': problems,
    }
    return render_to_response(template_name, context)
