from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.shortcuts import render
from django.core.urlresolvers import reverse

from labster.models import Lab


class LabForm(ModelForm):
	class Meta:
		model = Lab
		fields = ['name', 'description', 'objective', 'engine_xml', 'url', 'wiki_url', 'screenshot']


def lists(request):
	list_labs = Lab.objects.all()
	context = {'list_labs': list_labs}
	return render(request, 'labs/list_lab.html', {'list_labs': list_labs})


def add_lab(request):
	if request.method == 'POST':
		form = LabForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/labster/labs/lists')
	else:
		form = LabForm()

	return render(request, 'labs/add_lab.html', {'form': form})