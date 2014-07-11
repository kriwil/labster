from django.conf.urls import patterns, url

from labster.api.views import LabList, LabDetail
from labster.api.views import LabProxyList, LabProxyDetail
from labster.api.views import ProblemList, ProblemDetail
from labster.api.views import QuizBlockList, QuizBlockDetail
from labster.api.views import CreateUserProblem, CreateUserLabProxy
from labster.api.views import CreateUserSave, CreateErrorInfo, CreateDeviceInfo


urlpatterns = patterns('',  # nopep8

    url('^labs/$', LabList.as_view(), name='lab-list'),
    url('^labs/(?P<pk>\d+)/$', LabDetail.as_view(), name='lab-detail'),

    url('^quizblocks/$', QuizBlockList.as_view(), name='quiz-block-list'),
    url('^quizblocks/(?P<pk>\d+)/$', QuizBlockDetail.as_view(), name='quiz-block-detail'),

    url('^problems/$', ProblemList.as_view(), name='problem-list'),
    url('^problems/(?P<pk>\d+)/$', ProblemDetail.as_view(), name='problem-detail'),

    url('^lab-proxies/$', LabProxyList.as_view(), name='lab-proxy-list'),
    url('^lab-proxies/(?P<pk>\d+)/$', LabProxyDetail.as_view(), name='lab-proxy-detail'),

    url('^user-save/$', CreateUserSave.as_view(), name='user-save'),
    url('^error-info/$', CreateErrorInfo.as_view(), name='error-info'),
    url('^device-info/$', CreateDeviceInfo.as_view(), name='device-info'),

    url('^user-problem/$', CreateUserProblem.as_view(), name='user-problem'),
    url('^user-lab-proxy/$', CreateUserLabProxy.as_view(), name='user-lab-proxy'),

)
