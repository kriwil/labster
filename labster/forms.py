from django import forms

from labster.models import Lab, UserSave, ErrorInfo, DeviceInfo
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


class ErrorInfoForm(forms.ModelForm):

    class Meta:
        model = ErrorInfo
        fields = ('browser', 'os', 'message',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.lab_proxy = kwargs.pop('lab_proxy')
        super(ErrorInfoForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.required = False

    def clean(self):
        data = super(ErrorInfoForm, self).clean()
        values = [value for key, value in data.items()]
        if not any(values):
            raise forms.ValidationError("At least one field is required.")
        return data

    def save(self, *args, **kwargs):
        kwargs['commit'] = False

        instance = super(ErrorInfoForm, self).save(*args, **kwargs)
        instance.user = self.user
        instance.lab_proxy = self.lab_proxy

        return instance


class DeviceInfoForm(forms.ModelForm):

    class Meta:
        model = DeviceInfo
        fields = ('device_id', 'frame_rate', 'machine_type', 'os', 'ram', 'processor',
                  'cores', 'gpu', 'memory', 'fill_rate', 'shader_level',
                  'quality', 'misc')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.lab_proxy = kwargs.pop('lab_proxy')
        super(DeviceInfoForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.required = False

    def clean(self):
        data = super(DeviceInfoForm, self).clean()
        values = [value for key, value in data.items()]
        if not any(values):
            raise forms.ValidationError("At least one field is required.")
        return data

    def save(self, *args, **kwargs):
        kwargs['commit'] = False

        instance = super(DeviceInfoForm, self).save(*args, **kwargs)
        instance.user = self.user
        instance.lab_proxy = self.lab_proxy

        return instance
