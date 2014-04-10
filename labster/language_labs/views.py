from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.shortcuts import render, get_object_or_404

from labster.models import LanguageLab


class LanguageForm(ModelForm):
    class Meta:
        model = LanguageLab
        field = ['language_code', 'language_name']


def index(request):
    language_labs = LanguageLab.objects.all()
    context = {'language_labs': language_labs}
    return render(request, 'language_labs/index.html', context)


def add(request):
    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/labster/language_labs/')
    else:
        form = LanguageForm()

    return render(request, 'language_labs/add.html', {'form': form})


def update(request, lang_id):
    lang = get_object_or_404(LanguageLab, pk=lang_id)
    if request.method == 'POST':
        form = LanguageForm(request.POST, instance=lang)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/labster/language_labs/')
    else:
        form = LanguageForm(instance=lang)

    return render(request, 'language_labs/update.html', {'form': form, 'lang': lang})


def delete(request, lang_id):
    lang = get_object_or_404(LanguageLab, pk=lang_id)
    lang.delete()
    return HttpResponseRedirect('/labster/language_labs/')