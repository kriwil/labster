from django.conf.urls import patterns, url

from labster.api.views import LabList, LabDetail


urlpatterns = patterns('',  # nopep8

    url('^labs/$', LabList.as_view()),
    url('^labs/(?P<pk>\d+)/$', LabDetail.as_view()),
)
