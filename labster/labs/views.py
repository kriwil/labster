from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.shortcuts import render, get_object_or_404

from labster.models import Lab


class LabForm(ModelForm):
    class Meta:
        model = Lab
        fields = ['name', 'description', 'url', 'wiki_url', 'screenshot']


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

    return render(request, 'labs/add_lab.html', {'form': form})


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