from django import forms

from labster.models import QuizBlock


class QuizBlockForm(forms.ModelForm):

    class Meta:
        model = QuizBlock
        fields = (
            'slug',
            'description',
        )

    def __init__(self, *args, **kwargs):
        self.lab = kwargs.pop('lab')
        super(QuizBlockForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False

        instance = super(QuizBlockForm, self).save(*args, **kwargs)
        instance.lab = self.lab
        instance.save()

        return instance
