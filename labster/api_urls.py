from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from labster.api.views import APIRoot
from labster.api.views import CreateSave, CreateError, CreateDevice
from labster.api.views import LabProxyView, AnswerProblem, Wiki, ArticleSlug
from labster.api.views import UserAuth, PlayLab, FinishLab


urlpatterns = patterns('',  # nopep8

    url('^$', APIRoot.as_view(), name='root'),
    url('auth/$', UserAuth.as_view(), name='auth'),
    # url('^lab-proxy/(?P<location>[^\/]+)/$', LabProxyView.as_view(), name='lab-proxy-detail'),
    # url('^lab-proxy/(?P<location>[^\/]+)/answer-problem/$', AnswerProblem.as_view(), name='answer-problem'),
    # url('^lab-proxy/(?P<location>[^\/]+)/user-save/$', CreateUserSave.as_view(), name='user-save'),
    # url('^lab-proxy/(?P<location>[^\/]+)/error-info/$', CreateErrorInfo.as_view(), name='error-info'),
    # url('^lab-proxy/(?P<location>[^\/]+)/device-info/$', CreateDeviceInfo.as_view(), name='device-info'),
    # url('^lab-proxy/(?P<location>[^\/]+)/play-lab/$', PlayLab.as_view(), name='play-lab'),
    # url('^lab-proxy/(?P<location>[^\/]+)/finish-lab/$', FinishLab.as_view(), name='finish-lab'),

    url('^labs/(?P<lab_id>[^\/]+)/questions/$', LabProxyView.as_view(), name='lab-proxy-detail'),
    url('^labs/(?P<lab_id>[^\/]+)/answer/$', AnswerProblem.as_view(), name='answer-problem'),
    url('^labs/(?P<lab_id>[^\/]+)/save/$', CreateSave.as_view(), name='save'),
    url('^labs/(?P<lab_id>[^\/]+)/error/$', CreateError.as_view(), name='error'),
    url('^labs/(?P<lab_id>[^\/]+)/device/$', CreateDevice.as_view(), name='device'),
    url('^labs/(?P<lab_id>[^\/]+)/play-lab/$', PlayLab.as_view(), name='play-lab'),
    url('^labs/(?P<lab_id>[^\/]+)/finish-lab/$', FinishLab.as_view(), name='finish-lab'),

    url('^wiki/(?P<course_id>[^/]+/[^/]+/[^/]+)/?$', Wiki.as_view(), name='wiki'),
    # since article can have children it might conflict with course-wiki, so I add keyword article in the end
    url('^wiki/(?P<article_slug>.+/|)$', ArticleSlug.as_view(), name='article_slug'),
)


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['xml', 'json', 'html'])
