from django.conf.urls import patterns, url

from labster.api.views import LabList, LabDetail
from labster.api.views import LabProxyList, LabProxyDetail
from labster.api.views import ProblemList, ProblemDetail
from labster.api.views import QuizBlockList, QuizBlockDetail
from labster.api.views import CreateUserProblem, CreateUserLabProxy


urlpatterns = patterns('',  # nopep8

    url('^labs/$', LabList.as_view(), name='lab-list'),
    url('^labs/(?P<pk>\d+)/$', LabDetail.as_view(), name='lab-detail'),

    url('^quizblocks/$', QuizBlockList.as_view()),
    url('^quizblocks/(?P<pk>\d+)/$', QuizBlockDetail.as_view()),

    url('^problems/$', ProblemList.as_view()),
    url('^problems/(?P<pk>\d+)/$', ProblemDetail.as_view()),

    url('^lab-proxies/$', LabProxyList.as_view()),
    url('^lab-proxies/(?P<pk>\d+)/$', LabProxyDetail.as_view()),

    url('^user-problem/$', CreateUserProblem.as_view()),
    url('^user-lab-proxy/$', CreateUserLabProxy.as_view()),
)
