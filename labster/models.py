from django.db import models


class LanguageLab(models.Model):
	language_code = models.CharField(max_length=4)
	language_name = models.CharField(max_length=32)


class Lab(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField(default='')
	objective = models.TextField(default='')
	engine_xml = models.CharField(max_length=64)
	url = models.CharField(max_length=120)
	wiki_url = models.CharField(max_length=120)
	screenshot = models.CharField(max_length=120)	
	# lab can have many languages
	languages = models.ManyToManyField(LanguageLab)


# class CourseProxy(models.Model):

#     course_id = models.CharField(max_length=100)
#     chapter = models.CharField(max_length=100)
#     section = models.CharField(max_length=100, default="", blank=True)
#     position = models.CharField(max_length=100, default="", blank=True)
