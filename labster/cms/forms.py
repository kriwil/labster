from django import forms

from labster.models import QuizBlock, Problem


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


class ProblemForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = (
            'content_markdown',
        )

    def __init__(self, *args, **kwargs):
        self.quiz_block = kwargs.pop('quiz_block')
        super(ProblemForm, self).__init__(*args, **kwargs)

        self.fields['content_markdown'].label = "content"

    def save(self, *args, **kwargs):
        kwargs['commit'] = False

        instance = super(ProblemForm, self).save(*args, **kwargs)
        instance.quiz_block = self.quiz_block
        instance.save()

        return instance
