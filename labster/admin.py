from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from labster.models import (
    LanguageLab, Lab, ErrorInfo, DeviceInfo, UserSave, Token, LabProxy,
    UnityLog, UserAnswer, ProblemProxy)


class BaseAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'modified_at')


class LabAdmin(BaseAdmin):
    list_display = ('name', 'engine_xml', 'engine_file', 'use_quiz_blocks',)
    fields = ('name', 'description', 'engine_xml', 'languages', 'engine_file', 'use_quiz_blocks',
              'screenshot_url')
    filter_horizontal = ('languages',)


class LabProxyAdmin(BaseAdmin):
    list_display = ('id', 'course_from_location', 'lab', 'location', 'is_active')
    list_filter = ('is_active',)


class UserSaveAdmin(BaseAdmin):
    list_display = ('user', 'lab', 'location', 'has_file', 'modified_at')

    def lab(self, obj):
        return obj.lab_proxy.lab.name

    def location(self, obj):
        return obj.lab_proxy.location

    def has_file(self, obj):
        return obj.save_file is not None


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


class UnityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab_proxy', 'log_type', 'created_at')


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab', 'created_at')

    def lab(self, obj):
        return obj.problem_proxy.lab_proxy.lab.name

    def question(self, obj):
        return obj.problem_proxy.question


class ProblemProxyAdmin(admin.ModelAdmin):
    list_display = ('lab', 'location', 'created_at')

    def lab(self, obj):
        return obj.lab_proxy.lab.name


admin.site.register(LanguageLab)
admin.site.register(ErrorInfo, ErrorInfoAdmin)
admin.site.register(DeviceInfo, DeviceInfoAdmin)
admin.site.register(UserSave, UserSaveAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(Lab, LabAdmin)
admin.site.register(LabProxy, LabProxyAdmin)
admin.site.register(ProblemProxy, ProblemProxyAdmin)
admin.site.register(UnityLog, UnityLogAdmin)


# remove defaul UserAdmin and replace it
admin.site.unregister(User)


class CustomUserAdmin(UserAdmin):

    def set_active(self, request, queryset):
        queryset.update(is_active=True)
    set_active.short_descripion = "Set users active."

    def set_inactive(self, request, queryset):
        queryset.update(is_active=False)
    set_inactive.short_descripion = "Set users inactive."

    actions = UserAdmin.actions + [set_active, set_inactive]


admin.site.register(User, CustomUserAdmin)
