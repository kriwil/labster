from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from labster.api.views import APIRoot
from labster.api.views import CreateSave, CreateError, CreateDevice
from labster.api.views import LabProxyView, AnswerProblem, Wiki, ArticleSlug
from labster.api.views import UserAuth, PlayLab, FinishLab, LabSettings
from labster.api.views import UnityPlayLab


urlpatterns = patterns('',  # nopep8

    url('^$', APIRoot.as_view(), name='root'),
    url('auth/$', UserAuth.as_view(), name='auth'),

    url('^labs/(?P<lab_id>\d+)/questions/$', LabProxyView.as_view(), name='questions'),
    url('^labs/(?P<lab_id>\d+)/answer/$', AnswerProblem.as_view(), name='answer-problem'),
    url('^labs/(?P<lab_id>\d+)/save/$', CreateSave.as_view(), name='save'),
    url('^labs/(?P<lab_id>\d+)/log/error/$', CreateError.as_view(), name='log-error'),
    url('^labs/(?P<lab_id>\d+)/log/device/$', CreateDevice.as_view(), name='log-device'),
    url('^labs/(?P<lab_id>\d+)/play/$', UnityPlayLab.as_view(), name='play'),

    url('^wiki/(?P<course_id>[^/]+/[^/]+/[^/]+)/?$', Wiki.as_view(), name='wiki'),
    # since article can have children it might conflict with course-wiki, so I add keyword article in the end
    url('^wiki/article/(?P<article_slug>.+/|)$', ArticleSlug.as_view(), name='wiki-article'),

    url('^collect-response/(?P<api_type>\w+)/$', 'labster.lms.views.collect_response'),

    url('^labs/(?P<lab_id>\d+)/settings/$', LabSettings.as_view(), name='lab-proxy-settings'),
    url('^labs/(?P<lab_id>\d+)/play-lab/$', PlayLab.as_view(), name='play-lab'),
    url('^labs/(?P<lab_id>\d+)/finish-lab/$', FinishLab.as_view(), name='finish-lab'),
)


# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['xml', 'json', 'html'])
