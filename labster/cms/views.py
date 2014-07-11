from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, Http404

from edxmako.shortcuts import render_to_response

from labster.cms.forms import QuizBlockForm, ProblemForm
from labster.edx_bridge import duplicate_lab_content
from labster.models import Lab, QuizBlock, Problem, LabProxy


def master(request):
    user = User.objects.prefetch_related("groups").get(id=request.user.id)
    request.user = user  # keep just one instance of User
    # get_master_quiz_blocks()

    parent = "location:LabsterX+LAB101+2014_LAB+sequential+32d23ce6ea7c421d9d6159f94a8376c4"  # Racheal Fuller
    source = "location:LabsterX+LAB101+2014_LAB+sequential+cfa417d79fab4e8a88a4f646988241ea"  # Flossie Wolf

    duplicate_lab_content(request.user, source, parent)
    return HttpResponse('ok')


def duplicate_lab(request):
    # FIXME use 405 instead
    if request.method != 'POST':
        raise Http404

    # FIXME validate the content
    parent_locator = request.POST.get('parent_locator')
    source_locator = request.POST.get('source_locator')
    redirect_url = request.POST.get('redirect_url')

    duplicate_lab_content(request.user, source_locator, parent_locator)
    return redirect(redirect_url)


def lab_list(request):
    template_name = "labster/lab_list.html"
    labs = Lab.objects.all()
    lab_proxies = LabProxy.objects.all()
    context = {
        'labs': labs,
        'lab_proxies': lab_proxies,
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


def lab_proxy_detail(request, id):
    template_name = "labster/lab_detail.html"
    lab_proxy = get_object_or_404(LabProxy, id=id)
    quiz_blocks = QuizBlock.objects.filter(lab_proxy_id=id)

    context = {
        'lab': lab_proxy.lab,
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
