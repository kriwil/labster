import binascii
import os

from lxml import etree

from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.contrib.auth.models import User


class Token(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=40, primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name

    def for_header(self):
        return "Token {}".format(self.key)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super(Token, self).save(*args, **kwargs)


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
    engine_xml = models.CharField(max_length=128, default='')
    # lab can have many languages
    languages = models.ManyToManyField(LanguageLab)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

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
    unit_id = models.CharField(max_length=100)

    # not used?
    position = models.CharField(max_length=100, default="", blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('lab', 'unit_id')
        verbose_name_plural = 'Lab proxies'

    def __unicode__(self):
        return "Proxy for {}".format(self.lab.name)


class UserSave(models.Model):
    """
    SavePoint need to be linked to LabProxy instead of Lab

    The way we designed the system, many courses could use same lab,
    with different set of questions.
    """
    lab_proxy = models.ForeignKey(LabProxy)
    user = models.ForeignKey(User)
    save_file = models.FileField(blank=True, null=True, upload_to='labster/lab/save_file')
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('lab_proxy', 'user')


@receiver(pre_delete, sender=UserSave)
def game_user_save_delete(sender, instance, **kwargs):
    # Also delete the save game file when deleting the GameUserSave
    instance.save_file.delete(False)


def update_modified_at(sender, instance, **kwargs):
    instance.modified_at = timezone.now()


pre_save.connect(update_modified_at, sender=Lab)
pre_save.connect(update_modified_at, sender=QuizBlockLab)
pre_save.connect(update_modified_at, sender=LabProxy)
pre_save.connect(update_modified_at, sender=UserSave)


class ErrorInfo(models.Model):
    user = models.ForeignKey(User)
    lab_proxy = models.ForeignKey(LabProxy)
    browser = models.CharField(max_length=64)
    os = models.CharField(default='', max_length=32)
    user_agent = models.CharField(default='', max_length=200)
    message = models.TextField(default='')
    date_encountered = models.DateTimeField(default=timezone.now)


class DeviceInfo(models.Model):
    user = models.ForeignKey(User)
    labProxy = models.ForeignKey(LabProxy)
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

    created_at = models.DateTimeField(default=timezone.now)


class QuizBlock(models.Model):
    lab = models.ForeignKey(Lab)
    lab_proxy = models.ForeignKey(LabProxy, blank=True, null=True)

    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)

    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('lab__name', 'order', 'created_at')

    def __unicode__(self):
        return self.slug

    def to_json(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'description': self.description,
            'order': self.order,
            'problems': [p.to_json() for p in self.problem_set.all()],
        }


class Problem(models.Model):
    quiz_block = models.ForeignKey(QuizBlock)

    TYPE_MULTIPLE_CHOICE = 1
    TYPE_TEXT_INPUT = 2
    TYPE_CHOICES = (
        (TYPE_MULTIPLE_CHOICE, 'multiple choice'),
        (TYPE_TEXT_INPUT, 'text input'),
    )
    problem_type = models.IntegerField(choices=TYPE_CHOICES, blank=True, null=True)

    content_markdown = models.TextField()
    content_xml = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def to_json(self):
        return {
            'id': self.id,
            'problem_type': self.problem_type,
            'content_markdown': self.content_markdown,
            'content_xml': self.content_xml,
        }


pre_save.connect(update_modified_at, sender=QuizBlock)
pre_save.connect(update_modified_at, sender=Lab)


def copy_quizblocks(lab_id, lab_proxy):
    quizblocks = QuizBlock.objects.filter(lab_id=lab_id, lab_proxy=None)

    new_quizblocks = []
    for quizblock in quizblocks:
        new_quizblock, _ = QuizBlock.objects.get_or_create(
            lab_id=lab_id,
            lab_proxy_id=lab_proxy.id,
            defaults={
                'slug': quizblock.slug,
                'description': quizblock.description,
                'order': quizblock.order,
            }
        )

        copy_problems(old_quizblock=quizblock, new_quizblock=new_quizblock)
        new_quizblocks.append(new_quizblock)

    return new_quizblocks


def copy_problems(old_quizblock, new_quizblock):

    problems = Problem.objects.filter(quiz_block_id=old_quizblock.id)

    new_problems = []
    for problem in problems:
        new_problem = Problem.objects.create(
            quiz_block_id=new_quizblock.id,
            problem_type=problem.problem_type,
            content_markdown=problem.content_markdown,
            content_xml=problem.content_xml)

        new_problems.append(new_problem)

    return new_problems


def create_lab_proxy(lab_id, unit_id):
    lab_proxy, created = LabProxy.objects.get_or_create(lab_id=lab_id, unit_id=unit_id)
    if not created:
        copy_quizblocks(lab_id, lab_proxy)

    return lab_proxy


def update_lab_proxy(lab_proxy_id, lab_id):
    # delete quizblocks and problems
    lab_proxy = LabProxy.objects.get(id=lab_proxy_id)
    lab_proxy.lab_id = lab_id
    lab_proxy.save()

    QuizBlock.objects.filter(lab_proxy_id=lab_proxy_id).delete()
    copy_quizblocks(lab_id, lab_proxy)

    return lab_proxy
