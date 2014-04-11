from django import forms
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.shortcuts import render, get_object_or_404

from labster.models import Lab, LanguageLab


class LabForm(ModelForm):

    languages = forms.ModelMultipleChoiceField(queryset=LanguageLab.objects.all(),
                                               widget=CheckboxSelectMultiple)

    class Meta:
        model = Lab
        fields = ['name', 'description', 'url', 'wiki_url', 'screenshot', 'languages']


def index(request):
    list_labs = Lab.objects.all()
    context = {'list_labs': list_labs}
    return render(request, 'labs/index.html', context)


def add(request):
    if request.method == 'POST':
        form = LabForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/labster/labs/')
    else:
        form = LabForm()

    return render(request, 'labs/add.html', {'form': form})


def update(request, lab_id):
    lab = get_object_or_404(Lab, pk=lab_id)
    if request.method == 'POST':
        form = LabForm(request.POST, instance=lab)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/labster/labs/')
    else:
        form = LabForm(instance=lab)

    return render(request, 'labs/update.html', {'form': form, 'lab': lab})


def delete(request, lab_id):
    lab = get_object_or_404(Lab, pk=lab_id)
    lab.delete()
    return HttpResponseRedirect('/labster/labs/')