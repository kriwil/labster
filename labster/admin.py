from django.contrib import admin

from labster.models import LanguageLab, Lab, QuizBlockLab, LabProxy
from labster.forms import LabAdminForm


class BaseAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'modified_at')


class LabProxyInlineAdmin(admin.TabularInline):
    exclude = ('created_at', 'modified_at')
    model = QuizBlockLab


class LabAdmin(BaseAdmin):
    list_display = ('name', 'description', 'url', 'wiki_url', 'screenshot')
    filter_horizontal = ('languages',)
    form = LabAdminForm
    inlines = [LabProxyInlineAdmin]


class LabProxyAdmin(BaseAdmin):
    list_display = ('lab', 'course_id', 'created_at', 'modified_at')


admin.site.register(LanguageLab)
admin.site.register(Lab, LabAdmin)
admin.site.register(QuizBlockLab, BaseAdmin)
admin.site.register(LabProxy, LabProxyAdmin)
