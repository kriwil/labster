from collections import defaultdict

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

from contentstore.utils import get_modulestore
from contentstore.views.helpers import _xmodule_recurse
from contentstore.views.item import _duplicate_item
from courseware.courses import get_course_by_id
from edxmako.shortcuts import render_to_response
from opaque_keys.edx.keys import UsageKey
from opaque_keys.edx.locations import SlashSeparatedCourseKey

from labster.cms.forms import QuizBlockForm, ProblemForm
from labster.models import Lab, QuizBlock, Problem, LabProxy


def get_master_quiz_blocks():
    course_id = "LabsterX/LAB101/2014_LAB"
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    course = get_course_by_id(course_key)

    quiz_blocks_by_lab = defaultdict(list)

    for section in course.get_children():
        for lab in section.get_children():  # sub section
            print unicode(lab.location), lab.display_name
            for quiz_blocks in lab.get_children():  # unit
                quiz_blocks_by_lab[lab.display_name].append(quiz_blocks)

    return quiz_blocks_by_lab


def master(request):
    user = User.objects.prefetch_related("groups").get(id=request.user.id)
    request.user = user  # keep just one instance of User
    # get_master_quiz_blocks()

    parent = "location:LabsterX+LAB101+2014_LAB+sequential+32d23ce6ea7c421d9d6159f94a8376c4"  # Racheal Fuller
    source = "location:LabsterX+LAB101+2014_LAB+sequential+cfa417d79fab4e8a88a4f646988241ea"  # Flossie Wolf

    parent_locator = UsageKey.from_string(parent)
    source_locator = UsageKey.from_string(source)
    source_store = get_modulestore(source_locator)
    source_item = source_store.get_item(source_locator)

    def _publish(block):
        # This is super gross, but prevents us from publishing something that
        # we shouldn't. Ideally, all modulestores would have a consistant
        # interface for publishing. However, as of now, only the DraftMongoModulestore
        # does, so we have to check for the attribute explicitly.
        store = get_modulestore(block.location)
        store.publish(block.location, request.user.id)

    for quiz_block in source_item.get_children():
        duplicated = _duplicate_item(parent_locator, quiz_block.location, quiz_block.display_name, request.user)
        item = source_store.get_item(duplicated)
        _xmodule_recurse(
            item,
            _publish
        )

    return HttpResponse('ok')


def duplicate_lab(request):
    parent_locator = UsageKey.from_string(request.POST.get('parent_locator'))
    duplicate_source_locator = UsageKey.from_string(request.POST.get('duplicate_source_locator'))
    redirect_url = request.POST.get('redirect_url')

    store = get_modulestore(duplicate_source_locator)
    source_item = store.get_item(duplicate_source_locator)
    display_name = source_item.display_name

    _duplicate_item(parent_locator, duplicate_source_locator,
                    display_name, request.user)

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
