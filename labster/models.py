import binascii
import os

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone


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
            'template_location': '',
        }

    @property
    def studio_detail_url(self):
        return "/labster/labs/{}/".format(self.id)

    @property
    def new_quiz_block_url(self):
        return reverse('labster_create_quiz_block', args=[self.id])

    def get_quizblocks(self):
        return self.quizblocklab_set.all()


class CourseLab(models.Model):
    """
    Stores connection between subsection and lab
    """

    lab = models.ForeignKey(Lab)
    location = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.location


class LabProxy(models.Model):

    lab = models.ForeignKey(Lab)
    location_id = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('lab', 'location_id')
        verbose_name_plural = 'Lab proxies'

    def __unicode__(self):
        return "Proxy for {}".format(self.lab.name)

    @property
    def studio_detail_url(self):
        return "/labster/lab-proxies/{}/".format(self.id)


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
    lab_proxy = models.ForeignKey(LabProxy)
    device_id = models.CharField(default='', max_length=128)
    frame_rate = models.CharField(default='', max_length=128)
    machine_type = models.CharField(default='', max_length=128)
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


@receiver(pre_delete, sender=UserSave)
def game_user_save_delete(sender, instance, **kwargs):
    # Also delete the save game file when deleting the GameUserSave
    return
    # try:
    #     instance.save_file.delete(False)
    # except OSError:
    #     pass


@receiver(pre_delete, sender=Lab)
def lab_delete(sender, instance, **kwargs):
    # Also delete the screenshot image file when deleting the Lab
    return
    # instance.screenshot.delete(False)


def update_modified_at(sender, instance, **kwargs):
    instance.modified_at = timezone.now()


def fetch_labs_as_json():
    labs = Lab.objects.order_by('name')
    labs_json = [lab.to_json() for lab in labs]
    return labs_json


def get_or_create_course_lab(location, lab):
    location = location.strip()
    try:
        course_lab = CourseLab.objects.get(location=location)
    except CourseLab.DoesNotExist:
        course_lab = CourseLab(location=location)

    if course_lab.lab != lab:
        course_lab.lab = lab
        course_lab.save()

    return course_lab


pre_save.connect(update_modified_at, sender=Lab)
pre_save.connect(update_modified_at, sender=LabProxy)
pre_save.connect(update_modified_at, sender=UserSave)
pre_save.connect(update_modified_at, sender=Lab)
pre_save.connect(update_modified_at, sender=CourseLab)
