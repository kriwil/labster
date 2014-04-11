from django.contrib import admin
from labster.models import LanguageLab, Lab


class LabAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'url', 'wiki_url', 'screenshot')


admin.site.register(LanguageLab)
admin.site.register(Lab, LabAdmin)