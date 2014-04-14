from django.db import models


class LanguageLab(models.Model):
    language_code = models.CharField(max_length=4)
    language_name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.language_name


class Lab(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(default='')
    url = models.CharField(max_length=120)
    wiki_url = models.CharField(max_length=120)
    screenshot = models.FileField(upload_to='labster/lab')
    questions = models.TextField(default='')
    # lab can have many languages
    languages = models.ManyToManyField(LanguageLab)

    def __unicode__(self):
        return self.name


class CourseProxy(models.Model):

    lab = models.ForeignKey(Lab)
    course_id = models.CharField(max_length=255)
    chapter_id = models.CharField(max_length=100)
    section_id = models.CharField(max_length=100, default="", blank=True)
    unit_id = models.CharField(max_length=100, default="", blank=True)
    position = models.CharField(max_length=100, default="", blank=True)

    def __unicode__(self):
        return "Proxy for {}".format(self.lab.name)
