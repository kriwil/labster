from django.contrib import admin

from labster.models import LanguageLab, Lab, ErrorInfo, DeviceInfo, UserSave, Token, LabProxy


class BaseAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'modified_at')


class LabAdmin(BaseAdmin):
    fields = ('name', 'description', 'engine_xml', 'languages')
    filter_horizontal = ('languages',)


class LabProxyAdmin(BaseAdmin):
    pass


class UserSaveAdmin(BaseAdmin):
    list_display = ('user', 'lab', 'is_finished', 'play_count', 'modified_at')

    def lab(self, obj):
        return obj.lab_proxy.lab.name


class ErrorInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab', 'browser', 'os', 'message', 'created_at')

    def lab(self, obj):
        return obj.lab_proxy.lab.name


class DeviceInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab', 'device_id', 'frame_rate', 'machine_type', 'os',
                    'ram', 'processor', 'cores', 'gpu', 'memory', 'fill_rate',
                    'shader_level', 'quality', 'misc')

    def lab(self, obj):
        return obj.lab_proxy.lab.name


class TokenAdmin(admin.ModelAdmin):
    exclude = ('key', 'created_at')
    list_display = ('name', 'key', 'created_at')


admin.site.register(LanguageLab)
admin.site.register(ErrorInfo, ErrorInfoAdmin)
admin.site.register(DeviceInfo, DeviceInfoAdmin)
admin.site.register(UserSave, UserSaveAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(Lab, LabAdmin)
admin.site.register(LabProxy, LabProxyAdmin)
