from edxmako.shortcuts import render_to_response
from django.shortcuts import get_object_or_404, redirect

from labster.cms.forms import QuizBlockForm, ProblemForm
from labster.models import Lab, QuizBlock, Problem


def lab_list(request):
    template_name = "labster/lab_list.html"
    labs = Lab.objects.all()
    context = {
        'labs': labs,
    }
    return render_to_response(template_name, context)


def lab_detail(request, id):
    template_name = "labster/lab_detail.html"
    lab = get_object_or_404(Lab, id=id)
    quiz_blocks = QuizBlock.objects.filter(lab_id=id)

    context = {
        'lab': lab,
        'quiz_blocks': quiz_blocks,
    }
    return render_to_response(template_name, context)


def create_quiz_block(request, lab_id):
    template_name = "labster/create_quiz_block.html"
    lab = get_object_or_404(Lab, id=lab_id)

    if request.method == 'POST':
        form = QuizBlockForm(request.POST, lab=lab)
        if form.is_valid():
            quiz_block = form.save()
            return redirect('labster_quiz_block_detail', id=quiz_block.id)

    form = QuizBlockForm(lab=lab)
    context = {
        'lab': lab,
        'form': form,
    }
    return render_to_response(template_name, context)


def quiz_block_detail(request, id):
    template_name = "labster/quiz_block_detail.html"
    quiz_block = get_object_or_404(QuizBlock, id=id)
    problems = Problem.objects.filter(quiz_block_id=id)

    context = {
        'quiz_block': quiz_block,
        'problems': problems,
    }
    return render_to_response(template_name, context)


def create_problem(request, quiz_block_id):
    template_name = "labster/create_problem.html"
    quiz_block = get_object_or_404(QuizBlock, id=quiz_block_id)

    if request.method == 'POST':
        form = ProblemForm(request.POST, quiz_block=quiz_block)
        if form.is_valid():
            form.save()
            return redirect('labster_quiz_block_detail', id=quiz_block.id)

    form = ProblemForm(quiz_block=quiz_block)
    context = {
        'quiz_block': quiz_block,
        'form': form,
    }
    return render_to_response(template_name, context)
