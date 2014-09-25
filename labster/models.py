import binascii
import calendar
import json
import os

from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save
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
    engine_file = models.CharField(max_length=128, blank=True, default="labster.unity3d")
    use_quiz_blocks = models.BooleanField(default=False)

    # lab can have many languages
    languages = models.ManyToManyField(LanguageLab)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    url = models.URLField(max_length=120, blank=True, default="")
    wiki_url = models.URLField(max_length=120, blank=True, default="")
    screenshot = models.ImageField(upload_to='edx/labster/lab/images', blank=True)
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
    save_file = models.FileField(blank=True, null=True, upload_to='edx/labster/lab/save')
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    # these will be deleted
    play_count = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)

    class Meta:
        unique_together = ('lab_proxy', 'user')

    def get_new_save_file_name(self):
        timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
        file_name = "{}_{}_{}.zip".format(timestamp, self.lab_proxy_id, self.user_id)
        return file_name


class UserAttemptManager(models.Manager):
    def latest_for_user(self, lab_proxy, user):
        try:
            return self.get_query_set().filter(
                lab_proxy=lab_proxy, user=user).latest('created_at')
        except self.model.DoesNotExist:
            return None


class UserAttempt(models.Model):
    lab_proxy = models.ForeignKey(LabProxy)
    user = models.ForeignKey(User)
    is_finished = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(blank=True, null=True)

    objects = UserAttemptManager()

    @property
    def play(self):
        return 0

    def mark_finished(self):
        self.is_finished = True
        self.finished_at = timezone.now()
        self.save()

    def get_total_play_count(self):
        return UserAttempt.objects.filter(
            user=self.user, lab_proxy=self.lab_proxy).count()


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


class UnityLog(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    lab_proxy = models.ForeignKey(LabProxy, blank=True, null=True)

    log_type = models.CharField(max_length=100, db_index=True)
    url = models.CharField(max_length=255, default='')
    request_method = models.CharField(max_length=10, blank=True, default='')
    message = models.TextField(help_text="JSON representation of data")

    created_at = models.DateTimeField(default=timezone.now)

    def get_message(self):
        if self.message:
            return json.loads(self.message)
        return None

    def set_message(self, message):
        self.message = json.dumps(message)

    def save(self, *args, **kwargs):
        self.log_type = self.log_type.strip().upper()
        return super(UnityLog, self).save(*args, **kwargs)

    @classmethod
    def new(self, user, lab_proxy, log_type, message, url='', request_method=''):
        message = json.dumps(message)
        return self.objects.create(
            user=user, lab_proxy=lab_proxy,
            log_type=log_type, message=message, url=url, request_method=request_method)


class ProblemProxy(models.Model):
    """
    Model to store connection between quiz and the location
    """
    lab_proxy = models.ForeignKey(LabProxy)
    question = models.CharField(max_length=100, db_index=True, help_text='Question in md5')
    location = models.CharField(max_length=200)
    correct_answer = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('lab_proxy', 'question')


class UserAnswer(models.Model):
    user = models.ForeignKey(User)
    problem_proxy = models.ForeignKey(ProblemProxy)
    created_at = models.DateTimeField(default=timezone.now)

    attempt_count = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    completion_time = models.FloatField(blank=True, null=True)
    is_view_theory_clicked = models.BooleanField(default=False)
    play_count = models.IntegerField(blank=True, null=True)


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


def create_master_lab(sender, instance, created, **kwargs):
    from labster.quiz_blocks import update_master_lab
    update_master_lab(instance)
post_save.connect(create_master_lab, sender=Lab)


def update_modified_at(sender, instance, **kwargs):
    instance.modified_at = timezone.now()
pre_save.connect(update_modified_at, sender=Lab)
pre_save.connect(update_modified_at, sender=LabProxy)
pre_save.connect(update_modified_at, sender=UserSave)
pre_save.connect(update_modified_at, sender=Lab)
