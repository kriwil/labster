from django.conf.urls import patterns, url

from labster.api.views import CreateUserSave, CreateErrorInfo, CreateDeviceInfo
from labster.api.views import LabProxyView, AnswerProblem, CourseWiki


urlpatterns = patterns('',  # nopep8

    url('^lab-proxy/(?P<location>[^\/]*)/$', LabProxyView.as_view()),
    url('^lab-proxy/(?P<location>[^\/]*)/answer-problem/$', AnswerProblem.as_view(), name='answer-problem'),

    url('^user-save/$', CreateUserSave.as_view(), name='user-save'),
    url('^error-info/$', CreateErrorInfo.as_view(), name='error-info'),
    url('^device-info/$', CreateDeviceInfo.as_view(), name='device-info'),

    url('^course-wiki/(?P<course_id>[^/]+/[^/]+/[^/]+)/?$', CourseWiki.as_view(), name='course-wiki'),
)
