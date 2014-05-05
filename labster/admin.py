from django.contrib import admin

from labster.models import LanguageLab, Lab, QuizBlockLab, LabProxy,\
    ErrorInfo, DeviceInfo, UserSave, Token
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


class UserSaveAdmin(BaseAdmin):
    list_display = ('user', 'lab', 'save_file', 'created_at', 'modified_at')

    def lab(self, obj):
        return obj.lab_proxy.lab.name


class ErrorInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab', 'browser', 'os', 'message', 'date_encountered')

    def lab(self, obj):
        return obj.lab_proxy.lab.name


class DeviceInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab', 'device_id', 'frame_rate', 'type', 'os',
                    'ram', 'processor', 'cores', 'gpu', 'memory', 'fill_rate',
                    'shader_level', 'quality', 'misc')

    def lab(self, obj):
        return obj.lab_proxy.lab.name


class TokenAdmin(admin.ModelAdmin):
    exclude = ('key', 'created_at')
    list_display = ('name', 'key', 'created_at')


admin.site.register(LanguageLab)
admin.site.register(Lab, LabAdmin)
admin.site.register(QuizBlockLab, BaseAdmin)
admin.site.register(LabProxy, LabProxyAdmin)
admin.site.register(ErrorInfo, ErrorInfoAdmin)
admin.site.register(DeviceInfo, DeviceInfoAdmin)
admin.site.register(UserSave, UserSaveAdmin)
admin.site.register(Token, TokenAdmin)
