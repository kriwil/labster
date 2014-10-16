from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from labster.api.cms_views import CourseDuplicate


urlpatterns = patterns('',  # nopep8
    url('^course/duplicate/$', CourseDuplicate.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])
