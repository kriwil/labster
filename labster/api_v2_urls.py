from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from labster.api.views import api_root
from labster.api.views import CreateUserSave, CreateErrorInfo, CreateDeviceInfo
from labster.api.views import LabProxyView, AnswerProblem, CourseWiki


urlpatterns = patterns('',  # nopep8

    url('^$', api_root, name='root'),
    url('^lab-proxy/(?P<location>[^\/]+)/$', LabProxyView.as_view(), name='lab-proxy-detail'),
    url('^lab-proxy/(?P<location>[^\/]+)/answer-problem/$', AnswerProblem.as_view(), name='answer-problem'),
    url('^lab-proxy/(?P<location>[^\/]+)/user-save/$', CreateUserSave.as_view(), name='user-save'),
    url('^lab-proxy/(?P<location>[^\/]+)/error-info/$', CreateErrorInfo.as_view(), name='error-info'),
    url('^lab-proxy/(?P<location>[^\/]+)/device-info/$', CreateDeviceInfo.as_view(), name='device-info'),

    url('^course-wiki/(?P<course_id>[^/]+/[^/]+/[^/]+)/?$', CourseWiki.as_view(), name='course-wiki'),
)


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['xml', 'json', 'html'])
