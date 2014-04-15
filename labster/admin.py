from django.conf import settings
from django.contrib import admin

from labster.models import LanguageLab, Lab, QuizBlockLab, CourseProxy
from labster.forms import LabAdminForm


class BaseAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'modified_at')


class LabAdmin(BaseAdmin):
    list_display = ('name', 'description', 'url', 'wiki_url', 'screenshot')
    form = LabAdminForm


class CourseProxyAdmin(BaseAdmin):
    list_display = ('lab', 'course_id')


admin.site.register(LanguageLab)
admin.site.register(Lab, LabAdmin)
admin.site.register(QuizBlockLab, BaseAdmin)
admin.site.register(CourseProxy, CourseProxyAdmin)
