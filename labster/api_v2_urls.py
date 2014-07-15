from django.conf.urls import patterns, url

from labster.api.views import CreateUserSave, CreateErrorInfo, CreateDeviceInfo
from labster.api.views import CourseLab, AnswerProblem, CourseWikiDetail


urlpatterns = patterns('',  # nopep8

    url('^course-lab/(?P<location>[^\/]*)/$', CourseLab.as_view()),
    url('^course-lab/(?P<location>[^\/]*)/answer-problem/$', AnswerProblem.as_view()),

    url('^user-save/$', CreateUserSave.as_view(), name='user-save'),
    url('^error-info/$', CreateErrorInfo.as_view(), name='error-info'),
    url('^device-info/$', CreateDeviceInfo.as_view(), name='device-info'),

    url('^course-wiki-detail/$', CourseWikiDetail.as_view(), name='course-wiki-detail'),
)
