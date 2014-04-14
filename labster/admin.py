from django.contrib import admin

from labster.models import LanguageLab, Lab, QuizBlockLab
from labster.forms import LabAdminForm


class LabAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'url', 'wiki_url', 'screenshot')
    form = LabAdminForm



admin.site.register(LanguageLab)
admin.site.register(Lab, LabAdmin)
admin.site.register(QuizBlockLab)