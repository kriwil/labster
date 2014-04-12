from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from labster.models import Lab, LanguageLab
from labster.widgets import WYMEditor


class LabAdminForm(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField(queryset=LanguageLab.objects.all(),
                                               widget=CheckboxSelectMultiple)
    description = forms.CharField(widget=WYMEditor)

    class Meta:
        model = Lab