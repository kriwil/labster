from django import forms

from labster.models import Lab, UserSave
from labster.widgets import WYMEditor


class LabAdminForm(forms.ModelForm):
    description = forms.CharField(widget=WYMEditor)

    class Meta:
        model = Lab


class UserSaveForm(forms.ModelForm):

    class Meta:
        model = UserSave
        fields = ('save_file',)

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        lab_proxy_id = kwargs.pop('lab_proxy_id')
        super(UserSaveForm, self).__init__(*args, **kwargs)
        self.instance, _ = UserSave.objects.get_or_create(
            user_id=user_id, lab_proxy_id=lab_proxy_id)
