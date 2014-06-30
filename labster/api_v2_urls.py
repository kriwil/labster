from django.conf.urls import patterns, url

from labster.api.views import LabList, LabDetail
from labster.api.views import LabProxyList, LabProxyDetail
from labster.api.views import ProblemList, ProblemDetail
from labster.api.views import QuizBlockList, QuizBlockDetail
from labster.api.views import CreateUserProblem, CreateUserLabProxy, CreateUserSave, CreateErrorInfo


urlpatterns = patterns('',  # nopep8

    url('^labs/$', LabList.as_view()),
    url('^labs/(?P<pk>\d+)/$', LabDetail.as_view()),

    url('^quizblocks/$', QuizBlockList.as_view()),
    url('^quizblocks/(?P<pk>\d+)/$', QuizBlockDetail.as_view()),

    url('^problems/$', ProblemList.as_view()),
    url('^problems/(?P<pk>\d+)/$', ProblemDetail.as_view()),

    url('^lab-proxies/$', LabProxyList.as_view()),
    url('^lab-proxies/(?P<pk>\d+)/$', LabProxyDetail.as_view()),

    url('^user-problem/$', CreateUserProblem.as_view()),
    url('^user-lab-proxy/$', CreateUserLabProxy.as_view()),

    url('^user-save/$', CreateUserSave.as_view()),   
    url('^error-info/$', CreateErrorInfo.as_view), 
)
