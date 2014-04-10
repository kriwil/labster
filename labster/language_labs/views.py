from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.shortcuts import render
from django.core.urlresolvers import reverse

from labster.models import LanguageLab


class LanguageForm(ModelForm):
    class Meta:
        model = LanguageLab
        field = ['language_code', 'language_name']


def index(request):
    language_labs = LanguageLab.objects.all()
    context = {'language_labs': language_labs}
    return render(request, 'language_labs/index.html', context)


def add_language_lab(request):
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/labster/language_labs/index')
    else:
        form = LanguageForm()

    return render(request, 'language_labs/add_language_lab.html', {'form': form})