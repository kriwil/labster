from django.shortcuts import redirect

from labster.edx_bridge import duplicate_lab_content


def duplicate_lab(request):
    redirect_url = request.POST.get('redirect_url')

    if request.method != 'POST':
        return redirect(redirect_url)

    parent_locator = request.POST.get('parent_locator')
    source_locator = request.POST.get('source_locator')

    if not all([parent_locator, source_locator, redirect_url]):
        return redirect(redirect_url)

    duplicate_lab_content(request.user, source_locator, parent_locator)
    return redirect(redirect_url)
