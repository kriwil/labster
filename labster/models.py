from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


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

    def __unicode__(self):
        return self.name


@receiver(pre_delete, sender=Lab)
def lab_delete(sender, instance, **kwargs):
    # Also delete the screenshot image file when deleting the Lab
    instance.screenshot.delete(False)

# class CourseProxy(models.Model):

#     course_id = models.CharField(max_length=100)
#     chapter = models.CharField(max_length=100)
#     section = models.CharField(max_length=100, default="", blank=True)
#     position = models.CharField(max_length=100, default="", blank=True)
