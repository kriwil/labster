from django.contrib import admin

from labster.models import LanguageLab, Lab, QuizBlockLab, LabProxy, GameErrorInfo, UserDeviceInfo, GameUserSave
from labster.forms import LabAdminForm


class BaseAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'modified_at')


class LabProxyInlineAdmin(admin.TabularInline):
    exclude = ('created_at', 'modified_at')
    model = QuizBlockLab


class LabAdmin(BaseAdmin):
    list_display = ('name', 'description', 'url', 'wiki_url', 'engine_xml', 'screenshot')
    filter_horizontal = ('languages',)
    form = LabAdminForm
    inlines = [LabProxyInlineAdmin]


class LabProxyAdmin(BaseAdmin):
    list_display = ('lab', 'course_id', 'created_at', 'modified_at')


class GameErrorInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab', 'browser', 'os', 'message', 'date_encountered')


class UserDeviceInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab', 'device_id', 'frame_rate', 'type', 'os', 'ram', 'processor', 'cores', 'gpu', 'memory', 'fill_rate', 'shader_level', 'quality', 'misc')


class GameUserSaveAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab', 'game_save_file', 'created_at', 'modified_at')


admin.site.register(LanguageLab)
admin.site.register(Lab, LabAdmin)
admin.site.register(QuizBlockLab, BaseAdmin)
admin.site.register(LabProxy, LabProxyAdmin)
admin.site.register(GameErrorInfo, GameErrorInfoAdmin)
admin.site.register(UserDeviceInfo, UserDeviceInfoAdmin)
admin.site.register(GameUserSave, GameUserSaveAdmin)
