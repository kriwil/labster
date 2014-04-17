from django import forms

from labster.models import Lab
from labster.widgets import WYMEditor


class LabAdminForm(forms.ModelForm):
    description = forms.CharField(widget=WYMEditor)

    class Meta:
        model = Lab
