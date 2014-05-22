from django.conf.urls import patterns, url

from labster.api.views import LabList, LabDetail
from labster.api.views import QuizBlockList, QuizBlockDetail
from labster.api.views import ProblemList, ProblemDetail


urlpatterns = patterns('',  # nopep8

    url('^labs/$', LabList.as_view()),
    url('^labs/(?P<pk>\d+)/$', LabDetail.as_view()),

    url('^quizblocks/$', QuizBlockList.as_view()),
    url('^quizblocks/(?P<pk>\d+)/$', QuizBlockDetail.as_view()),

    url('^problems/$', ProblemList.as_view()),
    url('^problems/(?P<pk>\d+)/$', ProblemDetail.as_view()),
)
