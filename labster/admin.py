from django.contrib import admin

from labster.models import LanguageLab, Lab, QuizBlockLab, LabProxy, GameErrorInfo
from labster.forms import LabAdminForm


class BaseAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'modified_at')


class LabAdmin(BaseAdmin):
    list_display = ('name', 'description', 'url', 'wiki_url', 'screenshot')
    filter_horizontal = ('languages',)
    form = LabAdminForm


class LabProxyAdmin(BaseAdmin):
    list_display = ('lab', 'course_id', 'created_at', 'modified_at')


class GameErrorInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab', 'browser', 'os', 'message', 'date_encountered')


admin.site.register(LanguageLab)
admin.site.register(Lab, LabAdmin)
admin.site.register(QuizBlockLab, BaseAdmin)
admin.site.register(LabProxy, LabProxyAdmin)
admin.site.register(GameErrorInfo, GameErrorInfoAdmin)