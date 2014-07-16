from django.conf.urls import patterns, url

from labster.api.views import CreateUserSave, CreateErrorInfo, CreateDeviceInfo
from labster.api.views import LabProxyView, AnswerProblem, CourseWiki, CourseWikiArticle


urlpatterns = patterns('',  # nopep8

    url('^lab-proxy/(?P<location>[^\/]+)/$', LabProxyView.as_view(), name='lab-proxy-detail'),
    url('^lab-proxy/(?P<location>[^\/]+)/answer-problem/$', AnswerProblem.as_view(), name='answer-problem'),
    url('^lab-proxy/(?P<location>[^\/]+)/user-save/$', CreateUserSave.as_view(), name='user-save'),
    url('^lab-proxy/(?P<location>[^\/]+)/error-info/$', CreateErrorInfo.as_view(), name='error-info'),
    url('^lab-proxy/(?P<location>[^\/]+)/device-info/$', CreateDeviceInfo.as_view(), name='device-info'),

    url('^course-wiki/(?P<course_id>[^/]+/[^/]+/[^/]+)/?$', CourseWiki.as_view(), name='course-wiki'),
    # since article can have children it might conflict with course-wiki, so I add keyword article in the end
    url('^course-wiki-article/(?P<article_slug>.+/|)$', CourseWikiArticle.as_view(), name='course-wiki-article'),
)
