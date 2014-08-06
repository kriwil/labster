import binascii
import os

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from django.utils import timezone


PLATFORM_NAME = 'platform'


class Token(models.Model):
    name = models.CharField(max_length=100, unique=True)
    key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def get_for_platform(self):
        obj, _ = self.objects.get_or_create(name=PLATFORM_NAME)
        return obj

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
    engine_xml = models.CharField(max_length=128, blank=True, default="")

    # lab can have many languages
    languages = models.ManyToManyField(LanguageLab)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    url = models.URLField(max_length=120, blank=True, default="")
    wiki_url = models.URLField(max_length=120, blank=True, default="")
    screenshot = models.ImageField(upload_to='labster/lab/images', blank=True)
    questions = models.TextField(default='', blank=True)

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


class LabProxy(models.Model):
    """
    Stores connection between subsection and lab
    """

    lab = models.ForeignKey(Lab, blank=True, null=True)
    location = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Lab proxies'


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
    browser = models.CharField(max_length=64, blank=True, default="")
    os = models.CharField(max_length=32, blank=True, default="")
    user_agent = models.CharField(max_length=200, blank=True, default="")
    message = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)


class DeviceInfo(models.Model):
    user = models.ForeignKey(User)
    lab_proxy = models.ForeignKey(LabProxy)

    cores = models.CharField(default="", max_length=128, blank=True)
    device_id = models.CharField(default="", max_length=128, blank=True)
    fill_rate = models.CharField(default="", max_length=128, blank=True)
    frame_rate = models.CharField(default="", max_length=128, blank=True)
    gpu = models.CharField(default="", max_length=128, blank=True)
    machine_type = models.CharField(default="", max_length=128, blank=True)
    memory = models.CharField(default="", max_length=128, blank=True)
    misc = models.TextField(default="", blank=True)
    os = models.CharField(default="", max_length=32, blank=True)
    processor = models.CharField(default="", max_length=128, blank=True)
    quality = models.CharField(default="", max_length=128, blank=True)
    ram = models.CharField(default="", max_length=32, blank=True)
    shader_level = models.CharField(default="", max_length=128, blank=True)

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


def get_or_create_lab_proxy(location, lab=None):
    location = location.strip()
    try:
        lab_proxy = LabProxy.objects.get(location=location)
        created = False
    except LabProxy.DoesNotExist:
        lab_proxy = LabProxy(location=location)
        created = True

    modified = all([lab is not None, lab_proxy.lab is not lab])
    if modified:
        lab_proxy.lab = lab

    if created or modified:
        lab_proxy.save()

    return lab_proxy


pre_save.connect(update_modified_at, sender=Lab)
pre_save.connect(update_modified_at, sender=LabProxy)
pre_save.connect(update_modified_at, sender=UserSave)
pre_save.connect(update_modified_at, sender=Lab)
