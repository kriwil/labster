from lxml import etree

from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone


class LanguageLab(models.Model):
    language_code = models.CharField(max_length=4)
    language_name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.language_name


class Lab(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(default='')
    url = models.URLField(max_length=120)
    wiki_url = models.URLField(max_length=120, blank=True)
    screenshot = models.ImageField(upload_to='labster/lab/images', blank=True)
    questions = models.TextField(default='', blank=True)
    # lab can have many languages
    languages = models.ManyToManyField(LanguageLab)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name

    def get_quizblocks(self):
        return self.quizblocklab_set.all()


@receiver(pre_delete, sender=Lab)
def lab_delete(sender, instance, **kwargs):
    # Also delete the screenshot image file when deleting the Lab
    instance.screenshot.delete(False)


class QuizBlockLab(models.Model):
    lab = models.ForeignKey(Lab)
    quiz_block_id = models.CharField(max_length=64, unique=True)
    order = models.IntegerField(default=0)
    description = models.CharField(max_length=120, default='')
    questions = models.TextField(default='')

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('lab__id', 'order')

    def __unicode__(self):
        return self.quiz_block_id

    @property
    def xml(self):
        output = """<quizblock id="{id}" description="{description}">{questions}</quizblock>"""
        output = output.format(id=self.id, description=self.description,
                               questions=self.questions)
        return output

    @property
    def question_list(self):
        root = etree.fromstring(self.xml)
        problems = root.findall('problem')
        question_list = [etree.tostring(problem).strip() for problem in problems]
        return question_list

    @property
    def serialized(self):
        fields = ['lab_id', 'quiz_block_id', 'order', 'description',
                  'questions', 'xml']

        data = {each: getattr(self, each) for each in fields}
        return data


class LabProxy(models.Model):

    lab = models.ForeignKey(Lab)
    course_id = models.CharField(max_length=255)
    chapter_id = models.CharField(max_length=100)
    section_id = models.CharField(max_length=100)

    # not used?
    unit_id = models.CharField(max_length=100, default="", blank=True)
    position = models.CharField(max_length=100, default="", blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('lab', 'course_id', 'chapter_id', 'section_id')

    def __unicode__(self):
        return "Proxy for {}".format(self.lab.name)


def update_modified_at(sender, instance, **kwargs):
    instance.modified_at = timezone.now()


pre_save.connect(update_modified_at, sender=Lab)
pre_save.connect(update_modified_at, sender=QuizBlockLab)
pre_save.connect(update_modified_at, sender=LabProxy)
