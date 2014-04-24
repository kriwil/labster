from lxml import etree

from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.contrib.auth.models import User


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
    questions = models.TextField(default='', blank=True)

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
    unit_id = models.CharField(max_length=100)

    # not used?
    position = models.CharField(max_length=100, default="", blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('lab', 'course_id', 'chapter_id', 'section_id', 'unit_id')

    def __unicode__(self):
        return "Proxy for {}".format(self.lab.name)


class UserGameSaveFile(models.Model):
    lab = models.ForeignKey(Lab)
    user = models.ForeignKey(User)
    game_save_file = models.FileField(upload_to='labster/lab/game_save_file')
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)


@receiver(pre_delete, sender=UserGameSaveFile)
def game_save_file_delete(sender, instance, **kwargs):
    # Also delete the save game file when deleting the UserGameSaveFile
    instance.game_save_file.delete(False)


def update_modified_at(sender, instance, **kwargs):
    instance.modified_at = timezone.now()


pre_save.connect(update_modified_at, sender=Lab)
pre_save.connect(update_modified_at, sender=QuizBlockLab)
pre_save.connect(update_modified_at, sender=LabProxy)
pre_save.connect(update_modified_at, sender=UserGameSaveFile)


class GameErrorInfo(models.Model):
    user = models.ForeignKey(User)
    lab = models.ForeignKey(Lab)
    browser = models.CharField(max_length=64)
    os = models.CharField(default='', max_length=32)
    message = models.TextField(default='')
    date_encountered = models.DateTimeField(default=timezone.now)


class UserDeviceInfo(models.Model):
    user = models.ForeignKey(User)
    lab = models.ForeignKey(Lab)
    device_id = models.CharField(default='', max_length=128)
    frame_rate = models.CharField(default='', max_length=128)
    type = models.CharField(default='', max_length=128)
    os = models.CharField(default='', max_length=32)
    ram = models.CharField(default='', max_length=32)
    processor = models.CharField(default='', max_length=128)
    cores = models.CharField(default='', max_length=128)
    gpu = models.CharField(default='', max_length=128)
    memory = models.CharField(default='', max_length=128)
    fill_rate = models.CharField(default='', max_length=128)
    shader_level = models.CharField(default='', max_length=128)
    date = models.DateTimeField(default=timezone.now)
    quality = models.CharField(default='', max_length=128)
    misc = models.TextField(default='')
